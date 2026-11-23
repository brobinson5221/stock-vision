# HTML/CSS style and color guide

Adapted for Codex from [Awesome Copilot: HTML/CSS Style Color Guide](https://awesome-copilot.github.com/instruction/html-css-style-color-guide/). Apply when creating or modifying browser-rendered HTML/CSS styles and color choices, including component styles and utility classes.

## Respect the design context

Follow explicit user requirements and established brand/design specifications. Otherwise use the following palette defaults. These are aesthetic choices, not claims that a hue is inherently inaccessible or unprofessional. Preserve an existing design system rather than recoloring unrelated screens.

## Palette and balance

- Hot colors: oranges, reds, and yellows. Cool colors: blues, greens, and purples. Neutrals: grays and grayscale variations. Black and white form the source guide's binary category.
- Aim for a 60/30/10 balance: roughly 60% primary surfaces, 30% secondary surfaces, and 10% accents. Prefer cool/light primary and secondary surfaces and a restrained complementary warm accent where useful. Treat the proportions as a composition guide, not a pixel quota.
- Unless explicitly required by a user or design specification, avoid purple/magenta, pink, red, orange, yellow, and other hot background fills. Prefer white/off-white, light cool colors, or subtle neutrals. Preserve intentional dark themes with suitable dark neutral surfaces.
- Avoid bright purples/magentas, bright pinks, neon colors, and heavily saturated warm colors by default. Reserve red/orange/yellow for limited urgency, warnings, errors, or important accents. Pair semantic colors with text or icons.

## Text and accessibility

Use dark neutral text on light backgrounds, such as #1f2328 or #24292f, and near-white text on dark backgrounds. Avoid yellow or pink text under the default palette. Never use light text on a similarly light surface or dark text on a similarly dark surface.

Measure the actual foreground/background combinations, including opacity, gradients, hover/focus states, placeholders, and dark mode. For WCAG AA, normal text generally needs at least 4.5:1 contrast; large text needs 3:1. Relevant non-text controls, boundaries, and graphical information need 3:1 against adjacent colors where required. Do not infer compliance from a color name or a sample hex value.

Keep links, focus indicators, errors, selection, and interactive states distinguishable without relying on hue alone. Preserve keyboard focus and native/high-contrast behavior. An explicit brand request can change the palette defaults but does not remove accessibility requirements.

## Gradients and styling

Prefer restrained, same-family transitions such as #E6F2FF to #F5F7FA and linear gradients for backgrounds. Avoid mixing strongly contrasting hot and cool hues by default. Use gradients only where they improve the requested design: containers, headers/navigation, cards, buttons, or subtle depth effects. Verify text contrast across the entire gradient, not just one endpoint.

Reuse existing semantic color tokens and component states. Add only the tokens and styles needed for the task; avoid spreading hardcoded palette values or overriding unrelated components.

## Verify

Inspect affected pages at representative viewport sizes and supported themes when a preview is available. Check actual text/control contrast, keyboard focus, hover/disabled/error states, and any changed gradient backgrounds. Use existing accessibility tooling where practical and report visual or contrast checks that were not performed.
