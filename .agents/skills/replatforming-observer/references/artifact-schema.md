# Observer artifact schema

Use one `run.json` per site execution. Keep baseline and candidate runs separate.

## Workspace

```text
.replatforming-observer/runs/<run-id>/
├── benchmark-config.json
├── skill-baseline/
├── dif/
│   ├── iteration-<n>.json
│   └── iteration-<n>.patch
├── baseline/<site-slug>/run.json
├── candidate-<n>/<site-slug>/run.json
├── screenshots/<site-slug>/<phase>/<route>/<viewport>/
└── benchmark.json
```

## run.json

Required fields:

```json
{
  "schema_version": 1,
  "run_id": "2026-06-20T23-30-00Z-talkingslop-baseline",
  "phase": "baseline",
  "iteration": 0,
  "site": "https://talkingslop.ai/",
  "inner_skill_digest": "sha256:...",
  "status": "passed",
  "metrics": {
    "duration_ms": 120000,
    "total_tokens": null,
    "credits": null,
    "visual_score": 82,
    "routes_compared": 1,
    "viewports_compared": 2,
    "build_passed": true,
    "provider_independent": true
  },
  "metrics_unavailable_reason": {
    "total_tokens": "runtime did not expose token telemetry",
    "credits": "runtime did not expose credit telemetry"
  },
  "phase_durations_ms": {
    "inventory": 10000,
    "conversion": 50000,
    "build": 20000,
    "comparison": 40000
  },
  "mismatches": [
    {
      "category": "typography",
      "severity": "major",
      "route": "/",
      "viewport": "1440x900",
      "evidence": "screenshots/.../original-full.png vs generated-full.png",
      "diagnosis": "Generated page omitted the source font."
    }
  ],
  "artifacts": {
    "generated_project": "outputs/talking-slop",
    "screenshots": "screenshots/talkingslop/baseline",
    "transcript": null
  }
}
```

Allowed `phase` values are `baseline` and `candidate`. Allowed `status` values are `passed`, `failed`, and `blocked`.

Metrics may be `null` only when the field is listed in `metrics_unavailable_reason`. Never estimate tokens or credits.

## DIF record

Each `dif/iteration-<n>.json` records:

- `hypothesis`
- `evidence`
- `categories`
- `target_files`
- `expected_quality_impact`
- `expected_efficiency_impact`
- `regression_risks`
- `keep_gates`
- `diff_path`
- `decision`: `proposed`, `kept`, `reverted`, `pending`, or `no-change`
- `decision_evidence`

Every completed baseline or candidate run requires one DIF outcome record. When `decision` is `proposed`, `kept`, `reverted`, or `pending`, `diff_path` must reference a concrete unified diff against the frozen inner-skill snapshot. When `decision` is `no-change`, `diff_path` must be `null` and `decision_evidence` must explain why the evidence did not warrant a general inner-skill change.
