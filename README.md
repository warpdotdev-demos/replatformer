# Replatformer

A Warp agent skill that takes websites hosted on managed providers (e.g. Squarespace, Webflow, Wix, WordPress, Shopify) and migrates them into static, source-controlled code that can be deployed to a static-site host such as Vercel, Netlify, or Cloudflare Pages.

## Purpose

This skill has two goals:

1. **Demonstrate re-platforming** — show an end-to-end workflow that moves a hosted site into deployable static code.
2. **Demonstrate an outer-loop skill-improvement loop** — the skill itself is tuned by an automated outer loop that uses computer use to run the skill against example sites, evaluate the output for correctness and token efficiency, and feed the results back into the skill definition. The point is to show how a skill can be iteratively improved by executing it and measuring the results, rather than hand-tuning it once and leaving it static.

## What it does

Given a hosted website, the skill:

1. **Inventories** the source site — pages, assets, navigation, content, and metadata.
2. **Extracts** the content and structure into a static site framework (Next.js / Astro by default).
3. **Normalizes** assets (images, fonts, styles) into the repo so the site no longer depends on the host's CDN.
4. **Re-points** forms, search, and other dynamic features to serverless equivalents or third-party APIs.
5. **Generates** a deploy-ready project with the static host's config (e.g. `vercel.json`), so `vercel deploy` works out of the box.
6. **Verifies** the migrated site renders equivalently before cutover.

## Why

Hosted providers are convenient but lock you in: limited theming, per-seat pricing, and no access to the underlying code. Re-platforming to a static site gives you full source control, faster builds, cheaper hosting, and the ability to extend the site with code. Beyond the re-platforming workflow itself, this repo is also a demonstration of how to build a self-improving skill: the outer loop uses computer use to run the skill, score the output, and iterate on the skill definition until it is both more correct and more token efficient.

## Usage

This repo is an **example** of a re-platforming skill. Run it from Warp by pointing it at a hosted site URL and a destination framework:

```bash path=null start=null
# Example target
./replatform https://example-shop.myshopify.com --to next --deploy-target vercel
```

The skill walks through the steps above and leaves a deploy-ready project in the current directory.

## Project layout

```
replatformer/
├── README.md          # This file
├── SKILL.md           # Skill definition (added in a later commit)
└── src/               # Migration implementation (added in a later commit)
```

## License

This project is licensed under the [MIT License](./LICENSE).

## Status

Example / work-in-progress. The structure and README are initialized; the skill definition and migration logic will be added incrementally. This repo will be published as open source under the [`warpdotdev-demos`](https://github.com/warpdotdev-demos) GitHub organization.
