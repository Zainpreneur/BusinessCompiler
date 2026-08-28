# UI & Dashboards

Compiles responsive forms/views and KPI dashboards, one set per role from the BIR.

## Per-role views

For every human role in `roles`, define:

- **Home view**: the 3–5 things that role needs to see the second they open the app (today's
  appointments, low-stock alerts, pending approvals). This is the antidote to generic CRUD
  screens — it should read like "what does the front-desk person actually glance at first
  thing Monday morning."
- **Forms**: for each entity that role creates/edits, a form spec — field, input type
  (text/select/date/toggle/file/geopicker), validation, and which fields are auto-filled by an
  AI agent or automation vs. manually entered (e.g. "estimated completion time — auto-filled
  by the scheduling agent, editable").
- **List/table views**: default filters and sort for that role (a technician sees "my jobs
  today", not "all jobs ever").
- **Mobile vs. desktop**: call out which views are mobile-first (field staff, delivery
  drivers) vs. desktop-first (back-office, accounting) — this affects component choice later.

## Dashboards

For each KPI in `kpis` (and add domain-standard ones if the BIR list is thin — e.g. every
service business wants utilization rate, every retail-flavored one wants sell-through), specify:

- Formula (reuse from BIR).
- Visualization type (number tile, trend line, bar-by-segment, funnel).
- Refresh cadence (real-time, hourly, daily).
- Which role(s) see it, and whether it's also surfaced via a proactive alert (ties into
  automations — "if utilization drops below 60% for 3 days, notify the branch manager").

## Layout conventions

- One "Owner/Executive" dashboard aggregating cross-branch or cross-department KPIs, even for
  a solo business (it's just their one view then) — this is the "does the business make
  sense at a glance" screen.
- Group forms/dashboards by the same subdomain headers used in the data model (Core /
  Inventory / Staffing / Finance / CRM) so a reader can trace a KPI back to the entity/fields
  that produce it.

## Output format

Markdown, one `##` per role, with a table for forms/fields and a table for that role's
dashboard tiles. Keep it implementation-agnostic (don't hardcode a specific component library)
unless the deployment guide's chosen stack calls for concrete component names.
