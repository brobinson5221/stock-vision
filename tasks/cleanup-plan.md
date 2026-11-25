# Behavior-preserving screener cleanup

Simplify two pieces of `Screener.tsx` in one focused PR. Preserve API requests,
page resets, request cancellation, stale-response handling, and the accessible
loading, empty, and error states.

## Order of work

Run the current checks to establish a baseline. Then simplify the text-filter
update and derive the announced result range once, with browser coverage for
both empty states in place before changing the range calculation. Verify the
combined flow in Chromium and smoke-test the packaged app. Clarify the README's
default sorting and pagination description before review. Switch Starlette's
test client to `httpx2` and remove duplicate CI and contributor commands while
keeping the existing check jobs and local hooks.

The [cleanup checklist](cleanup-todo.md) records dependencies and verification.
The [sample delivery checklist](todo.md) continues to track its own PR gate.

## Follow-up findings

- The Graphify helper and intermediate files are absent from this checkout and
  from tracked `main`. Handle any scratch files in the checkout that owns them.
- A live data provider is separate feature work. The backend and frontend
  enforce synthetic provenance, and the UI uses the sample's sector list.

## Risks

Text filters must continue to compose with financial ranges and the selected
sort. Empty results and an out-of-range page both announce `0–0` but have
different messages. Keep their branches distinct and add a focused assertion
before editing if existing coverage misses either outcome.
