# Worked Example (excerpt): Multi-Branch Laundry

Input: `/business-compiler Multi-branch laundry management with inventory, pickup/delivery,
employees, accounting, CRM, automation and AI.`

This excerpt shows calibration for depth/tone on the newer sections (agents, automations,
WhatsApp, social, marketing, integrations). The full compile would also include the data
model, UI/dashboards, security, simulation, and deployment guide files, omitted here for
length.

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

This is the level of specificity every full compile should hit — real entity names, real
trigger conditions, real guardrail thresholds, nothing generic.
