# Repository agent toolkit inventory

Inventory date: 2026-11-23. Status: T1-T4 complete in PR #7: six selected skill
packages and 13 instruction files are copied and routed from root AGENTS.md.
The four existing skills are unchanged. Local path/metadata checks and routing
walkthroughs passed. Fresh-session automatic discovery/selection is unverified;
no new Codex session was started for this task. Application code is unchanged.
This inventory is not an independent security audit of all reference documents.

## Existing packages: preserve

All four live under `skills/` relative to this file. No replacements are planned.

| Package | Files | Comparison and provenance |
| --- | --- | --- |
| commit-message-storyteller | 5 | Includes SOURCE.md, MIT license, reference, and UI metadata. Entry differs from the current user-installed adaptation; preserve the repository version. |
| create-pr | 1 | Project-specific workflow; retains local review and PR skill references. Preserve as the owning project copy. |
| ponytail-review | 1 | Entry matches the installed ponytail 5.3.3 snapshot. Preserve. |
| pr | 3 | Entry matches the installed mattpocock-skills 1.3.2 snapshot; includes CREDITS.md and UI metadata. Preserve. |

## Selected sources and destinations

Skill destinations are `.agents/skills/<name>/`. Source versions identify the
installed snapshot, not a claim that upstream main still contains identical text.

| Skill | Source snapshot | License evidence | Required support and prerequisites |
| --- | --- | --- | --- |
| planning-and-task-breakdown | [addyosmani/agent-skills][as], plugin 0.6.17, commit `8c99fa36d90068c82d547f7c12a9d67a3e95f4ee` | Root MIT license, Addy Osmani | Entry plus root `references/definition-of-done.md`; adapt the cross-package path into the local package. No executable helper. |
| conventional-branch | [github/awesome-copilot][branch], local Codex adaptation pinned in SOURCE.md to `1683f50e94c9fd489191f73d7c8f7e2bd871bd0c` | Included MIT license, GitHub, Inc. | Four files: SKILL.md, SOURCE.md, LICENSE, agents/openai.yaml. Requires Git; no scripts. |
| frontend-ui-engineering | [addyosmani/agent-skills][as], plugin 0.6.17, same commit as planning | Root MIT license, Addy Osmani | Entry plus root `references/accessibility-checklist.md`; adapt its cross-package path. Tool examples are conditional, not tool-install instructions. |
| create-readme | User-installed Codex adaptation; [matching upstream skill][readme] inspected | Upstream [Awesome Copilot MIT license][ac-license] verified; local package has no license/source notice | Copied with upstream MIT LICENSE and explicit adaptation SOURCE.md. Exact adaptation history remains unavailable; the observed source hash below pins the installed adaptation. External example READMEs are links, not bundled dependencies. |
| modern-web-guidance | [GoogleChrome/modern-web-guidance][mw], plugin 1.0.1, commit `64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65` | Plugin root Apache-2.0 LICENSE; package metadata agrees | 211 files: entry and 210 Markdown guides (about 2 MB). Keep the selected package intact, plus license/source records. Entry uses external Node/npm CLI search/retrieve; guides alone do not install that CLI. |
| react-best-practices | [vercel/vercel-plugin][vc], installed plugin 0.54.1 | Manifest declares Apache-2.0; upstream [copyright/license notice][vc-license] verified | 75 files: entry, compiled AGENTS.md, UI metadata, 72 rule files. Include license and provenance. Wrapper README calls its runtime source 0.54.0; retain that discrepancy, use the content digest below, and verify upstream notice when copying. |

[as]: https://github.com/addyosmani/agent-skills/tree/8c99fa36d90068c82d547f7c12a9d67a3e95f4ee
[branch]: https://github.com/github/awesome-copilot/tree/1683f50e94c9fd489191f73d7c8f7e2bd871bd0c/skills/conventional-branch
[readme]: https://github.com/github/awesome-copilot/blob/main/skills/create-readme/SKILL.md
[ac-license]: https://github.com/github/awesome-copilot/blob/main/LICENSE
[mw]: https://github.com/GoogleChrome/modern-web-guidance/tree/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65
[vc]: https://github.com/vercel/vercel-plugin
[vc-license]: https://github.com/vercel/vercel-plugin/blob/main/LICENSE

