# Playwright TypeScript tests

Adapted from [Awesome Copilot Playwright TypeScript](https://awesome-copilot.github.com/instruction/playwright-typescript/) for Codex. Apply to test suites, not one-off browser automation or unrelated application files.

## Establish the suite

Read package scripts, installed Playwright version, playwright.config.*, configured projects, testDir, testMatch, and neighboring fixtures. Keep specs in the configured suite and naming convention; use `<feature>.spec.ts` only when its matcher accepts that pattern.

Import `test, expect` from `@playwright/test` for a new basic suite; use the project's extended `test` and fixture module when one exists. Group related scenarios with `test.describe`, share appropriate setup with `beforeEach`, and use `test.step` where steps improve reporting. Preserve per-test browser contexts and isolate mutable data.

## Write resilient tests

- Prefer `getByRole`, `getByLabel`, and user-facing text. Scope locators to make their targets unambiguous.
- Await web-first assertions: `toHaveText`, `toContainText`, `toHaveCount`, `toHaveURL`, and `toBeVisible` according to the expected outcome. Visibility assertions are valid without testing a transition.
- Avoid immediate checks such as `expect(await locator.isVisible()).toBe(true)` when retrying assertions express the behavior.
- Use `toMatchAriaSnapshot` when accessibility tree structure is part of the requirement and the installed version supports it. Keep snapshots focused and review changes; do not snapshot every component by default.
- Rely on auto-waiting and meaningful state changes. Avoid fixed sleeps or global timeout increases to hide failures.
- Give tests descriptive behavior-based titles and assert outcomes after actions. Add comments only for non-obvious reasoning.

## Verify

Run the project's test script with a focused spec and configured project. Use `npx playwright test` only when consistent with the project's package manager; pass `--project=chromium` only if that project exists. Inspect failures and traces, correct their cause, and rerun affected tests. Report checks and blockers accurately. Confirm version-sensitive APIs with current official documentation through Context7 before adopting them.
