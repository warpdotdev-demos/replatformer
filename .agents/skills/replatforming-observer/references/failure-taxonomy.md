# Replatforming failure taxonomy

Use stable categories so patterns can be aggregated across sites and iterations.

## Correctness categories

- `build-or-preview`: install, build, export, or preview failure.
- `route-coverage`: missing page, wrong URL, redirect, or broken navigation target.
- `content`: missing, duplicated, reordered, or incorrect text/content.
- `asset-localization`: missing asset or remaining dependency on the hosted provider CDN.
- `metadata-seo`: title, description, Open Graph, sitemap, robots, or canonical mismatch.
- `dynamic-feature`: form, search, commerce, comments, or other provider-backed feature mismatch.
- `interaction`: menu, dropdown, modal, carousel, link, keyboard, or focus behavior mismatch.

## Visual categories

- `layout`: section order, geometry, grid, alignment, width, or overflow.
- `responsive`: breakpoint-specific layout or visibility mismatch.
- `typography`: font family, weight, size, line height, or wrapping.
- `spacing`: margin, padding, gap, or density mismatch.
- `color-style`: color, border, shadow, radius, or decoration mismatch.
- `media`: missing/wrong image, crop, aspect ratio, video, icon, or background.
- `animation`: motion, transition, scroll effect, or timing mismatch.

## Efficiency categories

- `duplicate-discovery`: repeated crawling, scraping, or inventory work.
- `excessive-context`: unnecessarily broad file reads or noisy output.
- `avoidable-scaffold`: unnecessary dependencies, framework setup, or generated files.
- `retry-loop`: repeated failed command or tool attempt without a changed hypothesis.
- `non-reusable-fix`: solving an example directly instead of improving the inner skill.
- `telemetry-gap`: missing timing, token, credit, or phase data.

## Severity

- `blocker`: generated site cannot be built, previewed, navigated, or meaningfully compared.
- `major`: obvious visual/behavioral mismatch affecting a primary page or feature.
- `minor`: visible mismatch with limited user impact.
- `informational`: measurable difference or opportunity that does not materially affect parity.

Treat a mismatch as generalizable when it occurs on at least two pages or two sites, or when a blocker exposes a clear workflow defect.
