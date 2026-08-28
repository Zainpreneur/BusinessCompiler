# Marketing

Compiles `marketing` in the BIR: segmentation, funnels, campaigns, lifecycle messaging, paid
advertising, and loyalty — the layer that turns one-time customers into repeat ones and
connects WhatsApp/social activity to revenue. The sales-pipeline and support side of customer
relationships (deals, tickets, SLAs, customer-360) has its own file — see
`17-crm-sales-support.md`.

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

## Lifecycle drip sequences

Beyond one-shot campaigns, define `marketing.dripSequences` for anything that plays out over
multiple touches rather than a single message: a multi-day welcome series for new customers, a
nurture sequence for a lead that hasn't converted, a re-engagement sequence for an at-risk
segment that escalates channel/urgency across steps (email → WhatsApp → a discount offer) if
earlier steps go unopened. Each sequence: `trigger` (what enrolls a customer — a segment
transition, a lead-capture event) and ordered `steps` (message + wait period). Stop a sequence
immediately if the customer converts or replies — a drip that keeps firing after its purpose is
served is the fastest way to make a business's marketing feel spammy.

## Paid advertising

If the business runs or should run paid ads, define `marketing.adCampaigns`: platform
(Google/Meta/TikTok ads, matched to where `07-social-media-suite.md` already has organic
presence), objective (awareness/leads/conversions), `targetSegment` (reuse `segments`, don't
invent a separate ad-audience definition), and budget model. Tie ad spend to the same
attribution mechanism below so ROAS (return on ad spend) is a real computed number in
`13-analytics-and-reporting.md`, not a platform-reported vanity metric taken on faith.

## A/B testing

For campaigns, ad creative, or WhatsApp/email copy where the business has enough volume to
get a meaningful read, define `marketing.abTests`: a hypothesis, the variants being compared,
and the single metric that decides a winner. Don't run more simultaneous tests on the same
segment than the business has volume to reach significance on — for a low-volume local
business, prefer sequential testing over parallel A/B/C/D splits that never reach significance.

## Attribution

Explicitly connect marketing spend/effort to revenue: every campaign, ad, and social post
should be attributable via a promo code, UTM tag, or WhatsApp broadcast tag stored on the
`Order`/`Appointment` entity, so the KPI dashboard (`03-ui-dashboards.md`) can show "revenue
by channel" honestly instead of guessing. Set `marketing.attributionModel` explicitly —
`last-touch` is simplest and fine for a business with a short, single-channel path to
purchase; move to `linear-multi-touch` or `position-based` once a customer typically
encounters several channels (a social post, then a WhatsApp reminder, then a referral) before
converting, since last-touch alone would over-credit whichever channel happened to close it.

## Output format

Segments table, funnel stage list, campaigns table (segment/channel/trigger/offer), drip
sequences (trigger/steps), paid ad campaigns table (platform/objective/segment/budget), A/B
tests list, loyalty and referral structure, and the attribution model with a short note on why
it fits this business.
