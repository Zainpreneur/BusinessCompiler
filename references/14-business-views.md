# Multiple Views

Compiles `views`: the same underlying BIR and analytics, curated differently for different
audiences and moments. A dashboard tile (`03-ui-dashboards.md`) and a report
(`13-analytics-and-reporting.md`) are ingredients; a **view** is the assembled meal for one
audience — what they see, at what cadence, through what medium. Without this layer, everyone
ends up staring at the same undifferentiated firehose of data, which is how dashboards go
unused.

## Standard views (compile what fits; most businesses need 4-7 of these)

For each, define `audience`, `cadence`, `medium`, and `includes` (the KPI/report/dashboard IDs
it bundles):

- **Executive/Owner View** — leads with the business health score, then the 3-5 KPIs that
  matter most, then *only* exceptions/alerts (not raw data — an owner should never need to
  hunt for what needs their attention). Cadence: real-time available, but the primary
  consumption is the daily/weekly digest.
- **Operations View** — today's queue/status board, exceptions needing action right now
  (overdue orders, understaffed shifts). Real-time, in-app, usually the busiest screen in the
  system.
- **Financial View** — P&L, cash flow, AR/AP aging, integration sync status with accounting.
  Weekly/monthly cadence, in-app or emailed report.
- **Customer/CRM View** — segment sizes and movement, churn-risk list, campaign performance,
  WhatsApp/social engagement. Weekly, in-app.
- **Team/HR View** — schedules, coverage gaps, performance summaries, payroll status. Weekly.
- **Growth/Marketing View** — funnel stage volumes, campaign ROI, social analytics,
  channel attribution. Weekly, in-app.
- **Technical/Architecture View** — for the engineering team, not day-to-day operators:
  entity-relationship diagram, AI agent org chart, integration map, automation catalog. See
  the diagramming note below. On-demand.
- **Board/Investor View** — quarterly rollups, growth trend lines, headline metrics only —
  deliberately excludes operational noise a board doesn't need. Monthly/quarterly, PDF or
  emailed report.
- **Field/Mobile View** — for staff who aren't at a desk (drivers, technicians, delivery):
  minimal, action-oriented, works on a phone, tolerant of poor connectivity (queue actions
  offline, sync when back online). Real-time, in-app.

Don't compile every view for every business — a solo operator doesn't need a separate Board
View or Team View for themself; collapse those into the Executive View and say so.

## Diagram views

The Technical/Architecture view benefits from actual diagrams, not just a text description.
When producing this view as (or inside) a published Artifact, use Mermaid — it renders
natively there with no library needed:

- **Entity-relationship diagram**: from the entities/relations in `02-data-model-workflows.md`.
- **Agent org chart**: from the orchestrator/advisor/specialist/task hierarchy in
  `04-ai-agents.md`.
- **System/integration map**: entities and agents on one side, third-party platforms from
  `09-integrations-framework.md` on the other, edges labeled with direction and sync cadence.

If not producing an Artifact (e.g. writing plain Markdown output files), still describe these
as Mermaid code blocks — they're readable as structured text even unrendered, and any Markdown
renderer that supports Mermaid will pick them up for free.

## Choosing medium and cadence deliberately

Match medium to how the audience actually works, not just "everything's a dashboard":

- An owner checking in from their phone between tasks wants a WhatsApp or emailed digest, not
  a login-required dashboard.
- A board member wants a PDF they can forward, not app access.
- Field staff want push notifications and a lightweight mobile view, not the full back-office
  UI shrunk down.

## Output format

One `##` per compiled view: Audience / Cadence / Medium / Includes (bulleted list of KPI/
report/dashboard IDs, cross-referenced to where each is defined). Close the Technical/
Architecture view with its Mermaid diagram(s) if produced.
