#!/usr/bin/env python3
"""
Validate a compiled Business Intermediate Representation (bir.json) for internal
consistency: every ID one section references must actually exist somewhere else
in the BIR. This is the failure mode a generic JSON-Schema validator won't catch
(the schema just says `tools` is an array of strings — it can't know whether a
string in there is a real entity ID or a typo) but it's exactly the one
SKILL.md's "Everything traces to the BIR" rule exists to prevent, so run this
after every full compile before treating the output as done.

No third-party dependencies (jsonschema may not be installed wherever this
skill runs) — only the standard library.

Usage:
    python3 scripts/validate_bir.py path/to/bir.json
    python3 scripts/validate_bir.py path/to/bir.json --strict   # warnings fail too

Exit code 0 = clean (or warnings only, without --strict). Exit code 1 = errors
found (broken references) or the file didn't parse.
"""

import json
import re
import sys
from pathlib import Path


def load(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_ids(bir: dict) -> dict:
    """Gather every ID namespace the BIR defines, so references can be checked against them."""
    return {
        "entities": {e["id"] for e in bir.get("entities", []) if "id" in e},
        "roles": {r["id"] for r in bir.get("roles", []) if "id" in r},
        "agents": {a["id"] for a in bir.get("aiAgents", []) if "id" in a},
        "workflows": {w["id"] for w in bir.get("workflows", []) if "id" in w},
        "integrations": {i["id"] for i in bir.get("integrations", []) if "id" in i},
    }


def check_ref(value, valid_sets, label, errors, allow_namespaces=("entities", "roles", "agents")):
    """Check `value` exists in at least one of the allowed ID namespaces."""
    if value is None:
        return
    for ns in allow_namespaces:
        if value in valid_sets[ns]:
            return
    errors.append(f"{label}: '{value}' not found in {', '.join(allow_namespaces)}")


def validate(bir: dict):
    errors: list[str] = []
    warnings: list[str] = []
    ids = collect_ids(bir)

    # --- required top-level structure ---
    for key in ("meta", "ontology", "entities", "roles", "workflows"):
        if key not in bir:
            errors.append(f"Missing required top-level key: '{key}'")

    # --- naming conventions (warnings only — see references/01-ontology-and-bir.md) ---
    for e in bir.get("entities", []):
        eid = e.get("id", "")
        if eid and not re.match(r"^[A-Z][A-Za-z0-9]*$", eid):
            warnings.append(f"Entity id '{eid}' is not PascalCase")
        for f in e.get("fields", []):
            fid = f.get("id", "")
            if fid and not re.match(r"^[a-z][A-Za-z0-9]*$", fid):
                warnings.append(f"Field id '{eid}.{fid}' is not camelCase")
            if f.get("type") == "relation":
                check_ref(f.get("relationTo"), ids, f"Entity '{eid}' field '{fid}'.relationTo", errors, ("entities",))

    for r in bir.get("roles", []):
        rid = r.get("id", "")
        if rid and not re.match(r"^[a-z][a-z0-9-]*$", rid):
            warnings.append(f"Role id '{rid}' is not kebab-case")

    # --- workflows: steps reference real actors and entities ---
    for w in bir.get("workflows", []):
        wid = w.get("id", "?")
        if wid and not re.match(r"^[a-z][a-z0-9-]*$", wid):
            warnings.append(f"Workflow id '{wid}' is not kebab-case")
        for step in w.get("steps", []):
            sid = step.get("id", "?")
            check_ref(step.get("actor"), ids, f"Workflow '{wid}' step '{sid}'.actor", errors)
            check_ref(step.get("entity"), ids, f"Workflow '{wid}' step '{sid}'.entity", errors, ("entities",))

    # --- AI agents: hierarchy, entities touched, escalation targets ---
    for a in bir.get("aiAgents", []):
        aid = a.get("id", "?")
        if aid and not re.match(r"^[a-z][a-z0-9-]*$", aid):
            warnings.append(f"Agent id '{aid}' is not kebab-case")
        if a.get("reportsTo"):
            check_ref(a["reportsTo"], ids, f"Agent '{aid}'.reportsTo", errors, ("agents",))
        for eid in a.get("entitiesTouched", []):
            check_ref(eid, ids, f"Agent '{aid}'.entitiesTouched", errors, ("entities",))
        if a.get("escalatesTo"):
            check_ref(a["escalatesTo"], ids, f"Agent '{aid}'.escalatesTo", errors, ("roles",))
        if a.get("tier") in ("specialist", "task") and not a.get("guardrails"):
            warnings.append(f"Agent '{aid}' (tier={a.get('tier')}) has no guardrails — see references/04-ai-agents.md")

    # --- automations & reminders: trigger/owner entities exist ---
    for auto in bir.get("automations", []):
        auid = auto.get("id", "?")
        trig_entity = (auto.get("trigger") or {}).get("entity")
        check_ref(trig_entity, ids, f"Automation '{auid}'.trigger.entity", errors, ("entities",))
        check_ref(auto.get("owner"), ids, f"Automation '{auid}'.owner", errors)

    for rem in bir.get("reminders", []):
        rmid = rem.get("id", "?")
        check_ref(rem.get("entity"), ids, f"Reminder '{rmid}'.entity", errors, ("entities",))

    # --- integrations: synced entities exist ---
    for integ in bir.get("integrations", []):
        iid = integ.get("id", "?")
        for eid in integ.get("entitiesSynced", []):
            check_ref(eid, ids, f"Integration '{iid}'.entitiesSynced", errors, ("entities",))

    # --- KPIs: target roles exist ---
    for kpi in bir.get("kpis", []):
        kid = kpi.get("id", "?")
        for rid in kpi.get("targetRoles", []):
            check_ref(rid, ids, f"KPI '{kid}'.targetRoles", errors, ("roles",))

    # --- views: audience should resolve to a role or a recognizable human label ---
    for v in bir.get("views", []):
        vid = v.get("id", "?")
        aud = v.get("audience")
        if aud and aud not in ids["roles"] and "/" not in aud and " " not in aud:
            warnings.append(f"View '{vid}'.audience '{aud}' doesn't match a role id — "
                             f"OK if it's a human label like 'board/investors', otherwise check for a typo")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    path = sys.argv[1]
    strict = "--strict" in sys.argv[2:]

    if not Path(path).exists():
        print(f"File not found: {path}")
        sys.exit(1)

    try:
        bir = load(path)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}")
        sys.exit(1)

    errors, warnings = validate(bir)

    if errors:
        print(f"❌ {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print(f"⚠️  {len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    if not errors and not warnings:
        print("✅ BIR is internally consistent — no broken references, no naming issues.")
    elif not errors:
        print("✅ No broken references (warnings above are style-only).")

    sys.exit(1 if errors or (strict and warnings) else 0)


if __name__ == "__main__":
    main()
