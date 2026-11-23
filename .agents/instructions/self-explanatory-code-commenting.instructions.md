# Self-explanatory code and comments

Adapted for Codex from [Awesome Copilot: Self-explanatory Code Commenting](https://awesome-copilot.github.com/instruction/self-explanatory-code-commenting/). Apply when writing or reviewing code and comments in any language.

Prefer descriptive names, clear control flow, and small understandable expressions. Comment where the code cannot communicate the reason, constraint, or contract. Improve local naming when it removes a confusing comment, while preserving public interfaces and keeping refactoring within the task's scope.

## Useful comments

- Explain non-obvious business rules, algorithm choices, units, boundary conditions, and external constraints. Link an authoritative rule or issue when it helps maintenance.
- Explain complex regular expressions and their actual limits; do not describe a simple email pattern as complete email validation.
- Record why a constant, timeout, or retry limit has its value when that reasoning is not obvious.
- Document public interfaces in the language's normal docstring/help format: inputs, outputs, side effects, errors, units, and useful examples as needed. Public API documentation may describe what the API does.
- Keep essential security, concurrency, hardware calibration, and data-loss warnings. Required license notices, tool directives, generated-file markers, and suppression explanations remain valid.
- Use TODO/FIXME/workaround annotations for concrete unresolved work, with a relevant issue or removal condition where known. Describe an existing limit honestly; never substitute a TODO for required validation, authentication, or a requested fix.

## Avoid noise and drift

Remove or update comments made inaccurate by the change. Avoid narrating obvious assignments, restating a function name, decorative divider blocks, commented-out dead code, and change-history entries already covered by version control. Keep comments close to the relevant code and as short as the explanation permits.

Before finishing, check that each changed comment adds information, accurately describes the final code, and preserves necessary contract or safety details. Do not remove useful comments merely to minimize their count. Verify any behavior changed while simplifying code with checks appropriate to the change.
