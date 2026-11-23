# Markdown formatting

Adapted for Codex from [Awesome Copilot: Markdown](https://awesome-copilot.github.com/instruction/markdown/), based on [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/). Apply when writing, editing, or reviewing Markdown files. Match the repository's existing renderer, style, and lint configuration. The CommonMark specification is a reference; do not download it as a task artifact.

## Blocks and structure

- Use descriptive ATX headings with one to six # characters followed by a space. Keep a logical heading hierarchy. Separate headings, paragraphs, lists, and code blocks with blank lines for predictable rendering.
- Indent nested list items to their parent's content column. Use consistent bullet markers; marker changes can start a new list. For a numbered list, use the intended start number; an ordered list interrupting a paragraph must begin with 1, so prefer a separating blank line.
- Prefix block quotes with > and use blank quote lines for paragraph separation. Avoid relying on lazy continuation where it makes scope unclear.
- A thematic break consists of at least three matching hyphens, underscores, or asterisks. Keep it distinct from list markers and setext headings. Prefer ATX headings when an underline could be misread as a break.
- Four-space indentation can create a literal code block. Tabs use four-column tab stops for block structure; avoid accidental code blocks caused by indentation.

## Code and literal text

Use fenced code blocks with matching backtick or tilde characters: at least three on the opening fence and at least as many on the closing fence. Add a useful language identifier, such as python, json, powershell, or text. Backtick fence info strings cannot contain backticks.

When showing Markdown containing fences, use an outer fence longer than any matching fence inside, or use another fence character. Use code spans for identifiers and literal syntax; choose a longer backtick delimiter if the text itself contains backticks. Code spans and code blocks preserve escapes/entities literally, subject to code-span whitespace normalization.

Use backslash escapes for ASCII punctuation only where normal Markdown parsing needs them. Entity references do not stand in for structural markers. Avoid invisible control characters such as U+0000; replace with U+FFFD when normalizing such input.

## Links, images, and emphasis

- Use `[label](destination)` or reference links without whitespace before the destination delimiter. Use meaningful labels. Inline links cannot contain nested links.
- Wrap destinations containing spaces in angle brackets or encode them appropriately. Balance or escape parentheses in unwrapped destinations. Resolve project-relative links and anchors against the actual file location.
- Reference labels are case-insensitive under Unicode case folding; the first definition wins. Avoid conflicting duplicate definitions.
- Use `![alternative text](source)` for informative images. Provide meaningful alt text; empty alt text is appropriate for purely decorative images when the renderer/accessibility context supports it.
- Use explicit Markdown links or `<https://example.com>` autolinks. Bare URLs are not CommonMark autolinks, even if an extended renderer recognizes them.
- Use * or ** for emphasis/strong emphasis; use asterisks for intraword emphasis rather than underscores. Put literal underscores inside code spans when appropriate.

## Renderer differences

Tables, task lists, strikethrough, and bare-URL autolinking are extensions rather than core CommonMark. Use them where the target renderer supports them, such as GitHub-flavored Markdown. Raw HTML rendering and sanitization vary by host; avoid relying on unsupported HTML for essential content.

Normal paragraph newlines are soft breaks, whose display can vary by renderer. Use a blank line for a new paragraph, or two trailing spaces/a backslash for an intentional hard break where appropriate. Avoid accidental trailing backslashes that force breaks across an entire document.

## Validate

Check heading hierarchy, block spacing, list indentation, fence balance, code-language labels, image alternatives, link destinations, and reference definitions. Use existing Markdown lint/build/link tooling when relevant, and inspect the actual renderer when layout matters. Distinguish a textual check from a rendered preview; do not claim links or rendering were tested when only their syntax was inspected.
