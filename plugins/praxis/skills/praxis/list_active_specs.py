#!/usr/bin/env python3
"""List active praxis specs as a compact JSON array.

An "active" spec is one that is not fully complete: some discovery phase is
still null, it has no issues yet, or at least one issue is not "done".

Scans <root>/docs/specs/*/metadata.json (root defaults to the current working
directory). Prints one JSON object per active spec to stdout so the praxis
skill can pick / match a spec without reading every metadata.json itself.

Output object shape:
  {
    "slug": "...",
    "name": "...",
    "description": "...",
    "phase": "discovery" | "implementation",
    "state": "discovery · model" | "ISSUE-02 · tdd" | "ISSUE-02 pending",
    "next_issue": "ISSUE-02" | null,
    "issues": {"total": 3, "done": 1, "pending": 2, "in_progress": 0, "blocked": 0}
  }

Usage:
  python3 list_active_specs.py [root]   # root defaults to "."
"""

import json
import sys
from pathlib import Path


def first_null_phase(phases):
    """Return the first phase whose value is null, honoring insertion order."""
    if not isinstance(phases, dict):
        return None
    for name, value in phases.items():
        if value is None:
            return name
    return None


def pick_next_issue(issues):
    """Pick the active issue: in_progress first, else first eligible pending.

    Eligible = status "pending" and all blocked_by issues are "done".
    Returns (issue_id, issue_obj) or (None, None).
    """
    # in_progress takes priority
    for issue_id, issue in issues.items():
        if issue.get("status") == "in_progress":
            return issue_id, issue
    for issue_id, issue in issues.items():
        if issue.get("status") != "pending":
            continue
        blockers = issue.get("blocked_by") or []
        if all(issues.get(b, {}).get("status") == "done" for b in blockers):
            return issue_id, issue
    return None, None


def summarize(meta):
    """Return a summary dict if the spec is active, else None."""
    discovery = meta.get("discovery") or {}
    issues = meta.get("issues") or {}

    discovery_pending = first_null_phase(discovery)
    counts = {"total": len(issues), "done": 0, "pending": 0,
              "in_progress": 0, "blocked": 0}
    for issue in issues.values():
        status = issue.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1

    all_issues_done = bool(issues) and counts["done"] == counts["total"]
    is_active = bool(discovery_pending) or not issues or not all_issues_done
    if not is_active:
        return None

    base = {
        "slug": meta.get("slug"),
        "name": meta.get("name"),
        "description": meta.get("description"),
        "issues": counts,
    }

    if discovery_pending:
        base["phase"] = "discovery"
        base["state"] = f"discovery · {discovery_pending}"
        base["next_issue"] = None
        return base

    # discovery complete → implementation
    issue_id, issue = pick_next_issue(issues)
    base["phase"] = "implementation"
    base["next_issue"] = issue_id
    if issue_id is None:
        # nothing eligible (e.g. all remaining are blocked)
        base["state"] = "no eligible issue (blocked or all done)"
    else:
        step = first_null_phase(issue.get("phases") or {})
        if step is None or issue.get("status") == "pending":
            base["state"] = f"{issue_id} pending"
        else:
            base["state"] = f"{issue_id} · {step}"
    return base


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    specs_dir = root / "docs" / "specs"

    active = []
    if specs_dir.is_dir():
        for meta_path in sorted(specs_dir.glob("*/metadata.json")):
            try:
                meta = json.loads(meta_path.read_text())
            except (json.JSONDecodeError, OSError) as exc:
                print(f"warning: skipping {meta_path}: {exc}", file=sys.stderr)
                continue
            summary = summarize(meta)
            if summary is not None:
                active.append(summary)

    json.dump(active, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
