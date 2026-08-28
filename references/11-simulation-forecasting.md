# Simulation & Forecasting

Compiles `simulation`: models that let the business ask "what if" before committing money or
staffing, built directly on the data model's entities so forecasts are traceable to real
fields, not black-box numbers.

## Models to consider (pick what fits; name the inputs/outputs concretely)

- **Demand forecast**: predicts order/appointment volume by period (day/week/season) from
  historical `Order`/`Appointment` records, seasonality, and marketing campaign calendar
  overlay from `08-marketing-crm.md`. Output: expected volume ± confidence band per period.
- **Staffing/capacity simulator**: given the demand forecast and known service duration per
  job, computes required staff-hours vs. currently scheduled shifts — flags under/over-
  staffing windows. Feeds the `shift-scheduling optimizer` agent if one exists.
- **Cash flow forecast**: projects inflow (expected payments from open `Invoice`s +
  forecasted new orders) against known outflow (payroll, recurring supplier costs, loan
  payments if modeled) on a weekly/monthly grid — flags projected negative-balance weeks
  early enough to act.
- **Inventory/stock simulator**: for businesses holding stock, projects stockouts from
  current levels, reorder lead time, and demand forecast — feeds the `inventory-reorder`
  automation's threshold.
- **Pricing/scenario simulator**: models revenue/margin impact of a price change or a new
  service package before launching it, using current mix and price elasticity assumptions
  (state the assumption explicitly — this is inherently approximate).
- **Churn/LTV projection**: expected customer lifetime value and churn probability by
  segment (from `08-marketing-crm.md` segments), useful for justifying acquisition spend.

## What-if scenarios

Define a few named `scenarios` the owner can run without needing a data scientist, e.g. "what
if we open a second branch", "what if we raise prices 10%", "what if we add a delivery
service" — each scenario names which model(s) it perturbs and which inputs change.

## Calibration and honesty

- State the minimum historical data needed before a forecast is trustworthy (e.g. "demand
  forecasting needs ~8 weeks of order history; before that, show industry-benchmark defaults
  clearly labeled as such, not as if they were derived from this business's real data").
- Every simulated output should show its confidence/uncertainty, not a bare point estimate —
  a founder acting on a forecast needs to know how much to trust it.

## Output format

One subsection per model: Inputs / Method (plain description, not code) / Output shown on
which dashboard tile (link back to `03-ui-dashboards.md`) / Data requirement before it's
trustworthy. Then the named what-if scenarios list.
