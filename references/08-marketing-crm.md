# Marketing & CRM

Compiles `marketing` in the BIR: segmentation, funnels, campaigns, lifecycle messaging, and
loyalty — the layer that turns one-time customers into repeat ones and connects WhatsApp/
social activity to revenue.

## Segmentation

Define `segments` from real BIR fields, not vague labels: e.g. "New (0 orders)", "Active
(order in last 30d)", "At-risk (no order in 45–90d, previously active)", "Lapsed (>90d)",
"VIP (top 10% lifetime value)", "B2B accounts" if `meta.audience` includes B2B. Each segment
should be expressible as a filter over `Customer`/`Order` fields so it's actually computable,
not just descriptive.

## Funnels

`funnels`: name the stages relevant to this business's acquisition path (e.g. Awareness →
Lead → Trial/First booking → Repeat customer → Advocate). For each stage, note the primary
channel driving it (social content, WhatsApp broadcast, referral, paid ads, walk-in) and the
metric that marks progression — this is what social media analytics and the simulation
section's forecasts hook into.

## Campaigns

For each `campaigns` entry, specify: target segment, channel (email/SMS/WhatsApp/social —
respecting the consent rules from `06-whatsapp-integration.md`), trigger (scheduled/one-off
vs. lifecycle-triggered off a segment transition), and the offer/content angle. Cover at
least these lifecycle-triggered campaigns where relevant to the business:

- Welcome/first-purchase nudge
- Post-purchase review request (coordinate with the WhatsApp review-request template — don't
  duplicate across channels)
- Win-back for "at-risk"/"lapsed" segments
- VIP/loyalty recognition
- Seasonal/promotional pushes tied to the business's actual seasonality (a nursery has
  spring/holiday peaks; a laundry may not)

## Loyalty

If the business benefits from repeat visits (most do), define a `loyalty` structure: points-
per-spend or visit-based tiers, redemption rules, and how it's surfaced (WhatsApp balance
check, dashboard tile, receipt line). Keep it simple for solo/small-team businesses (a punch-
card equivalent) and only add tiering complexity for larger/franchise scale.

## Referral

Consider a lightweight referral mechanic (referral code on `Customer`, reward on the
referred customer's first purchase) — cheap to spec, high-value for most local/service
businesses; skip only if clearly not applicable (e.g. pure B2B with long sales cycles where
it doesn't fit).

## Attribution

Explicitly connect marketing spend/effort to revenue: every campaign and social post should
be attributable via a promo code, UTM tag, or WhatsApp broadcast tag stored on the `Order`/
`Appointment` entity, so the KPI dashboard (`03-ui-dashboards.md`) can show
"revenue by channel" honestly instead of guessing.

## Output format

Segments table, funnel stage list, campaigns table (segment/channel/trigger/offer), loyalty
and referral structure, and a short attribution note.
