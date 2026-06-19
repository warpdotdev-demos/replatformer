# Framework & host reference

Scaffolding and deploy config for each supported destination. Use alongside the main workflow in [../SKILL.md](../SKILL.md).

## Frameworks

### Next.js (default)

- Scaffold: `npx create-next-app@latest <dir> --typescript --app --no-src-dir --import-alias "@/*"`
- Static export: set `output: 'export'` in `next.config.mjs`. For images, set `images: { unoptimized: true }` since the optimizer doesn't run in static export.
- Asset dir: `public/`.
- Build: `npm run build` → outputs to `out/`.
- Good default for Vercel; also works on Netlify and Cloudflare Pages.

### Astro

- Scaffold: `npm create astro@latest <dir> -- --template minimal --typescript strict --no-install --no-git`
- Static output is the default.
- Asset dir: `public/`; components in `src/components`; pages in `src/pages` (file-based routing).
- Build: `npm run build` → outputs to `dist/`.
- Prefer Astro when the site is mostly content (blog, marketing, docs) and you want minimal JS.

## Static hosts

### Vercel (default)

- Next.js works with zero config. Don't add an empty `vercel.json`.
- Astro: auto-detected. Add a `vercel.json` only to set non-default options.
- Deploy: `vercel` (preview) or `vercel --prod` (production).
- Redirects: `vercel.json` `redirects` array, or `next.config.mjs` `redirects()` for Next.js.

### Netlify

- Add `netlify.toml` with build command and publish dir:
  - Next.js: build `npm run build`, publish `out` (with `output: 'export'`). For full Next features, use the Netlify Next adapter instead of static export.
  - Astro: build `npm run build`, publish `dist`.
- Forms: use Netlify Forms (add `data-netlify="true"` to forms) — native, no backend.
- Deploy: `netlify deploy --prod`.

### Cloudflare Pages

- Build command and output dir set in the Pages dashboard or `wrangler.toml`:
  - Next.js: build `npm run build`, output `out`.
  - Astro: build `npm run build`, output `dist`.
- Functions: Cloudflare Workers/Functions for any dynamic pieces.
- Deploy: `npx wrangler pages deploy <out-dir>`.

## Choosing framework vs host

The defaults (Next.js + Vercel) cover the majority of marketing/site re-platforms. Switch to Astro if the site is content-heavy and you want the smallest output. Switch the host only if the user asked for it or needs a host-specific feature (e.g. Netlify Forms).
