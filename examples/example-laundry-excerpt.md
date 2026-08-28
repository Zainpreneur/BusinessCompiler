# Worked Example (excerpt): Multi-Branch Laundry

Input: `/business-compiler Multi-branch laundry management with inventory, pickup/delivery,
employees, accounting, CRM, automation and AI.`

This excerpt shows calibration for depth/tone across the compiler's sections — agents and
reasoning, automations, WhatsApp, analytics, views, social, marketing, knowledge, and
integrations. The full compile would also include the data model, UI/dashboards, security,
simulation, and deployment guide files, omitted here for length.

A real full compile would write these into the clustered Output Package Structure from
SKILL.md (`01-foundation/`, `02-intelligence/`, etc., with `00-index.md` at the root) — this
excerpt inlines everything in one file purely for readability here.

## BIR meta (excerpt)

```json
{
  "meta": {
    "businessName": "Fresh Fold Laundry",
    "category": "multi-branch laundry",
    "scale": "multi-location",
    "audience": "B2C",
    "assumptions": [
      "3-8 branches, each with its own bay staff and a shared delivery fleet",
      "Pickup/delivery is optional per order, not required",
      "Pricing is per-kg for wash&fold, per-item for dry cleaning"
    ]
  },
  "ontology": {
    "coreObjects": ["Customer -> Customer", "Order -> LaundryOrder", "Location -> Branch"],
    "valueFlow": "Customer pays per order (wash&fold by kg or dry-clean by item), optionally on a weekly subscription.",
    "primaryLifecycle": "Intake -> Sort/Wash/Dry/Fold -> QualityCheck -> ReadyForPickup/Delivery -> Payment"
  }
}
```

## AI Agents (excerpt)

**`whatsapp-concierge`** (specialist)
- Purpose: handles booking, rescheduling, order-status lookup, and FAQ for customers over WhatsApp.
- Triggers: inbound WhatsApp message; `LaundryOrder` status change.
- Tools: `whatsapp.send`, `LaundryOrder.read`, `Branch.read`, `booking.create`.
- Guardrails: never modifies pricing; escalates to `branch-manager` role if customer requests a refund or is upset (sentiment below threshold).
- Escalates to: `branch-manager`.

**`inventory-forecaster`** (specialist)
- Purpose: predicts detergent/supply consumption per branch from order volume and flags reorder points before stockout.
- Triggers: nightly schedule; `Supply.quantity` crossing threshold.
- Tools: `Supply.read`, `LaundryOrder.read` (7/30-day rolling), `automation.trigger('reorder-supply')`.
- Guardrails: creates a reorder *task*, does not place supplier orders autonomously above $200 without `branch-manager` approval.

**`strategy-advisor`** (advisor, reports to `ops-orchestrator`)
- Purpose: answers open-ended questions from the owner ("should we open a 4th branch?", "why did margin drop last month?") with traceable, structured recommendations.
- Reasoning patterns: `scenario-comparison` (branch expansion questions — runs the capacity/cash-flow simulators), `root-cause-5-whys` (margin/anomaly questions — pulls from `analytics.anomalyRules`), `unit-economics` (marketing spend questions).
- Tools: `analytics.query`, `financial_model`, `web_search` (local market/competitor rent and pricing), `Branch.read`.
- Memory: remembers prior recommendations for 12 months so it doesn't contradict a stance without flagging what changed.
- Guardrails: never commits to a lease or hire — output is always a recommendation with confidence and a suggested cheap experiment (e.g. "run a 2-week pop-up before signing a lease"), routed to `owner`.
- Escalates to: `owner`.

## Analytics (excerpt)

