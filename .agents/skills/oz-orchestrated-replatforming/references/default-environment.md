# Default Oz web-build environment

Use this contract when the driver receives no explicit environment ID.

## Desired configuration

- **Name**: `replatforming-web-default`
- **Description**: `Reusable Oz environment for parallel static-site replatforming observations`
- **Scope**: personal by default; team only when requested
- **Docker image**: `node:22-bookworm`
- **Repositories**: none
- **Setup commands**, in order:
  1. `corepack enable`
  2. `npm install -g vercel@54 serve@14`
  3. `node --version && npm --version && vercel --version && serve --version`

The official Node Bookworm image is glibc-compatible, documented as a supported Oz environment base, and supplies the required Node/npm toolchain. The setup commands make local Vercel builds and static export previews explicit. Computer-use browser support is provided by the Oz run, not by these setup commands.

## Discovery and creation

1. Detect the available authenticated CLI, preferring `oz` and falling back to `oz-dev`.
2. List environments with JSON output and look for an exact-name match.
3. Inspect an exact-name match with JSON output before reuse. It is suitable only when it uses the desired image and contains the required setup commands.
4. If the name exists with an incompatible contract, preserve it and create a versioned name such as `replatforming-web-default-v2`.
5. If no suitable environment exists, state the name, image, and setup commands, then create it.

Command equivalents:
Use `oz environment list --output-format json` for discovery and `oz environment get <ENV_ID> --output-format json` for inspection. Substitute `oz-dev` when that is the installed CLI.

The equivalent CLI operation is:

```sh
oz environment create \
  --name "replatforming-web-default" \
  --personal \
  --docker-image "node:22-bookworm" \
  --setup-command "corepack enable" \
  --setup-command "npm install -g vercel@54 serve@14" \
  --setup-command "node --version && npm --version && vercel --version && serve --version" \
  --description "Reusable Oz environment for parallel static-site replatforming observations" \
  --output-format json
```

Use `oz-dev` in place of `oz` when that is the installed CLI. Request JSON output when supported so the environment ID can be captured without parsing prose.

Use `--team` instead of `--personal` only when the user requested a shared team environment.

## Verification and failure handling

- Inspect the created/reused environment and record its ID, image, and setup commands.
- For a newly created or changed environment, run one no-computer-use smoke cloud agent before the main batch. It must run `node --version`, `npm --version`, `npx --version`, `vercel --version`, and `serve --version`, returning the exact versions.
- Treat smoke-run or environment setup failure as a batch blocker; do not launch site agents against a broken environment.
- If the CLI is unauthenticated, ask the user to run `oz login` as the single blocking action. If the CLI is missing or lacks environment-creation permission, ask only for the corresponding installation or permission action.
- Do not attach repositories or request GitHub authorization for the default environment.
- Do not store credentials in setup commands. Use Oz secrets only when a future provider-specific observer requires credentials.

## Why not use an empty environment

Cloud-agent environments provide repeatability. Falling back to an empty or unverified environment would make first-run behavior depend on incidental packages and would undermine cross-site latency and quality comparisons.
