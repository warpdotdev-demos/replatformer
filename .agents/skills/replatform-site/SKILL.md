---
name: replatform-site
description: Re-platform a website off a hosted provider (Squarespace, Webflow, Wix, WordPress, Shopify, etc.) into static, source-controlled code in a modern JavaScript framework that deploys to a static host like Vercel, Netlify, or Cloudflare Pages. Use when the user wants to migrate a hosted site to static code, move a site off Squarespace/Webflow/Wix/WordPress/Shopify, or asks to "replatform" a website.
---

# replatform-site

Re-platform a hosted website into static, deployable code — one shot, end to end.

## Overview

Given a source site URL and (optionally) a destination framework + static host, this skill produces a deploy-ready static site project in the current directory. It gathers content from the source provider (preferring that provider's MCP/API when one is available, falling back to scraping the live site), scaffolds a project in a modern JS framework, converts pages/assets/navigation, re-points dynamic features to static-friendly equivalents, generates the host's deploy config, and verifies the build locally.

The skill is designed to run **one shot**: after the user supplies the source site and (optionally) the target platform, it proceeds end to end using the defaults below and does not stop to ask further questions. Only halt for user input if a decision is genuinely blocking and has no sensible default (rare).

## Inputs

The user supplies, in any form:

- **Source site** (required): the hosted site URL to migrate, and the provider if known (e.g. "my Squarespace site at https://...").
- **Destination framework** (optional, default: Next.js App Router with static export). Alternative: Astro.
- **Static host** (optional, default: Vercel). Alternatives: Netlify, Cloudflare Pages.
- **Output directory** (optional, default: `./<site-name>`).

Parse these from the user's message. For anything unspecified, apply the default and note it in the final summary. Do not prompt for optional inputs.

## Workflow

### 1. Confirm inputs and defaults

State the resolved plan up front (source, provider, framework, host, output dir) in one short line, then proceed. This is informational, not a prompt — keep going.

### 2. Gather source content

Prefer the provider's own data over scraping, since provider data is structured and authoritative. In order:

1. **Provider MCP/API**: if the provider has an MCP server or a documented API the agent can call (see [references/providers.md](references/providers.md)), use it to pull pages, products, posts, assets, navigation, and metadata. This is the highest-fidelity path.
2. **Live scrape fallback**: if no MCP/API is available or credentials aren't configured, scrape the live site. Fetch every internal page, download referenced assets (images, fonts, CSS, JS), and capture metadata. Treat the rendered DOM as the source of truth.

Capture a manifest of: pages (URL → title → route path), assets (URL → local path), nav structure, and any forms/search/dynamic features that need re-pointing.
Also capture provider-runtime presentation behavior that affects visible parity: generated selector or node-ID layout rules, responsive navigation, dropdowns, scroll effects, entry animations, and other interactions that disappear when provider JavaScript is removed.

### 3. Inventory and map the site

Build a content inventory:

- Page tree and URL → route mapping (e.g. `/about` → `app/about/page.tsx` for Next.js, `src/pages/about.astro` for Astro).
- Asset inventory with local filenames.
- Navigation (header, footer, menus).
- SEO metadata (titles, descriptions, Open Graph, sitemap, robots).
- Dynamic features to re-point (forms, search, ecommerce cart, comments).
- Provider-runtime behavior to reproduce (responsive menus, dropdowns, generated grid placement, animations, and scroll effects).

### 4. Scaffold the destination project

Scaffold the chosen framework in the output directory. See [references/frameworks.md](references/frameworks.md) for exact commands and config per framework/host combination. Defaults:

- **Next.js** (App Router) with `output: 'export'` for static export.
- **Vercel** as the deploy target (works with zero config for Next.js; add `vercel.json` only if non-default settings are needed).

Preserve the source site's visual identity (colors, type, layout) where discernible; otherwise keep framework defaults clean.

### 5. Convert content and assets

- Create one route/page per source page, preserving URL structure.
- Localize all assets into the repo (copy downloaded files under `public/` or the framework's asset dir). Never leave `<img src="https://...hosted...">` pointing back at the provider's CDN.
- Rebuild navigation from the inventory.
- Preserve SEO metadata, sitemap, and robots.
- Translate provider-generated layout rules that materially affect parity into explicit component styles. Do not assume semantic class names contain all grid placement, breakpoint, or visibility behavior.

### 6. Re-point dynamic features

Replace provider-hosted dynamic features with static-friendly equivalents using the defaults in [references/providers.md](references/providers.md):

- **Forms** → host-native forms (Vercel/Netlify) or Formspree.
- **Search** → Pagefind (client-side) unless the site is large enough to warrant an external search API.
- **Ecommerce** → keep product/collection pages static from exported data; route cart/checkout to the provider's Storefront/buy-button or a headless commerce provider. Do not attempt to rebuild a full cart in the static site.
- **Visible provider-runtime interactions** → reproduce them with accessible framework-native components. Do not copy provider JavaScript bundles into the generated site.

### 7. Generate deploy config

- Add the host's config file only if needed (e.g. `vercel.json`, `netlify.toml`, Cloudflare Pages settings). For Vercel + Next.js, default config is usually sufficient — don't add an empty `vercel.json`.
- Add a build command and output directory matching the framework.
- Add redirects for any old paths that changed, using the host's redirect format, to protect SEO.

### 8. Verify locally

Run the framework's build and serve the output, then sanity-check:

- Build succeeds with no errors.
- Home page and 2-3 key pages render with content and assets.
- No remaining hard references to the source provider's CDN.
- Navigation and redirects work.
- Responsive navigation, dropdowns, and primary visible animations/interactions match the source closely enough to preserve behavior.

Do not deploy for the user. Report the local preview URL and the exact deploy command(s) for their chosen host.

### 9. Hand off

Produce a short summary:

- What was migrated (page count, asset count).
- Defaults applied (framework, host).
- Dynamic features re-pointed and how.
- Any caveats (pages that couldn't be fully captured, features needing manual setup such as commerce checkout).
- The one or two commands to deploy (e.g. `vercel`).

## Best practices

- **One shot**: rely on defaults; don't ask. Only halt if a truly blocking decision has no default.
- **Provider data first**: structured provider data beats scraping. Always try MCP/API before scraping.
- **Localize everything**: never depend on the source provider's CDN after migration.
- **Preserve URLs**: keep route structure; add redirects for changes to protect SEO.
- **Migration, not redesign**: match the source site; don't "improve" it unless the user asked for changes.
- **Be token-efficient**: this skill is also a demonstration of an outer-loop improvement process that scores runs on correctness and token efficiency. Prefer batched operations, avoid re-reading large files, and reuse the content manifest rather than re-scraping.

## Related

- [references/providers.md](references/providers.md) — per-provider content gathering (MCP/API/scraping) and dynamic-feature re-pointing.
- [references/frameworks.md](references/frameworks.md) — destination framework scaffolding and per-host deploy config.