- Dimensions: Time, Branch, Channel, Segment. Measures: Revenue, Orders, AOV, Margin, Utilization.
- Report `revenue-by-branch-weekly`: measures `[Revenue, Orders]` × dimensions `[Branch, Time]`, cadence weekly.
- Financial statements generated: `profit-and-loss` (from `LaundryOrder`+`Invoice`), `ar-aging` (subscription customers on net-15 terms).
- Health score: 40% revenue growth WoW, 30% utilization rate, 20% repeat-customer rate, 10% refund rate (inverted).
- Anomaly rule: refund rate > 2 standard deviations above 8-week trailing average → alerts `branch-manager` and feeds `strategy-advisor`'s root-cause reasoning.

## Views (excerpt)

- **Executive View** (`owner`, daily digest via WhatsApp): health score, revenue-by-branch, any open anomalies — nothing else.
- **Operations View** (`branch-manager`, real-time in-app): today's order queue by status, overdue-pickup list, staff coverage gaps.
- **Field View** (`driver`, real-time mobile): today's delivery route only, one-tap "delivered" action, works offline and syncs on reconnect.

## Knowledge Base (excerpt)

- Document `service-receipt` (customer-facing, generated from `LaundryOrder`+`Invoice`).
- KB article `stain-policy-faq` grounds `whatsapp-concierge` — the agent must cite this article rather than improvise an answer when a customer disputes a stain-removal result.

## Accounting (excerpt)

- Chart of accounts (partial): `1000 Cash` (asset), `1200 A/R` (asset), `1400 Detergent Inventory` (asset), `4000 Wash Revenue` (revenue), `4100 Dry-Clean Revenue` (revenue), `2000 Supplier Payables` (liability), `5000 Payroll Expense` (expense).
- Ledger entity: `JournalEntry` — a `LaundryOrder` marked paid auto-posts `Debit 1000 Cash / Credit 4000 Wash Revenue` for the order total, referencing `LaundryOrder.id`.
- Tax: `sales-tax-ca` — 8.5% on `LaundryOrder` line items where `branch.state == 'CA'`, posts to `2100 Sales Tax Payable`.
- Close checklist: reconcile bank feed → post accrued detergent-supplier invoices not yet received → review A/R aging → lock period.

## CRM: Sales Pipeline & Support (excerpt)

- No B2B sales pipeline for individual customers; a lightweight one exists for corporate laundry contracts (hotels, gyms): `Lead -> Qualified -> Proposal Sent -> Won/Lost`.
- Ticket entity: `Ticket`, states `Open -> In Progress -> Resolved -> Closed`. SLA: first response 2h, resolution 24h for `damaged-item` tickets (routed straight to `branch-manager`, never auto-resolved by an agent).
- Customer 360 includes: order history, open tickets, loyalty tier, subscription status.

## Inventory (excerpt)

- Tracking method: `sku-quantity` for detergent/supplies. Reorder policy: "reorder to 30-day par when on-hand < 7-day average consumption."
- Purchase order `PurchaseOrder`: `Draft -> Sent -> Received -> Closed`; receiving auto-updates `Stock` and posts an A/P journal entry.

## HR & Payroll (excerpt)

- Compensation: hourly wage for bay staff, small per-order piece-rate bonus for drivers.
- Payroll cadence: biweekly. Pipeline: sum `Shift` hours + piece-rate from `LaundryOrder.driverId` → apply CA withholding → post to `5000 Payroll Expense` → disburse via Stripe payouts.

## Assets & IoT (excerpt)

- Asset types: wash-and-fold machines, dryers, delivery vans. Maintenance: dryers serviced every 90 days or 2,000 cycles, whichever first.
- IoT: vibration + temperature sensors on the 6 largest machines (branch 1 and 2 only — payback doesn't justify it at branch 3's volume yet). Predictive-maintenance agent flags a machine trending toward bearing failure and auto-creates a `MaintenanceOrder`, pulling the replacement part from `18-inventory-supply-chain.md` stock if in hand, else generating a `PurchaseOrder`.

## Platform API & Webhooks (excerpt)

