---
name: oz-orchestrated-replatforming
description: Drive parallel replatforming observations across many public websites using Oz cloud agents. Fan out one computer-use-capable cloud agent per site with replatforming-observer, gather and validate results, aggregate cross-site visual/behavioral/efficiency findings, and optionally coordinate one centralized replatform-site improvement plus parallel verification. Use whenever the user asks to run replatforming observations in parallel, benchmark many sites with Oz, orchestrate the observer skill, or gather cloud-agent migration results.
compatibility: Requires Oz cloud-agent orchestration with computer use. First-run automatic environment creation uses the authenticated Oz CLI. Cloud runs consume Warp credits; token and credit telemetry availability depends on the runtime.
---

# oz-orchestrated-replatforming

Use Oz cloud agents as the execution layer for parallel, isolated replatforming observations.

## Inputs and defaults

Accept:

- **Sites**: one or more public source URLs. Required.
- **Mode**: default `observe-only`; optional `improve-and-verify`.
- **Observer skill**: default `../replatforming-observer/SKILL.md`.
- **Inner skill**: default `../replatform-site/SKILL.md`.
- **Framework/host/viewports**: pass through to the observer; use observer defaults when omitted.
- **Environment**: default `auto`; reuse or create the simple `replatforming-web-default` Oz environment.
- **Environment scope**: default `personal`; use `team` only when the user requests a shared environment.
- **Maximum parallel sites**: default 8.
- **Workspace**: default `./.replatforming-observer/orchestrated/<UTC timestamp>/`.

Do not deploy generated sites. Do not commit, push, or open pull requests. Do not run authenticated/private sites without explicit authorization.

Read [references/default-environment.md](references/default-environment.md) before resolving the cloud environment. Read [references/result-schema.md](references/result-schema.md) before launching agents. Read the observer skill and its references before constructing child prompts.

## Why this driver exists

Independent sites are ideal Oz cloud-agent shards: each needs its own browser, preview server, dependencies, ports, and computer-use session. Parallel observation shortens wall-clock time and reveals recurring migration failures across providers.

Parallel agents must not edit the shared inner skill. Baseline agents run the observer in `propose-only` mode; the parent gathers proposals and owns any centralized DIF.

## Workflow

### 1. Resolve and freeze the run

1. Resolve sites, mode, framework, host, viewports, and output workspace.
2. Refuse duplicate URLs and normalize trailing slashes.
3. Cap the first batch at the requested/default maximum instead of silently creating many credit-consuming runs.
4. Snapshot and hash the complete observer and inner-skill directories.
5. Record the Git commit and local diffs affecting either skill.
6. Create `orchestration.json` using the result schema.
7. State the proposed cloud batch: site count, one agent per site, computer use enabled, whether a second validation phase may run, and that first-time setup may add one lightweight environment smoke run.
8. For explicit orchestration requests, wait for user approval before launching the batch.

Cloud agents consume Warp credits. Never multiply runs beyond one baseline agent per site without stating the additional phase and receiving the required approval.

### 2. Ensure a reusable web-build environment

Resolve the environment before presenting or launching the cloud batch:

1. If the user supplied an environment ID, inspect it and use it when it provides a working web toolchain.
2. Otherwise, discover an exact-name `replatforming-web-default` environment and verify its image and setup contract.
3. If no suitable environment exists, create it automatically with explicit personal/team scope using [references/default-environment.md](references/default-environment.md).
4. For a newly created or changed environment, launch one separate lightweight Oz smoke agent without computer use. It must verify `node`, `npm`, `npx`, `vercel`, and `serve`, then exit without modifying files.
5. Capture the environment ID, image, setup commands, creation/reuse decision, smoke-run ID, and verification result in `orchestration.json`.
6. Launch the main site batch only after the smoke run succeeds, then use the resolved environment ID for every child.

Environment creation is persistent Oz configuration and is appropriate here because this driver promises a repeatable first-run experience. State what will be created before doing it. If the CLI is unauthenticated or the account cannot create environments, stop and ask only for the required login/permission action; do not fall back to an unverified empty environment.

The default environment intentionally has no attached repository. Generated sites are ephemeral, public-site observations, and current skill snapshots are passed directly to the agents. This lets a new Oz user run the driver without configuring GitHub access first. The one-time smoke run is a separate batch because it does not need computer use; do not launch the credit-heavier browser batch when environment setup fails.

### 3. Construct one shared Oz batch

Use the orchestration agent's cloud-child mechanism rather than shelling out to the Oz CLI. Use the CLI/API only when the user explicitly requests it, needs scheduling, or needs programmatic automation outside an interactive run.

Launch all site agents in one batch because they share the same run-wide configuration:

- Remote Oz execution.
- Computer use enabled.
- One stable child name per site: `observe-<site-slug>`.
- Same model, harness, environment strategy, framework, host, viewports, and cache policy.
- Omit model/harness overrides unless the user requested them.
- Set the remote environment ID to the verified environment resolved in the previous step.