## Portable adaptations and content review

- Planning and frontend entries reference files outside their source skill
  directories. Bundle only the two named references inside their respective
  packages and rewrite those paths. Mentions of other skills in the definition
  of done/accessibility checklist are optional reading, not permission to vendor
  or activate the rest of the plugin.
- Planning's plan-mode wording must describe a planning workflow, not claim to
  switch Codex runtime modes. Retain its existing human review requirement.
- React guidance includes Next.js, SWR, Tailwind, and shadcn examples. Scope it to
  the installed React/Vite stack; it must not demand new libraries or migrations
  merely because an example prefers them. The compiled AGENTS.md is reference
  material inside that skill, not a replacement for project AGENTS.md.
- Modern-web guidance invokes a mutable `@latest` npm CLI and gives host-specific
  runner/cache advice. Document network/download effects and use a reviewed CLI
  version when implementing the local copy. Never treat its permission advice
  as authorization or set a machine-specific cache path in committed guidance.
  Preserve its browser-compatibility and task-specific retrieval requirements.
- README attribution and the Vercel packaging-version discrepancy are recorded
  in their local SOURCE.md files. No adaptation author or unknown runtime commit
  has been invented.
- Existing project conventions, user instructions, and authorization boundaries
  take priority over example code or generic skill preferences. No model changes,
  hooks, plugin registration, MCP configuration, credentials, or global files are
  part of this toolkit installation.

Entry points, license evidence, package structure, and the two cross-package
references were inspected for this inventory. The full 282 web/React supporting
reference documents have been enumerated and hashed, not individually reviewed
as a security audit. Review applicable content and any executable behavior before
use; no source helpers or copied snippets were executed for T1.

## Snapshot identifiers

Tree digests cover regular files inside each source skill directory, excluding
external references/licenses. For reproducibility: form `relative/path sha256`
lines (lowercase file SHA-256), sort case-sensitively by path, join with LF and no
trailing LF, and SHA-256 the UTF-8 bytes. Preserve actual source-byte hashes;
line-ending adaptation changes hashes and must be noted when copying.

| Source skill | SHA-256 tree digest |
| --- | --- |
| planning-and-task-breakdown | `917ad60c471d96a1feeaada23645de54319bbe311e22cfa1f92303f805a42083` |
| conventional-branch | `11e9b22608a141f37096f32902ee904f13dbe7862859114e1e29510b7b8129d0` |
| frontend-ui-engineering | `0bfe7e7cad36f0ad040bc502088cfbcaa3460eea8bc4184ff9cd021f40426197` |
| create-readme | `a2d9f821aacb14233fd2d0f74c69d21ada0da605495d198d14f62f2e99ae809a` |
| modern-web-guidance | `743f5eb4f9e16a92abc2dd37004783a6d9a2aee76f07045e37ec120148c3f2a6` |
| react-best-practices | `0e1255581b92f68c75c569cc1c4bc154a2a017485ec88c8b00b4bf7e7659d719` |

## Instruction sources

