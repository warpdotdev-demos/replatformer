---
name: replatforming-observer
description: Run the replatform-site skill against one or more public websites, launch the generated apps, compare original and migrated sites with browser/computer vision, measure quality plus latency/tokens/credits, diagnose general replatforming failure patterns, and improve replatform-site through evidence-backed differential iterations. Use whenever the user asks to observe, benchmark, evaluate, visually compare, tune, self-improve, or run an outer loop on the replatforming skill.
compatibility: Requires shell access plus child agents with browser/computer-use capability for visual comparisons. Token and credit metrics depend on runtime telemetry availability.
---

# replatforming-observer

Improve `replatform-site` by executing it, observing its outputs, and keeping only changes that improve a controlled benchmark.

## Inputs and defaults

Accept:

- **Sites**: one or more public source URLs. Required.
- **Inner skill**: default `../replatform-site/SKILL.md`.
- **Framework/host**: pass through to the inner skill; use its defaults when omitted.
- **Viewports**: default desktop `1440x900` and mobile `390x844`.
- **Maximum DIF iterations**: default 3.
- **DIF mode**: default `apply`; alternatives are `propose-only` and `validate-candidate`.
- **Workspace**: default `./.replatforming-observer/runs/<UTC timestamp>/`.

Do not deploy generated sites. Do not test authenticated or private sites without explicit authorization.

## Operating principles

- Evaluate migrations, not redesigns. Visual similarity to the source is the primary quality goal.
- Compare like with like: use the same sites, model/harness, framework, viewports, routes, browser state, and cache policy for baseline and candidate.
- Isolate site runs so generated projects, ports, and dependencies cannot collide.
- Preserve evidence. A conclusion without screenshots, metrics, or exact reproduction details is only a hypothesis.
- Improve the inner skill, not the generated example sites. Use example-site edits only to prove a diagnosis, then translate the lesson into a general inner-skill change.
- Keep the inner skill lean. A quality improvement that substantially increases latency or token/credit cost needs clear justification.
- Every completed observation produces a DIF outcome artifact. A generalizable finding produces a concrete diff; a no-change outcome records why no diff is warranted.

Read [references/artifact-schema.md](references/artifact-schema.md) before creating run artifacts. Read [references/failure-taxonomy.md](references/failure-taxonomy.md) before categorizing mismatches.

## Workflow

### 1. Create a controlled benchmark

1. Resolve all inputs and state them briefly.
2. Create the workspace and an immutable snapshot of the inner skill directory.
3. Record:
   - Git commit and working-tree diff for the inner skill.
   - SHA-256 digest of every inner-skill file.
   - Chosen model, harness, framework, host, viewports, and cache policy.
   - Source URLs and selected representative routes.
4. Select routes:
   - Always include the home page.
   - Include up to three routes representing distinct templates or dynamic features.
   - For a one-page site, compare meaningful sections and interactions instead.

### 2. Run the baseline in isolated child agents

Run one child agent per site in a single batch with computer use enabled. Remote execution is preferred because each child needs an isolated browser, app server, filesystem, and ports.

Give every child:

- The exact source URL, routes, viewports, and output artifact schema.
- The full current inner-skill content or a durable snapshot it can access. Do not assume remote children can see uncommitted local files.
- An isolated workspace and unique ports.
- Instructions to invoke the inner skill, build the result, start its preview server, and compare original versus generated pages.
- Instructions to return a concise result and preserve screenshot/browser artifacts in the run.

Capture lifecycle timing/token telemetry as soon as it is surfaced. If total tokens or credits are unavailable, record `null` plus `metrics_unavailable_reason`; never estimate them.

### 3. Compare original and generated sites

For every selected route and viewport:

1. Load the original site in a clean browser state.
2. Wait for fonts, images, and layout to settle; dismiss only non-content overlays such as cookie banners.
3. Capture a full-page screenshot and a viewport screenshot.
4. Load the generated site at the equivalent route under the same conditions and capture the same screenshots.
5. Use computer vision to compare:
   - Overall composition, section order, spacing, typography, colors, and responsive behavior.
   - Images, crops, icons, backgrounds, and fonts.
   - Header, navigation, footer, forms, dropdowns, carousels, and other visible interactions.
   - Content, route coverage, metadata, and provider-CDN independence.
6. Exercise key interactions on both sites and record behavioral mismatches.
7. Assign a visual score from 0 to 100 and record specific mismatch evidence.

Keep screenshots paired and named predictably:

`<site>/<phase>/<route-slug>/<viewport>/<original|generated>-<full|viewport>.png`

### 4. Measure efficiency and latency

Record these separately so quality and cost tradeoffs remain visible:

- Total inner-loop wall-clock duration.
- Phase durations: inventory, scaffold/convert, dependency install, build, preview startup, and comparison.
- Inner-loop total tokens and credits when runtime telemetry exposes them.
- Build duration, route count, asset count, and generated project size.
- Failed commands, retries, repeated file reads/scrapes, and avoidable work observed in the transcript.

Use `scripts/aggregate_metrics.py` to aggregate completed `run.json` files. Compare means only when both phases have equivalent metric coverage; report coverage beside every aggregate.

### 5. Diagnose general failure categories

Categorize every mismatch using the taxonomy. Then distinguish:

- **Example-specific issue**: caused by unusual source content; do not immediately change the inner skill.
- **Provider/framework pattern**: likely to recur for that provider or target; update the relevant reference.
- **General workflow failure**: likely to affect many migrations; update the main skill or bundle a reusable script.
- **Efficiency failure**: repeated work, noisy reads, avoidable scaffolding, retries, or unnecessary dependencies.

