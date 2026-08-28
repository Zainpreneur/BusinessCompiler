# BusinessCompiler

A Claude skill that compiles a business idea or category into a complete, ready-to-deploy
business operating system: data model, workflows, UI/dashboards, analytics, an AI agent
workforce with a strategic reasoning layer, automations and reminders, WhatsApp integration, a
social media suite, marketing, a full CRM, native accounting, inventory, HR/payroll, a
knowledge base, integrations with any third-party platform, security, and simulation/
forecasting — all generated from one consistent shared model so nothing contradicts anything
else.

## Using it

In Claude Code (or anywhere this skill is installed), invoke it as:

```
/business-compiler <describe the business>
```

e.g. `/business-compiler Multi-branch laundry with pickup/delivery, employees, accounting, CRM, automation and AI`

Add `/include-sections A,B,C` to compile only specific sections — see the Section Catalog in
`SKILL.md` for the full list of names.

## How it's built

```
SKILL.md                     — the orchestrator: discovery → ontology/BIR → per-section compile
assets/
  bir-schema.json             — the Business Intermediate Representation (BIR) schema every
                                 section compiles from; the shared vocabulary that keeps an AI
                                 agent, a WhatsApp template, and a dashboard KPI referencing the
                                 same entities instead of drifting apart
references/                   — one file per compiled section (see SKILL.md's Section Catalog
                                 for the full map from section name to file)
scripts/
  validate_bir.py              — dependency-free linter: checks a compiled bir.json for broken
                                 cross-references (an agent/automation/workflow pointing at an
                                 entity or role that doesn't exist)
examples/
  example-laundry-excerpt.md   — a worked, abbreviated compile used to calibrate depth and tone
skill.json                    — marketplace-style metadata/description for this skill
```

This follows the standard progressive-disclosure pattern for Claude skills: `SKILL.md` stays
short and is always loaded when the skill triggers; the `references/` files are read on demand,
one per section, so the compiler can go deep on each without bloating the always-loaded
context.

## Validating a compile

After a full compile writes `bir.json`, sanity-check it:

```
python3 scripts/validate_bir.py <output-dir>/bir.json
```

This catches broken references (an AI agent touching an entity that was never defined, a
workflow step assigned to a role that doesn't exist) — the exact class of error the "everything
traces to the BIR" rule in `SKILL.md` exists to prevent.
