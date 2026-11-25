import { expect, test } from "@playwright/test";

test("restores sector filtering after the first stock request fails", async ({ page }) => {
  await page.route(/\/api\/stocks\?/, (route) => route.fulfill({ status: 503 }), { times: 1 });
  await page.goto("/");

  const sector = page.getByRole("combobox", { name: "Sector" });
  await expect(page.getByRole("alert")).toHaveText("Unable to load stocks. Please try reloading.");
  await expect(sector).toBeDisabled();

  await page.getByRole("button", { name: "Reload stocks" }).click();
  await expect(page.getByRole("alert")).toHaveCount(0);
  await expect(page.getByText("Data source: Offline synthetic test universe.")).toBeVisible();
  await expect(sector).toBeEnabled();
  await sector.selectOption("Utilities");
  await expect(page.getByRole("rowheader")).toHaveText("TEST45");
});

test("browses real API pages and recovers from a failed reload", async ({ page }) => {
  await page.goto("/");

  const table = page.getByRole("table");
  const status = page.getByRole("status");
  const previous = page.getByRole("button", { name: "Previous" });
  const next = page.getByRole("button", { name: "Next" });
  const reload = page.getByRole("button", { name: "Reload stocks" });

  await expect(table.getByRole("rowheader", { name: "DEMOA" })).toBeVisible();
  await expect(status).toHaveText("Showing 1–50 of 51 stocks.");
  await expect(previous).toBeDisabled();
  await expect(page.getByText("Data source: Offline synthetic test universe.")).toBeVisible();
  await expect(page.locator("time")).toHaveAttribute("datetime", "2026-11-24T15:00:00Z");
  await expect(page.getByRole("option", { name: "Utilities" })).toHaveCount(1);

  await next.click();
  await expect(status).toHaveText("Showing 51–51 of 51 stocks.");
  await expect(table.getByRole("rowheader")).toHaveText("TEST45");
  await expect(next).toBeDisabled();

  await page.route(/\/api\/stocks\?/, (route) => route.fulfill({ status: 503 }), { times: 1 });
  await reload.click();
  await expect(page.getByRole("alert")).toHaveText("Unable to load stocks. Please try reloading.");

  await reload.click();
  await expect(table.getByRole("rowheader")).toHaveText("TEST45");
  await expect(page.getByRole("alert")).toHaveCount(0);

  await previous.click();
  await expect(status).toHaveText("Showing 1–50 of 51 stocks.");
  await expect(table.getByRole("rowheader", { name: "DEMOA" })).toBeVisible();
  await page.getByRole("combobox", { name: "Sector" }).selectOption("Utilities");
  await expect(table.getByRole("rowheader")).toHaveText("TEST45");
  await expect(status).toHaveText("Showing 1–1 of 1 stock.");
  await expect(page.getByRole("option", { name: "Technology" })).toHaveCount(1);
});

test("combines search and sector filters and resets to the first page", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 720 });
  await page.goto("/");

  const search = page.getByRole("searchbox", { name: "Symbol or company" });
  const sector = page.getByRole("combobox", { name: "Sector" });
  const status = page.getByRole("status");
  const next = page.getByRole("button", { name: "Next" });
  const previous = page.getByRole("button", { name: "Previous" });

  await next.click();
  await expect(status).toHaveText("Showing 51–51 of 51 stocks.");
  await sector.selectOption("Healthcare");
  await expect(status).toHaveText("Showing 1–2 of 2 stocks.");
  await expect(previous).toBeDisabled();

  await search.fill("beTA");
  await expect(page.getByRole("rowheader")).toHaveText("DEMOB");
  await expect(status).toHaveText("Showing 1–1 of 1 stock.");
  await search.fill("Alpha");
  await expect(page.getByText("No stocks found.")).toBeVisible();
  await expect(status).toHaveText("Showing 0–0 of 0 stocks.");
  await expect(next).toBeDisabled();

  await page.getByRole("button", { name: "Clear filters" }).press("Enter");
  await expect(search).toHaveValue("");
  await expect(sector).toHaveValue("");
  await expect(status).toHaveText("Showing 1–50 of 51 stocks.");
  await expect(next).toBeEnabled();
  const pageOverflows = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  expect(pageOverflows).toBe(false);
});

test("returns to the previous page when results shrink", async ({ page }) => {
  await page.goto("/");
  const status = page.getByRole("status");
  const previous = page.getByRole("button", { name: "Previous" });
  const next = page.getByRole("button", { name: "Next" });

  await expect(status).toHaveText("Showing 1–50 of 51 stocks.");
  await page.route(/\/api\/stocks\?.*\boffset=50\b/, async (route) => {
    const response = await route.fetch();
    await route.fulfill({ response, json: { ...await response.json(), items: [], total: 50 } });
  });
  await next.click();
  await expect(status).toHaveText("Showing 0–0 of 50 stocks.");
  await expect(page.getByText("No stocks on this page. Use Previous to return.")).toBeVisible();
  await expect(next).toBeDisabled();
  await expect(previous).toBeEnabled();

  await previous.click();
  await expect(status).toHaveText("Showing 1–50 of 51 stocks.");
  await expect(previous).toBeDisabled();
});

