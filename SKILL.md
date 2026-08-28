---
name: business-compiler
description: Compiles any business idea or category into a complete, ready-to-deploy business operating system — data model, workflows, UI/dashboards, advanced multi-dimensional analytics and per-audience views, an AI agent workforce with a strategic reasoning layer, an automation/reminder engine, WhatsApp Business integration, a social-media marketing suite, advanced marketing (ads, A/B testing, multi-touch attribution, drip sequences), a full CRM (sales pipeline, lead scoring, support ticketing/SLAs, customer-360), native double-entry accounting & finance (chart of accounts, ledger, multi-currency, tax, budgets, period close), inventory & supply chain, HR & payroll, a knowledge base/document module, generic integrations with any third-party platform, RBAC/ABAC security, and a simulation/forecasting layer. Use this skill whenever the user describes a business, startup idea, or operational process (a shop, clinic, agency, SaaS, farm, restaurant, service business, franchise, etc.) and wants it turned into a system, a spec, an app, an ERP, a plan to build one, "how would I run/automate this," or wants business analytics, reporting, dashboards, accounting, CRM, or an AI advisor for a business. Trigger even if they don't say "business compiler" explicitly — phrases like "I'm opening a...", "help me set up systems for my...", "I want to automate my business", "build me an ERP/CRM for...", or "/business-compiler" all qualify.
---

# Business Compiler

You are compiling a business — the way a compiler turns source code into an executable. The
"source" is a business category plus whatever context the user gives you. The "target" is a
full specification (and, where the user wants it, real scaffolded artifacts) of the systems
that business needs to run: data, workflows, UI, analytics, per-audience views, an AI
workforce (including a strategic reasoning layer, not just task execution), automations,
marketing, a knowledge base, integrations, security, and forecasting — all cross-referenced
through one shared model so nothing you generate contradicts anything else.

Treat every invocation as producing a real deliverable a founder or engineering team could
hand off and build from — not a generic template with the business name swapped in. Depth
and domain-specificity are the whole point.

## Invocation

`/business-compiler <business description>` — e.g. "Multi-branch laundry with pickup/delivery,
inventory, employees, accounting, CRM, automation and AI."

Optional modifier: `/include-sections A,B,C` — compile only the named sections (see the
Section Catalog below for names). Without it, compile all sections. Users may also just
describe their business in plain language without the slash command — treat that the same way.

