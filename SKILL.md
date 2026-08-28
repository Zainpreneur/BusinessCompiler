---
name: business-compiler
description: Compiles any business idea or category into a complete, ready-to-deploy business operating system — data model, workflows, UI/dashboards, advanced multi-dimensional analytics and per-audience views, cross-platform data aggregation that pulls data from every integrated platform into advanced blended analysis (true ROAS, full-funnel conversion, downtime cost, partner benchmarking), an AI agent workforce with a strategic reasoning layer (plus a voice/omnichannel agent and a system-health meta-agent), an automation/reminder engine, WhatsApp Business integration, a social-media marketing suite, advanced marketing (ads, A/B testing, multi-touch attribution, drip sequences), a full CRM (sales pipeline, lead scoring, support ticketing/SLAs, customer-360), native double-entry accounting & finance (chart of accounts, ledger, multi-currency, tax, budgets, period close), inventory & supply chain, HR & payroll, asset/equipment tracking with IoT and predictive maintenance, a knowledge base/document module, generic integrations with any third-party platform PLUS the business's own outbound API and webhook platform for other systems to integrate into it, RBAC/ABAC security, a simulation/forecasting layer, and a final comprehensive QA pass that checks business logic, AI logic, and cross-module consistency before the compile is called done — all written into one consistently structured, clustered output package regardless of business niche. Use this skill whenever the user describes a business, startup idea, or operational process (a shop, clinic, agency, SaaS, farm, restaurant, service business, franchise, etc.) and wants it turned into a system, a spec, an app, an ERP, a plan to build one, "how would I run/automate this," or wants business analytics, reporting, dashboards, accounting, CRM, an API, or an AI advisor for a business. Trigger even if they don't say "business compiler" explicitly — phrases like "I'm opening a...", "help me set up systems for my...", "I want to automate my business", "build me an ERP/CRM for...", or "/business-compiler" all qualify.
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