The user reviews the batch before launch. Treat the resolved launch settings as authoritative.

### 4. Give every child a strict task

Put shared instructions in the batch base prompt and site-specific details in each child prompt. Every prompt must include:

- The source URL and resolved absolute workspace path inside the child environment.
- The exact observer and inner-skill snapshots, or durable skill references that the child can access.
- `DIF mode: propose-only`.
- Instructions to create an isolated generated project, build it, run its preview server, and compare original/generated sites with computer use.
- Instructions not to edit the inner skill, deploy, commit, push, or open a PR.
- The exact result schema and requirement to finish with one machine-readable `site-result.json` object.
- Requirement to record unavailable tokens/credits as `null` with a reason rather than estimating them.
- Requirement to preserve screenshot and browser artifacts in the Oz run and cite them in the result.

Remote children cannot see unsynced local files. If skill snapshots are not committed and available in the environment, include their exact content in the shared prompt rather than referencing local paths.

### 5. Monitor without polling

Track every trusted child agent ID returned by the launch.

- Capture lifecycle status, duration, tokens, and credit metadata when surfaced.
- Read pushed child messages as they arrive; do not poll.
- If a child is blocked or fails, inspect the reason. Resume the same child with focused guidance when possible instead of launching a replacement.
- When no other work is possible, wait for agent events.
- Treat a succeeded child as idle and still addressable for later candidate validation.

Write each completed result immediately to `<workspace>/sites/<site-slug>/baseline/site-result.json`.

### 6. Fan in and validate results

Validate each result against [references/result-schema.md](references/result-schema.md) with `scripts/validate_results.py`. Mark malformed or incomplete results as invalid rather than filling in missing evidence.

Aggregate:

- Completion/failure/blocked counts.
- Visual score and mismatch categories.
- Build, preview, route, asset, interaction, and provider-independence outcomes.
- Inner-loop duration/tokens/credits and Oz-run duration/tokens/credits, keeping these layers separate.
- Telemetry coverage and unavailable reasons.
- DIF proposals clustered by failure category and proposed target files.

Use the observer's `scripts/aggregate_metrics.py` for valid observer `run.json` artifacts. Only label a pattern cross-site when it appears on at least two sites, unless it is a correctness blocker.

### 7. Finish observe-only mode

In `observe-only` mode, do not modify `replatform-site`. Produce the gathered report with:

- Per-site outcomes and Oz run identifiers.
- Cross-site mismatch clusters and evidence.
- Quality/latency/token/credit aggregates with coverage.
- Ranked centralized DIF proposals.
- Failed or incomplete sites and recommended retry actions.

### 8. Optionally improve and verify centrally

In `improve-and-verify` mode:

1. Select one cross-site proposal with the strongest evidence and broadest likely impact.
2. Write a centralized DIF record.
3. Apply the smallest general diff to the local inner skill. The parent is the only writer.
4. Inspect the diff and compute the candidate skill digest.
5. Send a follow-up message to the same completed child agents with:
   - The exact candidate snapshot.
   - `DIF mode: validate-candidate`.
   - The original frozen benchmark configuration.
   - Instructions to rerun the equivalent candidate observation and return the same schema.
6. Gather candidate results in parallel and apply observer regression gates.
7. Keep the centralized diff only if aggregate quality/correctness improves without unjustified cost regression; otherwise revert it.

Reusing the same child agents preserves their site-specific context and avoids spending tokens rediscovering the source.

### 9. Report and hand off

Report:

- Oz batch configuration and counts.
- Per-site status, evidence, and run identifiers.
- Aggregate correctness, visual, latency, token, and credit metrics with coverage.
- Cross-site failure categories.
- Centralized DIF decision when applicable.
- Paths to `orchestration.json`, site results, observer artifacts, and aggregate reports.
- Recommended next batch or highest-value follow-up.

Clearly separate inner observer metrics from outer Oz cloud-run metrics. Do not claim cost improvements when credit/token telemetry is unavailable.

## Efficiency and safety

- One cloud child per site; never one child per page.
- Compare multiple routes inside the site's existing child.
- One shared batch for equivalent run-wide settings.
- Reuse the same children for candidate validation.
- Use strict JSON handoff so the parent does not reread noisy transcripts.
- Keep provider credentials and secrets out of prompts and result artifacts.
- Do not let parallel agents independently patch `replatform-site`.

## Related resources

- [references/result-schema.md](references/result-schema.md) — orchestration and child-result contract.
- [references/default-environment.md](references/default-environment.md) — first-run web/Vercel environment bootstrap.
- `scripts/validate_results.py` — deterministic child-result validation and status summary.
- `evals/evals.json` — representative driver scenarios.
- `../replatforming-observer/SKILL.md` — per-site observation and DIF logic.
- `../replatforming-observer/scripts/aggregate_metrics.py` — observer metric validation and aggregation.