Require the same category on at least two pages or two sites before treating it as general, unless it is a blocker such as a failed build, blank page, or missing primary navigation.

### 6. Apply DIF to the inner skill

DIF means **Differential Improvement Flow**:

1. **Diagnose**: state the evidence-backed failure pattern and root-cause hypothesis.
2. **Implement the smallest general diff**: update `replatform-site` instructions, references, or a reusable bundled script. Avoid fixes tied to a source URL, copied asset name, or one generated project.
3. **Follow through**: rerun the identical benchmark and decide whether to keep or revert the diff.

Before editing, write a DIF record containing:

- Evidence and affected failure categories.
- Files to change and why the change should generalize.
- Expected quality and efficiency impact.
- Regression risks and explicit keep/revert gates.

Inspect the actual diff after editing. Prefer one hypothesis per DIF iteration so cause and effect remain attributable.
Every completed baseline or candidate run must write one DIF outcome record under `dif/`, even when no improvement is warranted:

- When evidence supports a generalizable improvement, create the smallest concrete unified diff against the frozen inner-skill snapshot and record its path.
- In `apply` mode, apply that diff to the working inner skill, inspect it, and continue to candidate validation.
- In `propose-only` mode, preserve the concrete diff in the isolated run workspace without applying it to the shared inner skill. This mode is required when multiple observer agents run in parallel so they cannot race on shared skill files.
- When residual issues are example-specific, already covered, or unsupported by sufficient evidence, write a `no-change` DIF outcome with the evidence and reason instead of inventing a patch.

Do not finish a completed run with only prose describing a possible improvement. The DIF outcome record and either its concrete patch or explicit no-change reason are required handoff artifacts.

### 7. Rerun and gate the candidate

Run the same sites again with the candidate inner skill. Keep the diff only when:

- Every generated project still builds and previews.
- No blocker regression appears.
- Aggregate visual quality improves or a documented correctness blocker is removed.
- Route/asset/provider-independence checks do not regress.
- Tokens, credits, or latency do not regress by more than 15% without a justified quality gain.

Revert the inner-skill diff when gates fail. Apply the stop criteria in section 8 before running another DIF.

In `validate-candidate` mode, compare the supplied candidate inner-skill snapshot against the supplied baseline snapshot, apply the same gates, and report the decision without editing either snapshot.

### 8. Stop criteria and convergence detection

Do not run DIF iterations to the hard cap by default. Stop early and tell the user the skill appears to be in an optimal state as soon as the evidence supports it. Treat any one of the following as a stop signal, and treat two or more as a strong signal:

- **Diminishing diffs**: across two or more consecutive kept DIFs, the diffs shrink to cosmetic or example-specific edits—fewer general failure categories touched, fewer files, fewer lines—and no longer move the quality needle.
- **Quality plateau**: aggregate visual quality fails to improve by more than 2 points across two or more consecutive iterations despite distinct hypotheses, and no new blocker category appears.
- **Repeated pattern**: the same failure category or the same fix shape recurs across iterations without net improvement, which means the skill has already captured that lesson and further iteration is redundant.
- **No generalizable failures remain**: every residual mismatch is example-specific or already covered by an existing reference or inner-skill instruction.
- **Cost floor reached**: latency, tokens, and credits are stable or improving while quality plateaus, so no quality/cost tradeoff remains to exploit.

Also stop when a candidate passes all gates, the maximum iteration count is reached, or no generalizable improvement remains.

Track the DIF history needed to evaluate these signals: per iteration, record the diff scope (files and lines changed), the failure categories it targeted, whether it was kept or reverted, and the resulting aggregate visual score. Keep this in the run artifacts so convergence is auditable, not asserted.

When a stop signal fires:
- Stop iterating and do not open a new DIF.
- Report the skill as appearing to be in an optimal or plateaued state, not as a failure or an incomplete run.
- Summarize the convergence evidence: the sequence of diffs, the quality trend, which signal fired, and the residual mismatches that remain.
- Recommend the user treat the skill as stable. If the user wants further progress, propose expanding the eval or site set, targeting a different provider/framework frontier, or running a cross-critique pass instead of more DIF loops.

### 9. Report

Provide:

- Baseline versus candidate quality, latency, tokens, credits, and metric coverage.
- Per-site and per-category mismatch summary with evidence paths.
- The DIF hypothesis and exact inner-skill files changed.
- Paths to every DIF outcome record and proposed/applied patch, or the explicit no-change reason.
- Kept/reverted decision and regression-gate results.
- Convergence status: which stop signal fired, the DIF history it relied on, and whether the skill appears to be in an optimal/plateaued state.
- Remaining mismatches and the highest-value next experiment.

Do not claim improvement when telemetry or comparison evidence is missing. Clearly separate measured results from hypotheses.

## Efficiency guidance

- Fan out independent sites in one child-agent batch and fan in once for diagnosis.
- Reuse the source inventory and route set within an iteration; do not rediscover them for every comparison.
- Batch file reads and deterministic checks.
- Avoid re-scaffolding when testing a diagnosis that can be isolated first, but always perform a clean end-to-end rerun before keeping a DIF.
- Bundle deterministic helpers when multiple runs independently recreate the same script.

## Related resources

- [references/artifact-schema.md](references/artifact-schema.md) — required workspace and `run.json` format.
- [references/failure-taxonomy.md](references/failure-taxonomy.md) — stable categories and severity rules.
- `scripts/aggregate_metrics.py` — validate and aggregate run metrics.
- `evals/evals.json` — representative prompts for evaluating this skill.