Work through these stages in order. Stages 1–2 build the shared model everything else reads
from; do not skip to section generation before you have a BIR, or the sections will drift out
of sync with each other (e.g. an AI agent referencing a field the data model doesn't have).
Stage 4 is not optional for a full compile — it's what keeps this a system that was actually
checked, not just a large pile of plausible-looking Markdown.

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
duplicate them here. Compile in cluster order (Foundation → Intelligence → Operations →
Growth → Finance → Platform), with one exception: Cross-Platform Data Aggregation
(`references/23-cross-platform-data-aggregation.md`) compiles *last*, after Platform, because
it needs to know every integration and API partner before it can define what external data
feeds analytics — see the Section Catalog's dagger note.

### Stage 4 — Comprehensive QA

For a full compile (not narrowed by `/include-sections` to something trivial), read
`references/22-qa-and-completeness.md` and walk every compiled section back through its
checklist: business logic (dead-end states, unbacked KPIs, numbers that disagree across
modules), AI logic (every agent complete and guardrailed, no unchecked authority over
irreversible actions), integration/API/security logic, and coverage against what the user
actually asked for. Fix what you find; write `07-delivery/qa-report.md` documenting the pass.
Then run `python3 scripts/validate_bir.py <output-dir>/bir.json` as the mechanical half of
this stage — it catches broken cross-references and a few structural issues (duplicate IDs,
dead-end states) that Stage 4's manual checklist would otherwise have to catch by hand. Fix
anything it reports as an error; warnings are worth a glance but not blocking. Only present the
compile as finished once both halves of this stage are done and `00-index.md` is written.

## Section Catalog

Every section belongs to one of seven clusters — this is also the compilation order within
Stage 3, and it's the same grouping the Output Package Structure below turns into real
directories, so "what cluster is this in" answers both "when do I compile it" and "where does
it live" at once.

| Cluster | Section | Reference file | Output file | What it produces |
|---|---|---|---|---|
| **Foundation** | Data Model & Workflows | `references/02-data-model-workflows.md` | `01-foundation/data-model.md` | Entities, fields, relations, state machines, executable business workflows |
| **Foundation** | UI & Dashboards | `references/03-ui-dashboards.md` | `01-foundation/dashboards.md` | Responsive forms, views, and live KPI dashboards per role |
| **Foundation** | Security | `references/10-security-rbac-abac.md` | `01-foundation/security.md` | Roles, permissions, attribute-based policies, audit, compliance notes |
| **Intelligence** | Analytics & Reporting | `references/13-analytics-and-reporting.md` | `02-intelligence/analytics.md` | Multi-dimensional reporting cube, financial statements, cohort/retention analysis, benchmarking, anomaly detection, a business health score |
| **Intelligence** | Business Views | `references/14-business-views.md` | `02-intelligence/views.md` | Per-audience bundles (Executive, Operations, Financial, CRM, Team, Growth, Technical/diagrams, Board, Field) with cadence and medium |
| **Intelligence** | AI Agents & Reasoning | `references/04-ai-agents.md` | `02-intelligence/ai-agents.md` | An AI agent hierarchy (orchestrator/advisor/specialist/task) with tools, triggers, guardrails, a strategic reasoning layer, and a system-health meta-agent |
| **Intelligence** | Simulation & Forecasting | `references/11-simulation-forecasting.md` | `02-intelligence/simulation.md` | Demand/cashflow/staffing simulators, forecasting models, what-if scenarios |
| **Operations** | Automations & Reminders | `references/05-automations-reminders.md` | `03-operations/automations.md` | Event→condition→action automation engine, scheduled reminders, escalation chains |
| **Operations** | Inventory & Supply Chain | `references/18-inventory-supply-chain.md` | `03-operations/inventory.md` | Stock tracking, warehouses, purchase orders, suppliers, reorder policy, transfers, shrinkage |
| **Operations** | Assets, Equipment & IoT | `references/21-assets-equipment-iot.md` | `03-operations/assets-iot.md` | Asset registry, preventive maintenance, IoT telemetry, a predictive-maintenance agent |
| **Operations** | HR & Payroll | `references/19-hr-payroll.md` | `03-operations/hr.md` | Employee lifecycle, scheduling, compensation/payroll pipeline, leave, performance |
| **Growth** | WhatsApp Integration | `references/06-whatsapp-integration.md` | `04-growth/whatsapp.md` | WhatsApp Business API setup, message templates, conversational flows, opt-in/consent |
| **Growth** | Social Media Suite | `references/07-social-media-suite.md` | `04-growth/social-media.md` | Multi-platform content calendar, publishing, listening, analytics |
| **Growth** | Marketing | `references/08-marketing-crm.md` | `04-growth/marketing.md` | Segmentation, funnels, campaigns, lifecycle drip sequences, paid ads, A/B testing, multi-touch attribution, loyalty, referral |
| **Growth** | CRM: Sales Pipeline & Support | `references/17-crm-sales-support.md` | `04-growth/crm.md` | Deal/pipeline stages, lead scoring, support ticketing with SLAs, customer-360 view |
| **Finance** | Accounting & Finance | `references/16-accounting-finance.md` | `05-finance/accounting.md` | Chart of accounts, double-entry ledger auto-posted from workflows, multi-currency, tax, banking/reconciliation, budgets, period close |
| **Platform** | Knowledge Base & Documents | `references/15-knowledge-and-documents.md` | `06-platform/knowledge-base.md` | Document templates (invoices, contracts, SOPs), a knowledge base that grounds customer-facing agents |
| **Platform** | Integrations Framework | `references/09-integrations-framework.md` | `06-platform/integrations.md` | Generic "connect to any platform" connector spec — this business *consuming* other platforms |
| **Platform** | Platform API & Webhooks | `references/20-api-and-webhooks.md` | `06-platform/api-webhooks.md` | The mirror image of Integrations — this business's own API/webhook surface for *other systems to integrate into it* |
| **Intelligence**† | Cross-Platform Data Aggregation | `references/23-cross-platform-data-aggregation.md` | `02-intelligence/data-aggregation.md` | Pulls data from every integration and platform-API partner into the analytics cube, plus the advanced cross-source analyses (true ROAS, full-funnel conversion, downtime cost, partner benchmarking) only possible once sources are blended |
| **Delivery** | Deployment Guide | `references/12-deployment-guide.md` | `07-delivery/deployment-guide.md` | Step-by-step path from spec to running system, stack choices, rollout plan |
| **Delivery** | Comprehensive QA (Stage 4, always last) | `references/22-qa-and-completeness.md` | `07-delivery/qa-report.md` | Business/AI-logic/cross-module checklist results and what was fixed |

† Files under `02-intelligence/` like everything else in that cluster, but — unlike every
other section — **compile it out of cluster order, last in Stage 3** (positioned in the table
right after Platform, above): it depends on knowing every integration and API partner, which
aren't compiled until the Platform cluster. Revisit `analytics.md` at this point too if the
aggregation work surfaces a cross-source measure worth promoting into the main reporting cube.

**Foundation, Intelligence, Operations, and Growth are never skipped by default**, even for a
simple-sounding business — a one-location laundromat still gets a reminder agent, a WhatsApp
pickup-ready notification, a real ledger instead of a shoebox of receipts, and a weekly owner
digest. Within **Operations**, Inventory/Assets-IoT/HR should each be skipped or minimized
when they genuinely don't apply (a single-founder SaaS has no inventory, no equipment, no
payroll) — say so rather than padding the output. Within **Platform**, Platform API & Webhooks
is worth skipping only for a genuinely single-operator business with no plausible third-party
integrators; **Finance** (native accounting) is worth skipping only when the business has
firmly committed to an external accounting product instead (see `09-integrations-framework.md`).
Cross-Platform Data Aggregation should be brief (a short paragraph, not the full treatment)
for a business with only one or two integrations — there isn't much to aggregate yet, and
that's fine; say so rather than manufacturing analysis the data doesn't support.

