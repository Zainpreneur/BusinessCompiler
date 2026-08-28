# Integrations Framework ("connect to any platform")

Compiles `integrations`: a generic connector pattern so the business can plug into whatever
third-party platforms it already uses or will want later, without every integration being
bespoke.

## The connector pattern

Every integration, regardless of platform, compiles to the same BIR `integration` shape —
this uniformity is the point, it's what makes "any platform" tractable:

- `category`: payments / accounting / ecommerce / calendar / maps-logistics /
  communications / storage / analytics / custom-webhook.
- `direction`: inbound (platform → business data), outbound (business → platform), or
  bidirectional.
- `entitiesSynced`: which BIR entities map to which objects on the other platform (e.g.
  `Customer <-> QuickBooks Customer`, `Order <-> Shopify Order`).
- `authType`: oauth2 / api-key / webhook-secret / basic.

## Standard integration set (compile what fits the business; this is the "any platform" menu)

- **Payments**: Stripe / Square / PayPal / regional processor (e.g. Razorpay, Paystack) —
  outbound charge creation, inbound webhook for payment status → drives the `Order`/`Invoice`
  state machine directly (link to the transitions defined in `02-data-model-workflows.md`).
- **Accounting**: QuickBooks / Xero / Wave — bidirectional sync of invoices, expenses,
  customers; typically nightly batch or on-invoice-created webhook. This syncs an *external*
  accounting product; if the business instead runs its books natively inside the compiled
  system, see `16-accounting-finance.md`'s chart of accounts and ledger — the two are
  alternatives, not both at once, unless the native ledger is deliberately mirrored out to an
  external tool for a bookkeeper's convenience.
- **E-commerce/POS**: Shopify / WooCommerce / Square POS / Toast — for any business that also
  sells online or has a physical POS, sync products/orders/inventory bidirectionally.
- **Calendar**: Google Calendar / Outlook — bidirectional sync of `Appointment` so staff see
  bookings in their normal calendar and external calendar blocks (vacation, personal events)
  block availability in the compiled system.
- **Maps/logistics**: Google Maps/Distance Matrix for delivery/route agents; a
  delivery-fleet API (e.g. Onfleet, or a courier's API) if the business does delivery.
- **Communications**: email (SendGrid/Postmark/SES), SMS (Twilio), on top of the WhatsApp
  section already covered separately.
- **Storage/docs**: Google Drive / Dropbox for document-heavy workflows (contracts, compliance
  logs, media assets for the social suite).
- **Analytics**: Google Analytics / Meta Pixel for attributing the marketing funnel's web-
  facing stages.
- **IoT/telemetry**: sensor platforms or an MQTT broker feeding equipment signal data —
  inbound, usually real-time or high-frequency polling; see `21-assets-equipment-iot.md` for
  what to do with the data once it's flowing (preventive/predictive maintenance) and
  `23-cross-platform-data-aggregation.md` for folding telemetry trends into analytics.
- **Custom webhook**: for anything not covered above, a generic inbound/outbound webhook
  contract (payload schema keyed to a BIR entity, HMAC-signed) so a business-specific or
  future platform can be wired in without redesigning the framework — always include at least
  one of these as a documented escape hatch.

## Sync and failure handling

For each integration, note:

- **Sync direction and cadence** (real-time webhook vs. polling vs. nightly batch).
- **Conflict resolution** when the same entity is edited on both sides (default: most-recent-
  write-wins per field, with a human-reviewable log for financial data — don't silently
  auto-resolve payment/accounting conflicts).
- **Failure/retry behavior**: exponential backoff, dead-letter logging, and which role gets
  alerted on repeated failure (this is itself an automation from `05-automations-reminders.md`
  — reuse that pattern rather than inventing a separate one here).

## Output format

A table: Integration | Category | Direction | Entities Synced | Auth, grouped by category,
followed by a short note on sync cadence and failure handling per integration where it's
non-default.