All 13 selected files are installed Codex adaptations with an explicit Awesome
Copilot attribution link in their opening paragraphs. Those original sources
are in [github/awesome-copilot](https://github.com/github/awesome-copilot), whose
MIT license was inspected. Preserve those links and include the upstream license
with the copied instruction set. Exact local adaptation revision/author metadata
is absent; the observed content hashes below pin the reviewed source snapshots.
Do not relabel locally adapted text as an unchanged upstream version.

Each destination is `.agents/instructions/<topic>.instructions.md`:

| Topic | Source SHA-256 |
| --- | --- |
| context-engineering | `BE614CC359C50353DC70859E161C99CEEA313F78C178BF5BE3EBC862E47FEF99` |
| context7 | `1C96FF52C4E236167B0B18054225C4A0EA09FF964FB8DEC707A0E126B40BA350` |
| self-explanatory-code-commenting | `3C227C3521BB82E24DE711D4DD3737DBE808B93315DE1850DEC8B7C3F43A48E0` |
| update-docs-on-code-change | `85C467872652361C1CFFC819694CAB03B5D1D1D63B778578802662D0A06FF884` |
| code-review-generic | `0B1F22AB72776B112B94CB8C5C40F0DE347211068B0B73E4A9766241C6DC970E` |
| markdown | `17D9597232CF6316F4D16F730E46455EB52938C50E5E1B955907277A901C2B6D` |
| github-actions-ci-cd-best-practices | `A50FF597B9934855C4C23FA4EEF0B20879815BE641FEB4BB611E460FA2161A94` |
| codexer | `B695BDB10D75DAB869EFDF5CE7625BEE898199B7717C08A19C9976B9295D3CF2` |
| html-css-style-color-guide | `FFF4AB7D9951A7EC914F067E7676D9F36FD4F83EEA955EC52F62856990A31231` |
| playwright-typescript | `A200B4B1C829184B91CE4FF43B4548B0F96E6EFDAA87D0128AC3526EF5D1C2E6` |
| containerization-docker-best-practices | `26B288E5667B145857891FFA0AF634B914F8D4DC5887CD6B92030F2A7AE6D091` |
| instructions | `B92F5A9B1AB0FA075486FD2DC3F516C47E08557903BED7AF0236CBC281351646` |
| prompt | `271ADB01E9760727062F96AE4E3E4C51A13E8F02A26E48176C487CED091E3B37` |

The context7 and codexer copies now reference the Context7 workflow in
root AGENTS.md. Instruction authoring guidance's personal-environment examples
are context, not installation targets. Do not copy the full global instruction
router into the project. Project AGENTS.md now links the local copies conditionally.

## Named copying batches

Each batch is a coherent commit. Record source/license completion in skill SOURCE.md
or this instruction inventory, and refresh it if the selected source changes.

| Batch | Contents | Planned file scope |
| --- | --- | --- |
| T2a | Planning entry, local definition-of-done reference, MIT LICENSE, SOURCE.md | 4 |
| T2b | Complete conventional-branch package | 4 |
| T2c | Frontend entry, local accessibility reference, MIT LICENSE, SOURCE.md | 4 |
| T2d | create-readme entry, upstream MIT LICENSE, adaptation SOURCE.md | 3; finish attribution first |
| T2e | Complete modern-web-guidance package plus Apache LICENSE and SOURCE.md | 213; atomic package exception so its 210 guides remain coherent |
| T2f | Complete React package plus applicable license and SOURCE.md/notice | 77; atomic package exception so rule references and compiled guide remain coherent |
| T3a | context-engineering, context7, self-explanatory-code-commenting, update-docs-on-code-change; shared upstream MIT LICENSE | 5 |
| T3b | code-review-generic, markdown, github-actions-ci-cd-best-practices, codexer, html-css-style-color-guide | 5 |
| T3c | playwright-typescript, containerization-docker-best-practices, instructions, prompt | 4 |

No source skill package contains executable helper scripts. Examples and CLI
commands in the guidance still require content review and normal authorization.
Optional custom agent definitions and unrelated plugin skills stay out of scope.

## External tools and later verification

- Git and the project's uv/Python and Node/npm environments remain prerequisites.
- Context7 requires the connected MCP tools. Copies of its instruction text do
  not configure or authenticate that connection; use the documented official-doc
  fallback when unavailable and report it.
- Web guidance's CLI uses Node/npm and network access unless a reviewed local
  installation/cache is available. Do not silently bootstrap external tools.
- React examples do not imply Next.js, SWR, Tailwind, or shadcn installations.
- T4 must validate metadata and local paths, walk through matching and unrelated
  task routing, and test fresh-session discovery where available. Nothing here
  claims these uninstalled packages have been discovered by Codex.

For updates, compare a named source revision/snapshot with the recorded digest,
review license and dependency changes, preserve project adaptations, validate
references/metadata, and submit focused commits through the same PR workflow.
Do not automatically synchronize the toolkit or overwrite existing local skills.

## T2 installation verification

All six entrypoints pass the skill-creator structural validator. Every regular
source file was byte-compared immediately after copying, and supporting files
remain unchanged after the documented entrypoint adaptations. Installed package
file counts match T2a-T2f: 4, 4, 4, 3, 213, and 77 (305 files total).
The four pre-existing packages have no diff against the merged baseline.

Planning/frontend references now resolve inside their packages. React's
unsupported host-specific validate/retrieval frontmatter was removed; its UI
metadata, rule documents, and compiled guide are retained. Modern-web guidance
uses the bundled guides first and pins optional external CLI commands to 1.0.1;
no web-guidance CLI or plugin was installed/executed; no MCP connection was configured.

The new/modified entrypoint and source-note whitespace checks pass. A full
branch `git diff --check` reports inherited whitespace in unchanged upstream
reference documents (including Markdown hard breaks). Those source bytes are
retained deliberately; this is not a claim that the full whitespace check passed.
Ruff and pre-commit remain enabled. No supporting reference documents were
independently security-audited, and fresh-session discovery is still unverified.

## T3 instruction verification

All 13 instruction files are present with the shared [upstream MIT license](instructions/LICENSE).
Sources matched their recorded T1 hashes before copying. Eleven copies remain
byte-identical to their installed source snapshots. Only these two copies differ:

- [context7](instructions/context7.instructions.md): `global AGENTS.md` becomes
  `root AGENTS.md`, whose Context7 section already defines the workflow.
- [codexer](instructions/codexer.instructions.md): `global Context7 workflow`
  becomes `Context7 workflow in root AGENTS.md`.

After these replacements, all 13 files were compared against the expected source
text. Original attribution links and authorization boundaries remain; none
contains the author's absolute home path. The copied license matches the verified
upstream MIT text already bundled with conventional-branch. Generic examples of
user/global instruction scopes remain explanatory, not required installation paths.
No application, global configuration, or existing skill files changed in T3.
Root AGENTS.md conditional links and routing checks are covered by T4 below; copying instruction files alone is not proof of automatic loading.
## T4 routing and integration verification

Root [AGENTS.md](../AGENTS.md) conditionally links all 13 instruction topics and
all ten local skill entrypoints. README and the implementation plan now point
to the installed repository copies. No personal global copy is required by those
links. Read matching guidance only; examples do not expand the requested work.

The local reference check resolved all 45 links present at the first check,
verified all routes stay inside the repository, and counted 13 instruction routes
and ten skill entrypoints. All ten skills passed the structural validator. Root
AGENTS.md is 8,305 bytes on disk. Final changed-document links were checked again
before submission: all 46 local links resolved. Upstream vendored examples are not treated as project links.

Manual routing walkthroughs (instruction/table interpretation, not an automated
host-selection test):

| Representative request | Expected local guidance | Scope check |
| --- | --- | --- |
| Implement a Python API change using a library | Context, code comments, documentation impact, codexer; Context7 when looking up that library | No browser-test or container instructions merely because the project is a web app |
| Build the stock table in React | Frontend UI, local web guides, React review, HTML/CSS, code/documentation guidance | No Next.js/SWR/Tailwind installation implied |
| Change a GitHub Actions workflow | GitHub Actions, code/documentation guidance, scoped review | No frontend guidance for unrelated YAML changes |
| Refresh README | create-readme and Markdown | No complete toolkit load |
| Edit project AGENTS.md | instructions, prompt, Markdown; context guidance where applicable | Preserve user authorization and existing project rules |
| Explain a general programming concept without repository work | No task-specific toolkit required | Does not force library lookup or codebase inspection |
| Context7 connection unavailable | Root documented official-source fallback and disclosure | Does not configure credentials or install MCP services |

Only structural/path checks and these manual walkthroughs are verified here.
Automatic discovery, implicit selection, and behavior in a fresh Codex session
remain untested. Verify those in a fresh session for this checkout before
claiming them; direct entrypoint links remain available for explicit use.

Updates remain manual: identify the source snapshot, compare its changes and
license/dependencies, preserve local adaptations and support files, validate
metadata/links and matching-task behavior, then submit a focused PR. No global
configuration, external tool installation, new agent chat, or application change
is part of this task. Wait for user merge of toolkit PR #7 before task 6a.


Final T4 checks passed: Ruff lint/format, 40 pytest tests, both legacy unittest cases, and pre-commit. The existing upstream httpx TestClient deprecation warning remains without test failures.