test("cancels a pending search when a newer search returns", async ({ page }) => {
  await page.goto("/");
  const search = page.getByRole("searchbox", { name: "Symbol or company" });
  const stale = (url: URL) => url.pathname === "/api/stocks" && url.searchParams.get("q") === "Alpha";
  const responseHeld = Promise.withResolvers<void>();
  const releaseResponse = Promise.withResolvers<void>();
  await page.route(stale, async (route) => {
    const response = await route.fetch();
    responseHeld.resolve();
    await releaseResponse.promise;
    await route.fulfill({ response });
  });

  try {
    await search.fill("Alpha");
    await responseHeld.promise;
    const cancelled = page.waitForEvent("requestfailed", (request) => stale(new URL(request.url())));
    await search.fill("Beta");
    await expect(page.getByRole("rowheader")).toHaveText("DEMOB");
    releaseResponse.resolve();
    expect((await cancelled).failure()?.errorText).toContain("ABORTED");
    await expect(page.getByRole("rowheader")).toHaveText("DEMOB");
  } finally {
    releaseResponse.resolve();
  }
});

test("combines financial ranges with search and sector and shows invalid bounds", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 720 });
  await page.goto("/");

  const price = page.getByRole("group", { name: "Price (USD)" });
  const minimumPrice = price.getByLabel("Minimum");
  const maximumPrice = price.getByLabel("Maximum");
  const minimumCap = page.getByRole("group", { name: "Market cap (USD)" }).getByLabel("Minimum");
  const maximumPE = page.getByRole("group", { name: "P/E ratio" }).getByLabel("Maximum");
  const search = page.getByRole("searchbox", { name: "Symbol or company" });
  const sector = page.getByRole("combobox", { name: "Sector" });
  const status = page.getByRole("status");
  const alert = page.getByRole("alert");

  await page.getByRole("button", { name: "Next" }).click();
  await expect(status).toHaveText("Showing 51–51 of 51 stocks.");
  await maximumPrice.fill("75");
  await expect(status).toHaveText("Showing 1–5 of 5 stocks.");
  await expect(page.getByRole("button", { name: "Previous" })).toBeDisabled();

  await minimumCap.fill("0");
  await expect(status).toHaveText("Showing 1–4 of 4 stocks.");
  await search.fill("demo");
  await sector.selectOption("Healthcare");
  await expect(status).toHaveText("Showing 1–2 of 2 stocks.");
  await maximumPE.fill("20");
  await expect(page.getByRole("rowheader")).toHaveText("DEMOF");
  await expect(search).toHaveValue("demo");
  await expect(sector).toHaveValue("Healthcare");

  await minimumPrice.fill("80");
  await expect(alert).toContainText("Each minimum must be at most its maximum");
  await expect(page.getByRole("table")).toHaveCount(0);
  await minimumPrice.fill("40");
  await expect(alert).toHaveCount(0);
  await expect(page.getByRole("rowheader")).toHaveText("DEMOF");

  await maximumPrice.fill("invalid");
  await expect(alert).toContainText("Enter finite numbers");
  await page.getByRole("button", { name: "Clear filters" }).click();
  await expect(maximumPrice).toHaveValue("");
  await expect(minimumCap).toHaveValue("");
  await expect(maximumPE).toHaveValue("");
  await expect(status).toHaveText("Showing 1–50 of 51 stocks.");
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});

test("sorts by keyboard, keeps missing values last, and preserves ties between pages", async ({ page }) => {
  await page.goto("/");
  const status = page.getByRole("status");
  const symbols = page.getByRole("rowheader");
  const next = page.getByRole("button", { name: "Next" });
  const search = page.getByRole("searchbox", { name: "Symbol or company" });
  const minimumPrice = page.getByRole("group", { name: "Price (USD)" }).getByLabel("Minimum");
  const marketCap = page.getByRole("columnheader", { name: "Market cap (USD)" });
  const marketCapSort = marketCap.getByRole("button");

  await search.fill("demo");
  await minimumPrice.fill("20");
  await next.click();
  await expect(status).toHaveText("Showing 51–51 of 51 stocks.");
  await marketCapSort.press("Enter");
  await expect(marketCap).toHaveAttribute("aria-sort", "ascending");
  await expect(status).toHaveText("Showing 1–50 of 51 stocks.");
  await expect(marketCapSort).toBeFocused();
  await expect(symbols.first()).toHaveText("DEMOE");
  await expect(search).toHaveValue("demo");
  await expect(minimumPrice).toHaveValue("20");
  await next.click();
  await expect(symbols).toHaveText("DEMOC");

  await marketCapSort.press("Space");
  await expect(marketCap).toHaveAttribute("aria-sort", "descending");
  await expect(symbols.first()).toHaveText("DEMOA");
  await next.click();
  await expect(symbols).toHaveText("DEMOC");

  const sector = page.getByRole("columnheader", { name: "Sector" });
  await sector.getByRole("button").click();
  await expect(sector).toHaveAttribute("aria-sort", "ascending");
  await expect(page.locator("th[aria-sort]")).toHaveCount(1);
  await expect(status).toHaveText("Showing 1–50 of 51 stocks.");
  await expect(symbols.last()).toHaveText("TEST44");
  await next.click();
  await expect(symbols).toHaveText("TEST45");

  await page.getByRole("combobox", { name: "Sector" }).selectOption("Healthcare");
  await expect(symbols).toHaveText(["DEMOB", "DEMOF"]);
  await expect(sector).toHaveAttribute("aria-sort", "ascending");
  await page.getByRole("columnheader", { name: "Price (USD)" }).getByRole("button").click();
  await expect(symbols).toHaveText(["DEMOF", "DEMOB"]);
});
