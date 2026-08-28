# Advanced Business Analytics & Reporting

Compiles `analytics`: the retrospective, multi-dimensional analysis layer that sits beneath
the live dashboards in `03-ui-dashboards.md`. Where a dashboard answers "what's happening
right now for my role," analytics answers "what's actually going on in the business, sliced
however I need to see it" — the difference between a speedometer and a flight recorder.

## The reporting cube

Define `analytics.dimensions` and `analytics.measures` once — every report is then just a
measure sliced by one or more dimensions, so the business gets combinatorial reporting power
from a short list instead of a bespoke report per question:

- **Standard dimensions** (adapt to the business): Time (day/week/month/quarter), Branch/
  Location, Channel (walk-in, WhatsApp, social, referral, marketplace), Customer Segment
  (from `08-marketing-crm.md`), Staff/Agent (human or AI), Product/Service line.
- **Standard measures**: Revenue, Order/Job count, Average Order Value, Gross Margin,
  Utilization/capacity rate, Customer Acquisition Cost, Refund rate.
- Add domain-specific measures the category obviously needs (occupancy rate for a clinic,
  yield-per-bed for a farm, churn for a subscription business) — don't stop at the generic
  list.

For `analytics.reports`, name the handful (5–10) of cuts that actually matter for this
business rather than generating every possible combination — e.g. "Revenue by Branch by
Week", "Margin by Service Line", "AOV by Channel" — each with a `cadence`.

## Financial statements

Generate these directly from BIR entities so every line traces back to a real field, not a
hand-waved number — list `analytics.financialStatements` and specify the mapping:

- **Profit & Loss**: Revenue from `Order`/`Invoice` fulfilled-and-paid records; COGS from
  inventory/supply consumption if the business holds stock; Opex from payroll + recurring
  integration costs if modeled; Net margin.
- **Cash Flow**: actual cash in (payments received) vs. cash out (payroll runs, supplier
  payments) by period — different from P&L when there's a lag between invoicing and payment.
- **Balance Sheet** (only if the business/scale warrants it — usually multi-location+):
  assets (cash, inventory value, equipment) vs. liabilities (payables, loans).
- **AR/AP aging**: for any business that invoices on terms rather than collecting at point of
  sale — buckets like current/30/60/90+ days.

Note explicitly which of these come "for free" from an accounting integration
(`09-integrations-framework.md`) vs. need to be computed natively — don't duplicate a
statement QuickBooks/Xero already produces if that integration is in place; surface it instead.

## Cohort & retention analysis

Group customers by acquisition period (the month/week they first transacted) and track
repeat-purchase or retention rate over subsequent periods — this is usually the single most
useful chart for a repeat-visit business (salons, laundries, subscription SaaS) because it
separates "we're growing" from "we're leaking customers as fast as we add them." List
`analytics.cohorts` as the cohort groupings that matter (by acquisition month, by acquisition
channel, by first-service type).

## Benchmarking

Two kinds, don't conflate them:
- **Internal baseline**: WoW/MoM/YoY comparison against the business's own history — always
  available once there's data.
- **External/industry benchmark**: approximate, clearly labeled as an industry reference
  point rather than measured fact (e.g. "typical laundry gross margin: 55-65%") — useful for
  a new business with no history yet, but never present it as this business's real number.

## Anomaly detection

List `analytics.anomalyRules` — simple, explainable rules beat opaque ML for a first compile:
a measure moving more than N standard deviations from its trailing baseline, a sudden spike
in refunds/cancellations, unusual after-hours activity. Route anomalies to an automation
(`05-automations-reminders.md`) that alerts the relevant role, and to the `strategy-advisor`
agent (`04-ai-agents.md`) if it warrants investigation rather than just a glance.

## Business health score

Optionally define `analytics.healthScore`: a small weighted composite of the 3-6 KPIs that
matter most for this business (e.g. revenue growth, margin, retention, utilization), producing
one number for the Executive View (`14-business-views.md`) to lead with. Keep the weighting
visible and editable — a black-box score nobody trusts is worse than no score.

## Scheduled digests

`analytics.scheduledDigests`: recurring compiled reports pushed to an audience on a cadence
(e.g. "Monday 8am owner digest" via email or WhatsApp) rather than requiring anyone to log in
and pull reports. Reuse the reminder/automation delivery mechanism from
`05-automations-reminders.md` and `06-whatsapp-integration.md` — a digest is just an
automation whose payload is a report instead of a transactional message.

## Output format

Dimensions/measures list, reports table (id/measures/dimensions/cadence), financial
statements with their entity mapping noted, cohort definitions, benchmark notes, anomaly
rules list, health score formula (if defined), and scheduled digests table.