## Output Package Structure

A full compile is a small repository, not a folder of loose files — structure it the same way
every time, for every business, so the shape is instantly familiar whether the business is a
laundromat or a SaaS platform, and so a future session (this one, on a follow-up, or a fresh
one working from these files alone) can navigate it without re-reading everything:

```
<business-slug>/
├── 00-index.md              — master table of contents + executive summary (see below)
├── bir.json                 — the BIR: the machine-readable root everything else compiles from
├── 01-foundation/           — data model, dashboards, security: the base layer everything else depends on
├── 02-intelligence/         — analytics, views, AI agents, simulation, cross-platform data aggregation: the "brain"
├── 03-operations/           — automations, inventory, assets/IoT, HR: day-to-day running
├── 04-growth/               — WhatsApp, social, marketing, CRM: the customer-facing engine
├── 05-finance/              — accounting: the ledger
├── 06-platform/             — knowledge base, integrations in, API/webhooks out
└── 07-delivery/             — deployment guide, qa-report.md
```

Use the exact cluster folder names above — the consistency is the point; don't rename them
per business even when a niche term would feel more natural, since a founder or engineer who's
seen this compiler's output once should recognize the shape immediately on the next one.

### `00-index.md`

The entry point — write this *last*, after every section is compiled and QA'd, so it reflects
the finished package, not a plan for it. It should let someone (human or AI) understand the
whole business and find anything in under a minute:

1. **Executive summary**: business name, category, scale, audience, the primary lifecycle from
   the ontology — 3-5 sentences, no jargon.
2. **Table of contents**: every output file, grouped by cluster, one line each — the file's
   path plus a one-sentence description (reuse the "What it produces" column from the Section
   Catalog, written in this business's actual terms rather than the generic wording).
3. **Key decisions**: the `meta.assumptions` logged during discovery, so anyone reading later
   knows what was inferred vs. explicitly stated.
4. **Status**: the QA pass result (clean, or what was fixed) and the validator output, so the
   index doubles as a one-glance confidence check on the whole package.

### Standard page template

Every compiled section file (everything under the cluster folders) opens with the same short
header before its content, so pages read as one cohesive product instead of 20 independently-
styled documents:

```markdown
# <Section Title>

*Part of the <Cluster> cluster. Compiled from `bir.json`.*

<1-3 sentences: what was decided for THIS business specifically — not a restatement of what
the section type generally covers.>

---

<the section's actual content, per that reference file's own Output Format guidance>
```

Skip further structural ceremony beyond that header — the reference files already specify
each section's internal format (tables, entity blocks, etc.); this template only standardizes
the opening so every page starts the same way regardless of which reference file produced it.

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
- **Write files, following the Output Package Structure.** For a full compile, write `bir.json`
  and every compiled section into the clustered directory layout defined above — including
  `07-delivery/qa-report.md` from Stage 4, which is a required deliverable of every full
  compile, not an optional side effect of running the checklist — finishing with `00-index.md`
  once everything else, QA report included, is done. Write to files rather than only printing
  to chat, so the result is a real deliverable — then summarize what was produced and where.
  For a narrowed `/include-sections` compile, still use the matching cluster folder(s) for
  whatever's produced, so a partial compile slots cleanly into a full one later rather than
  needing to be reorganized.
- **Version and iterate.** Treat a follow-up like "add loyalty points" or "make it
  multi-branch" as a recompile of the affected BIR entities and the sections that depend on
  them, not a restart from scratch — re-read the existing output files first if they exist.
  Re-run Stage 4 after any recompile, not just after the first full compile — a follow-up
  change is exactly the kind of edit that can quietly break a cross-reference or a number two
  modules used to agree on.

## Worked Example

`examples/example-laundry-excerpt.md` shows an abbreviated compile for a multi-branch laundry
business, focused on the agent/automation/WhatsApp/marketing/integration layers. Skim it when
you want a calibration reference for depth and tone.