If invoked conversationally rather than as a full spec request (e.g. "how do I remind
customers about pickup?"), answer the specific question using the relevant reference file
below rather than compiling the entire business — you don't need to run the full pipeline
for a narrow question.

## The Compilation Pipeline

Work through these stages in order. Stages 1–3 build the shared model everything else reads
from; do not skip to section generation before you have a BIR, or the sections will drift out
of sync with each other (e.g. an AI agent referencing a field the data model doesn't have).

### Stage 1 — Discover the Business DNA

Read `references/01-ontology-and-bir.md` for the discovery procedure. In short: infer as much
as you reasonably can from the category and any context given (an experienced operator in that
industry would recognize the entities, roles, and workflows involved), and only ask the user
clarifying questions when a genuinely pivotal, non-obvious fork exists (e.g. "single location
or multi-branch?" changes the data model shape; "B2B or B2C" changes the CRM and marketing
approach). Don't interrogate — 0-3 sharp questions at most, and prefer sensible defaults with
a note on what you assumed over blocking on questions.

### Stage 2 — Build the Ontology and compile to BIR

Turn the discovered DNA into the Business Intermediate Representation (BIR): a single JSON
document conforming to `assets/bir-schema.json` that names every entity, role, workflow, and
capability the business needs. Every section you generate afterward is a compilation target
*from* this BIR — this is what keeps a WhatsApp reminder referencing the same `Appointment`
entity that the data model and the dashboard use. See `references/01-ontology-and-bir.md`.

### Stage 3 — Compile each requested section

For each section in scope (all of them, unless `/include-sections` narrows it), read the
matching reference file and produce that section from the BIR. The reference files contain
the detailed patterns, checklists, and worked structures — SKILL.md intentionally does not
duplicate them here.

## Section Catalog

| # | Section | Reference file | What it produces |
|---|---------|-----------------|-------------------|
| 1 | Data Model & Workflows | `references/02-data-model-workflows.md` | Entities, fields, relations, state machines, executable business workflows |
| 2 | UI & Dashboards | `references/03-ui-dashboards.md` | Responsive forms, views, and live KPI dashboards per role |
| 3 | Analytics & Reporting | `references/13-analytics-and-reporting.md` | Multi-dimensional reporting cube, financial statements, cohort/retention analysis, benchmarking, anomaly detection, a business health score |
| 4 | Business Views | `references/14-business-views.md` | Per-audience bundles (Executive, Operations, Financial, CRM, Team, Growth, Technical/diagrams, Board, Field) with cadence and medium |
| 5 | AI Agents & Reasoning | `references/04-ai-agents.md` | An AI agent hierarchy (orchestrator/advisor/specialist/task) with tools, triggers, guardrails, and a strategic business-reasoning layer (structured decision frameworks, not just task execution) |
| 6 | Automations & Reminders | `references/05-automations-reminders.md` | Event→condition→action automation engine, scheduled reminders, escalation chains |
| 7 | WhatsApp Integration | `references/06-whatsapp-integration.md` | WhatsApp Business API setup, message templates, conversational flows, opt-in/consent |
| 8 | Social Media Suite | `references/07-social-media-suite.md` | Multi-platform content calendar, publishing, listening, analytics |
| 9 | Marketing | `references/08-marketing-crm.md` | Segmentation, funnels, campaigns, lifecycle drip sequences, paid ads, A/B testing, multi-touch attribution, loyalty, referral |
| 10 | CRM: Sales Pipeline & Support | `references/17-crm-sales-support.md` | Deal/pipeline stages, lead scoring, support ticketing with SLAs, customer-360 view |
| 11 | Accounting & Finance | `references/16-accounting-finance.md` | Chart of accounts, double-entry ledger auto-posted from workflows, multi-currency, tax, banking/reconciliation, budgets, period close |
| 12 | Inventory & Supply Chain | `references/18-inventory-supply-chain.md` | Stock tracking, warehouses, purchase orders, suppliers, reorder policy, transfers, shrinkage |
| 13 | HR & Payroll | `references/19-hr-payroll.md` | Employee lifecycle, scheduling, compensation/payroll pipeline, leave, performance |
| 14 | Knowledge Base & Documents | `references/15-knowledge-and-documents.md` | Document templates (invoices, contracts, SOPs), a knowledge base that grounds customer-facing agents |
| 15 | Integrations Framework | `references/09-integrations-framework.md` | Generic "connect to any platform" connector spec (payments, accounting, maps, e-commerce, calendars, etc.) |
| 16 | Security | `references/10-security-rbac-abac.md` | Roles, permissions, attribute-based policies, audit, compliance notes |
| 17 | Simulation & Forecasting | `references/11-simulation-forecasting.md` | Demand/cashflow/staffing simulators, forecasting models, what-if scenarios |
| 18 | Deployment Guide | `references/12-deployment-guide.md` | Step-by-step path from spec to running system, stack choices, rollout plan |

Sections 3–14 are the "exhaustive AI / analytics / automation / operations" layer the
compiler is known for — never skip these by default even for a simple-sounding business; a
one-location laundromat still benefits from a reminder agent, a WhatsApp pickup-ready
notification, a real ledger instead of a shoebox of receipts, and a weekly owner digest.
Sections 11–13 (Accounting, Inventory, HR) should be skipped or minimized when they genuinely
don't apply — a single-founder SaaS has no inventory and no payroll; say so rather than
padding the output.

## Cross-Cutting Rules

- **Everything traces to the BIR.** An AI agent's tools, an automation's trigger entity, a
  dashboard's KPI, a WhatsApp template's variables — all must reference real BIR entity/field
  IDs. If a section needs something the BIR doesn't have, add it to the BIR first (staying
  consistent) rather than inventing an orphaned reference.
- **Be domain-specific, not generic.** "Send a reminder" is not an output; "Send a WhatsApp
  reminder 2 hours before a grooming appointment, with a reschedule button, in the customer's
  saved language" is. Every generated item should read as if written by someone who has run
  this exact kind of business.
- **Right-size to the business.** A solo car-wash bay and a 40-branch laundry chain both go
  through the same pipeline, but the output should visibly differ in scale (number of roles,
  automation volume, integration count) — don't pad small businesses with enterprise bloat, and
  don't undersell complex ones.
- **Output artifacts, not prose essays.** Prefer structured JSON/YAML/tables per
  `assets/bir-schema.json` and the per-section formats in the reference files, with brief prose
  only to explain non-obvious choices. The user should be able to hand the output to an
  engineering team or feed it back into Claude Code to scaffold real code.
- **Write files.** For a full compile, write the BIR and each compiled section to files (e.g.
  a `<business-slug>/` output directory: `bir.json`, `data-model.md`, `dashboards.md`,
  `analytics.md`, `views.md`, `ai-agents.md`, `automations.md`, `whatsapp.md`,
  `social-media.md`, `marketing.md`, `crm.md`, `accounting.md`, `inventory.md`, `hr.md`,
  `knowledge-base.md`, `integrations.md`, `security.md`, `simulation.md`,
  `deployment-guide.md`) rather than only printing to chat, so the result is a real
  deliverable — then summarize what was produced and where.
- **Version and iterate.** Treat a follow-up like "add loyalty points" or "make it
  multi-branch" as a recompile of the affected BIR entities and the sections that depend on
  them, not a restart from scratch — re-read the existing output files first if they exist.
- **Validate before declaring done.** After writing `bir.json` for a full compile, run
  `python3 scripts/validate_bir.py <output-dir>/bir.json`. It's a dependency-free linter that
  catches exactly the failure mode the first rule above warns about — an agent, automation, or
  workflow step referencing an entity/role/agent ID that doesn't actually exist in the BIR.
  Fix anything it reports as an error before presenting the compile as finished; warnings
  (naming convention, missing guardrails) are worth a glance but not blocking.

## Worked Example

`examples/example-laundry-excerpt.md` shows an abbreviated compile for a multi-branch laundry
business, focused on the agent/automation/WhatsApp/marketing/integration layers. Skim it when
you want a calibration reference for depth and tone.
