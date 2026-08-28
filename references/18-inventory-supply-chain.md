# Inventory & Supply Chain

Compiles `inventory`. Added as an "other module upgrade" — any business that holds physical
stock (retail, food, medical supplies, nursery plants, laundry detergent) has been touched
only lightly so far (an `inventory-forecaster` agent, a generic `Supply` entity mention).
Businesses with no physical inventory (pure services, SaaS) should skip this file entirely —
say so explicitly in the compiled output rather than forcing a warehouse model onto them.

## Stock tracking

Set `inventory.trackingMethod` based on what the business actually needs, not the most
sophisticated option available:

- `none` — genuinely no inventory to track (most pure-service businesses).
- `sku-quantity` — track a running quantity per SKU/item, no per-unit identity (most retail,
  supplies, ingredients). The common case.
- `lot-batch` — track by batch/lot with an expiry or production date (food, cosmetics,
  anything perishable or recall-relevant).
- `serial-unit` — track individual serialized units (equipment, high-value items, anything
  under individual warranty).

## Warehouses/locations

`inventory.warehouses`: name each stock-holding location — for a multi-branch business this
is usually one per branch plus optionally a central warehouse. Add `Stock` as a BIR entity
(`02-data-model-workflows.md`) relating `Item`/`Supply` × `Warehouse` → `quantity`, so stock
levels are always location-specific, not one global number that hides a branch actually being
out while another is overstocked.

## Purchasing

`inventory.purchaseOrderEntity` (usually `PurchaseOrder`): state machine `Draft -> Sent ->
Partially Received -> Received -> Closed`, linked to a supplier and line items. Purchase
orders are how the `inventory-forecaster` agent's reorder recommendations
(`04-ai-agents.md`) actually become action — the agent creates a draft PO, a human approves
above the guardrail threshold, and receiving a shipment auto-updates `Stock` and (if
`accounting.payrollLinked`-style auto-posting is in place) creates the corresponding accounts-
payable journal entry in `16-accounting-finance.md`.

## Suppliers

`inventory.suppliers`: id, name, and `leadTimeDays` — lead time is a direct input to the
reorder policy and the inventory simulator (`11-simulation-forecasting.md`), so don't leave it
unspecified. Track supplier reliability (on-time delivery rate) as a KPI if the business has
had recurring supply issues — it's a strong candidate for an anomaly rule
(`13-analytics-and-reporting.md`).

## Reorder policy

`inventory.reorderPolicy`: state the actual rule in plain terms (e.g. "reorder to a 30-day par
level whenever on-hand drops below 7 days of average consumption"), not just "reorder when
low" — this is what the inventory-forecaster agent and the low-stock automation
(`05-automations-reminders.md`) both implement, so it needs to be a real, computable rule.

## Stock transfers

If `inventory.stockTransfers` is true (multi-branch business where stock can move between
locations rather than only in from suppliers), define the transfer workflow: request →
approve → ship → receive, decrementing the source `Stock` and incrementing the destination
only once actually received — never decrement source and increment destination in the same
step, or a transfer that's lost/damaged in transit silently shows as delivered stock.

## Shrinkage & write-offs

Define how inventory loss (breakage, theft, expiry) is recorded — a `StockAdjustment` entity
with a reason code, always requiring the same approval guardrail as a discount/refund in
`04-ai-agents.md` if an AI agent is involved, and always posting to a `Shrinkage`/`Inventory
Write-off` expense account in `16-accounting-finance.md` rather than silently vanishing from
the books.

## Output format

Tracking method and rationale, warehouses/locations list, purchase order state machine,
suppliers table (id/name/lead time), reorder policy statement, stock transfer workflow (if
applicable), and shrinkage/write-off handling.
