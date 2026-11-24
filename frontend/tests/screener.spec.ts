import { expect, test } from "@playwright/test";

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
  await expect(next).toBeDisabled();

  await page.getByRole("button", { name: "Clear filters" }).press("Enter");
  await expect(search).toHaveValue("");
  await expect(sector).toHaveValue("");
  await expect(status).toHaveText("Showing 1–50 of 51 stocks.");
  await expect(next).toBeEnabled();
  const pageOverflows = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  expect(pageOverflows).toBe(false);
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
