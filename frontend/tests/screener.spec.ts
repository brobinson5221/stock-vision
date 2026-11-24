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
