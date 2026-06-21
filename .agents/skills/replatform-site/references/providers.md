# Provider reference

Per-provider guidance for gathering source content and re-pointing dynamic features during a re-platform. Use alongside the main workflow in [../SKILL.md](../SKILL.md).

## General approach

For each provider, try in order:

1. **MCP server** — if an MCP server exists for the provider and is configured in the agent's environment, prefer it. It gives structured, authoritative data.
2. **Official API** — if no MCP but a documented REST/GraphQL API exists, call it directly. Credentials may be needed; if they aren't configured, fall back to scraping rather than prompting.
3. **Live scrape** — fetch the rendered site. Always available. Lower fidelity for structured data (products, posts) but fine for content + assets.

If credentials are required and not present, fall back to scraping and note the reduced fidelity in the final summary. Do not block on credential prompts — the skill runs one shot.

## Squarespace

- No official public MCP. Has a Commerce API (products, orders) requiring an API key.
- Scrape: Squarespace sites render server-side; fetch HTML per page, download assets under the `squarespace-cdn` and `static1.squarespace.com` domains.
- Dynamic features: forms → Squarespace forms are email-based; replace with host-native forms. Commerce → use the Commerce API to export products, render them statically, route checkout to Squarespace's external checkout link or a headless provider.

## Webflow

- Webflow has a REST API (sites, collections, pages, assets) requiring a token. No first-party MCP at time of writing.
- If a token is available, pull collections (CMS items) and pages via the API — highest-fidelity path for Webflow CMS sites.
- Else scrape: Webflow outputs static HTML already, so scraping yields clean markup. Download assets from `assets.website-files.com`.
- Dynamic features: CMS → render collection items as static pages. Forms → Webflow forms post to Webflow; replace with host-native forms or Formspree.
- Before conversion, inventory Webflow-specific presentation dependencies:
  - Extract material `w-node-*` grid placement, breakpoint, ordering, and visibility rules from Webflow stylesheets. Translate them into explicit generated component styles instead of preserving opaque node IDs.
  - Identify `w-nav` and `w-dropdown` components and record their desktop, mobile, hover, focus, and click behavior. Rebuild them as accessible framework-native components with equivalent responsive breakpoints.
  - Identify `data-w-id`, IX2, and parallax/scroll-effect behavior. Preserve primary visible motion with a small framework-native implementation; omit only decorative motion that does not materially affect parity.
- Do not rely on generic Webflow class names alone. They often omit node-ID layout overrides and runtime JavaScript behavior, producing broken grids, uncollapsed mobile navigation, or inert interactions.
- Do not ship Webflow runtime bundles as the migration solution. Reproduce the observed behavior in source-controlled components and verify it at every requested viewport.

## Wix

- No first-party MCP. Wix has a Headless API and the Velo platform for site owners with dev mode.
- Most Wix sites are best scraped; the rendered DOM is the practical source. Download assets and inline styles.
- Dynamic features: Wix forms → host-native forms. Stores → Wix Headless Stores API if available, else list products statically and link out to Wix checkout.

## WordPress

- No first-party MCP. The WordPress REST API (`/wp-json/wp/v2/`) is available on most self-hosted and WordPress.com sites and is the best structured source: posts, pages, media, menus, taxonomies.
- Pull pages and posts via `/wp-json/wp/v2/pages` and `/posts`; media via `/media`; menus may require the menus endpoint or scraping.
- Dynamic features: comments → Disqus or a static comment provider. Forms (Contact Form 7, etc.) → host-native forms. WooCommerce → use the WooCommerce REST API to export products, render statically, route checkout to a headless Woo or external provider.

## Shopify

- No first-party MCP. The Shopify Admin API (REST/GraphQL) requires a store access token and is the highest-fidelity path for products, collections, pages, blogs, and navigation.
- If a token is available, pull products, collections, pages, and blogs via GraphQL.
- Else scrape the storefront (note: Shopify storefronts are heavily JS-rendered; rendered DOM scraping or Liquid output is needed).
- Dynamic features: this is the hardest provider to fully re-platform because the cart and checkout are server-side. Default approach: render product and collection pages statically from exported data; keep the cart/checkout on Shopify via the Storefront API or buy-button SDK, or migrate to Shopify Headless / a headless commerce provider. Flag this as a caveat in the summary rather than attempting a full cart rebuild.

## Dynamic feature defaults (all providers)

- **Contact forms** → host-native forms (Vercel/Netlify) or Formspree.
- **Search** → Pagefind (client-side) for small/medium sites.
- **Comments** → Disqus or a static comment provider.
- **Ecommerce cart/checkout** → keep on provider (Shopify Storefront/buy-button) or migrate to headless commerce.
- **Blog** → render posts as static pages from provider API/scrape.

Only deviate from these defaults if the user specified something else in their initial message.
