# Dataset metadata hardening

Make every sector option usable as an API filter and verify that the screener
recovers when its first request fails. The [implementation checklist](dataset-hardening-todo.md)
defines commit checkpoints and the single PR boundary.

Keep the existing 100-character query limit and share it with stock validation.
An offline dataset that contains an unusable sector name should fail validation
before it reaches the dropdown. Confirm the boundary with a 100-character
sector that can be selected and a 101-character sector that is rejected.

Use the existing Chromium fixture and fail only the first stocks request.
Verify the error, disabled sector dropdown, and manual recovery. The sector
options should reappear after Reload stocks succeeds, and selecting a sector
should work again.

After [PR #21](https://github.com/brobinson5221/stock-vision/pull/21) merges,
fetch `origin/main` and branch from it. Commit this plan and the workflow
guidance separately from the two implementation commits. Publish them in one
PR with the repository `pr` and `create-pr` skills. Verify CI on the latest
commit and leave the merge to the user.
