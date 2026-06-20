#!/usr/bin/env python3
"""Validate Oz-orchestrated replatforming site-result.json artifacts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED = {
    "schema_version",
    "site",
    "site_slug",
    "phase",
    "agent_id",
    "status",
    "oz_metrics",
    "observer_run",
    "artifacts",
}
PHASES = {"baseline", "candidate"}
STATUSES = {"passed", "failed", "blocked", "invalid"}


def discover(paths: list[Path]) -> list[Path]:
    found: set[Path] = set()
    for path in paths:
        if path.is_dir():
            found.update(path.rglob("site-result.json"))
        elif path.name == "site-result.json":
            found.add(path)
    return sorted(found)


def validate(path: Path) -> dict[str, Any]:
    result = json.loads(path.read_text())
    errors: list[str] = []
    missing = sorted(REQUIRED - result.keys())
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if result.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if result.get("phase") not in PHASES:
        errors.append("phase must be baseline or candidate")
    if result.get("status") not in STATUSES:
        errors.append("invalid status")
    unavailable = result.get("oz_metrics_unavailable_reason", {})
    for name, value in result.get("oz_metrics", {}).items():
        if value is None and name not in unavailable:
            errors.append(f"null Oz metric {name} needs an unavailable reason")
    observer = result.get("observer_run")
    if not isinstance(observer, dict) or not isinstance(observer.get("run_json"), dict):
        errors.append("observer_run.run_json must be an object")
    return {
        "path": str(path),
        "site": result.get("site"),
        "phase": result.get("phase"),
        "status": result.get("status"),
        "valid": not errors,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    files = discover(args.paths)
    if not files:
        raise SystemExit("No site-result.json files found")
    results = [validate(path) for path in files]
    summary = {
        "schema_version": 1,
        "files": len(results),
        "valid": sum(result["valid"] for result in results),
        "invalid": sum(not result["valid"] for result in results),
        "statuses": dict(Counter(result["status"] for result in results)),
        "results": results,
    }
    rendered = json.dumps(summary, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    if summary["invalid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
