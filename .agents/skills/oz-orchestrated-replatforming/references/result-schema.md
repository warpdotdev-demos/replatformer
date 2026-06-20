# Oz-orchestrated replatforming result schema

The parent writes one `orchestration.json` and one `site-result.json` per site/phase.

## Workspace

```text
.replatforming-observer/orchestrated/<run-id>/
├── orchestration.json
├── skill-snapshots/
├── sites/<site-slug>/baseline/site-result.json
├── sites/<site-slug>/candidate/site-result.json
├── dif/centralized-dif.json
└── aggregate-report.json
```

## orchestration.json

Required fields:

```json
{
  "schema_version": 1,
  "run_id": "2026-06-20T23-40-00Z",
  "mode": "observe-only",
  "sites": ["https://example.com/"],
  "observer_skill_digest": "sha256:...",
  "inner_skill_digest": "sha256:...",
  "framework": "next",
  "host": "vercel",
  "viewports": ["1440x900", "390x844"],
  "cloud_batch": {
    "computer_use_enabled": true,
    "agent_ids": {},
    "resolved_model": null,
    "resolved_harness": null,
    "resolved_environment": {
      "id": "environment ID",
      "name": "replatforming-web-default",
      "scope": "personal",
      "image": "node:22-bookworm",
      "decision": "created",
      "smoke_run_id": "trusted Oz child-agent ID",
      "verified": true
    }
  },
  "status": "pending"
}
```

Allowed `mode` values: `observe-only`, `improve-and-verify`.

Allowed `status` values: `pending`, `running`, `completed`, `partial`, `failed`.

Allowed environment `decision` values: `provided`, `reused`, `created`.

## site-result.json

Required fields:

```json
{
  "schema_version": 1,
  "site": "https://example.com/",
  "site_slug": "example-com",
  "phase": "baseline",
  "agent_id": "trusted Oz child-agent ID",
  "status": "passed",
  "oz_metrics": {
    "duration_ms": null,
    "total_tokens": null,
    "credits": null
  },
  "oz_metrics_unavailable_reason": {
    "duration_ms": "not surfaced by runtime",
    "total_tokens": "not surfaced by runtime",
    "credits": "not surfaced by runtime"
  },
  "observer_run": {
    "run_id": "observer run ID",
    "run_json": {},
    "dif_proposal": {
      "hypothesis": "General failure hypothesis",
      "categories": ["layout"],
      "target_files": ["references/providers.md"],
      "evidence": ["computer-use artifact reference"]
    }
  },
  "artifacts": {
    "computer_use": [],
    "screenshots": [],
    "generated_project": null
  }
}
```

Allowed `phase` values: `baseline`, `candidate`.

Allowed `status` values: `passed`, `failed`, `blocked`, `invalid`.

Every `null` Oz metric needs a matching unavailable reason. Preserve the observer's inner-loop metrics inside `observer_run.run_json`; do not merge them with `oz_metrics`.