- Exposed entities: `LaundryOrder` (read, create), `Customer` (read, create), `Stock` (read). Not exposed: `JournalEntry`, `Employee`.
- Auth: API keys per corporate-contract partner (hotels/gyms from the CRM pipeline), scoped to `scopes.orders-readwrite` which maps to the `branch-manager` RBAC role's permissions — a hotel partner's key can only see and create orders for its own linked branch.
- Webhook `order.ready-for-pickup`: fires on `LaundryOrder: quality-check -> ready`, payload `{orderId, branchId, readyAt}`, HMAC-signed, retried 3x with backoff.

## AI Operations (excerpt)

- `system-health-agent` (advisor): weekly report shows `whatsapp-concierge` escalating 34% of conversations to `branch-manager` — above the 20% target — traced to low confidence on reschedule requests during the two weeks a new pricing promo ran; recommends adding promo-specific FAQ content to the knowledge base rather than lowering the confidence threshold.

## QA (excerpt)

`07-delivery/qa-report.md` would flag, for example: "⚠️ Business logic: `LaundryOrder` state `quality-check` had no outgoing transition to `ready` defined in the first draft — fixed, transition added, trigger `qc-passed`." — the kind of gap Stage 4 exists to catch before the compile is called done.

## Automations (excerpt)

| ID | Trigger | Condition | Action | Owner |
|---|---|---|---|---|
| `notify-ready-for-pickup` | `LaundryOrder: quality-check -> ready` | — | `send-whatsapp` template `order-ready` | `whatsapp-concierge` |
| `overdue-pickup-escalation` | `LaundryOrder.readyAt` +48h with no pickup | `order.deliveryRequested == false` | `send-whatsapp` → if unread 24h, `notify-role(branch-manager)` | `branch-manager` |
| `low-supply-reorder` | `Supply.quantity < reorderThreshold` | — | `invoke-agent(inventory-forecaster)` | `inventory-forecaster` |

## WhatsApp templates (excerpt)

| ID | Category | Variables |
|---|---|---|
| `order-confirmed` | UTILITY | `customerName`, `orderId`, `estimatedReadyTime` |
| `order-ready` | UTILITY | `customerName`, `branchName`, `pickupOrDelivery` |
| `review-request` | UTILITY | `customerName`, `orderId` |
| `weekly-subscriber-winback` | MARKETING | `customerName`, `discountCode` (marketing-consent gated) |

## Social & Marketing (excerpt)

- Platforms: Instagram (before/after stain-removal content, local-community feel), Google
  Business Profile (review generation is disproportionately valuable for a local laundry).
- Segment `at-risk`: no order in 21–45 days, previously ≥3 orders → triggers
  `weekly-subscriber-winback` campaign via WhatsApp (consent-gated) with a discount code
  tracked back onto `LaundryOrder.promoCode` for attribution.

## Integrations (excerpt)

| Integration | Category | Direction | Entities Synced | Auth |
|---|---|---|---|---|
| Stripe | payments | bidirectional | `LaundryOrder`, `Invoice` | oauth2 |
| QuickBooks | accounting | bidirectional | `Invoice`, `Branch` (as class) | oauth2 |
| Google Maps | maps-logistics | outbound | `DeliveryRoute` | api-key |
| Google Calendar | calendar | bidirectional | `Shift` | oauth2 |

## Cross-Platform Data Aggregation (excerpt)

- External sources: Google Ads (spend + impressions, daily sync, joins to Time/Branch via `LaundryOrder.promoCode` UTM tag), corporate-partner API pushes from hotel/gym contracts (their own booking volume, weekly).
- Cross-source analysis `blended-roas`: Google Ads spend ÷ revenue from `LaundryOrder`s carrying that campaign's promo code — answers whether the spring promo actually paid for itself, not just what Google's own dashboard reported.
- Freshness note: ad spend lags a day behind native order data — the Growth View (`14-business-views.md`) shows Google Ads figures with an "as of yesterday" label rather than implying same-day.

This is the level of specificity every full compile should hit — real entity names, real
trigger conditions, real guardrail thresholds, nothing generic.
