#!/usr/bin/env python3
"""Validate and aggregate replatforming observer run.json artifacts."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

METRICS = (
    "duration_ms",
    "total_tokens",
    "credits",
    "visual_score",
    "routes_compared",
    "viewports_compared",
)
REQUIRED = {
    "schema_version",
    "run_id",
    "phase",
    "iteration",
    "site",
    "inner_skill_digest",
    "status",
    "metrics",
    "mismatches",
    "artifacts",
}


def discover(paths: list[Path]) -> list[Path]:
    found: set[Path] = set()
    for path in paths:
        if path.is_dir():
            found.update(path.rglob("run.json"))
        elif path.name == "run.json":
            found.add(path)
    return sorted(found)


def load_run(path: Path) -> dict[str, Any]:
    run = json.loads(path.read_text())
    missing = sorted(REQUIRED - run.keys())
    if missing:
        raise ValueError(f"{path}: missing required fields: {', '.join(missing)}")
    if run["schema_version"] != 1:
        raise ValueError(f"{path}: unsupported schema_version {run['schema_version']}")
    if run["phase"] not in {"baseline", "candidate"}:
        raise ValueError(f"{path}: phase must be baseline or candidate")
    if run["status"] not in {"passed", "failed", "blocked"}:
        raise ValueError(f"{path}: invalid status {run['status']}")
    unavailable = run.get("metrics_unavailable_reason", {})
    for key, value in run["metrics"].items():
        if value is None and key not in unavailable:
            raise ValueError(f"{path}: null metric {key} needs metrics_unavailable_reason")
    run["_path"] = str(path)
    return run


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    phases: dict[str, Any] = {}
    for phase in ("baseline", "candidate"):
        selected = [run for run in runs if run["phase"] == phase]
        if not selected:
            continue
        metrics: dict[str, Any] = {}
        for name in METRICS:
            values = [
                run["metrics"].get(name)
                for run in selected
                if isinstance(run["metrics"].get(name), (int, float))
            ]
            metrics[name] = {
                "mean": statistics.fmean(values) if values else None,
                "stddev": statistics.pstdev(values) if len(values) > 1 else 0 if values else None,
                "coverage": len(values),
                "total_runs": len(selected),
            }
        categories = Counter(
            mismatch.get("category", "uncategorized")
            for run in selected
            for mismatch in run["mismatches"]
        )
        phases[phase] = {
            "runs": len(selected),
            "passed": sum(run["status"] == "passed" for run in selected),
            "metrics": metrics,
            "mismatch_categories": dict(categories.most_common()),
        }
    comparison: dict[str, Any] = {}
    if "baseline" in phases and "candidate" in phases:
        for name in METRICS:
            baseline = phases["baseline"]["metrics"][name]
            candidate = phases["candidate"]["metrics"][name]
            comparable = (
                baseline["coverage"] > 0
                and baseline["coverage"] == candidate["coverage"]
                and baseline["total_runs"] == candidate["total_runs"]
            )
            delta = (
                candidate["mean"] - baseline["mean"]
                if comparable
                else None
            )
            comparison[name] = {
                "comparable": comparable,
                "baseline_mean": baseline["mean"],
                "candidate_mean": candidate["mean"],
                "delta": delta,
                "delta_percent": (
                    delta / baseline["mean"] * 100
                    if delta is not None and baseline["mean"] not in {None, 0}
                    else None
                ),
            }
    return {
        "schema_version": 1,
        "runs": len(runs),
        "phases": phases,
        "comparison": comparison,
        "sources": [run["_path"] for run in runs],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    files = discover(args.paths)
    if not files:
        raise SystemExit("No run.json files found")
    result = summarize([load_run(path) for path in files])
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
