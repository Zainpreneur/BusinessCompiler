# Social Media Suite

Compiles `socialMedia` in the BIR: a real content operation, not just "post on social media."

## Platform selection

Pick platforms based on the audience (`meta.audience`) and category, don't default to "all of
them":

- **B2C, visual/local business** (salon, restaurant, nursery, car wash): Instagram, Facebook,
  TikTok, Google Business Profile (technically not "social" but belongs here operationally —
  reviews and posts).
- **B2B / professional services**: LinkedIn first, X/Twitter secondary, YouTube for
  demos/case studies.
- **Marketplace/community-driven**: add Reddit/community-specific channels, Pinterest for
  visually-browsable catalogs.

List chosen platforms in `socialMedia.platforms` with a one-line reason each.

## Content pillars & cadence

Define `contentPillars` (3–5 recurring themes, domain-specific — e.g. for a plant nursery:
"plant care tips", "customer transformations/before-after", "new stock drops", "behind the
scenes", "seasonal promotions") and a `postingCadence` per platform (e.g. Instagram 4x/week,
LinkedIn 2x/week). Tie pillars back to the marketing funnel stages in
`08-marketing-crm.md` where relevant (top-of-funnel awareness content vs. conversion-driving
promo content).

## Publishing pipeline

- **Content calendar**: entity-backed (add a lightweight `SocialPost` entity to the BIR if not
  already present: `platform`, `pillar`, `scheduledFor`, `status`, `assetRefs`, `caption`).
- **Generation**: the marketing content-generation agent (from `04-ai-agents.md`) drafts
  captions/copy from templates per pillar; a human role approves before publish by default —
  only make it fully autonomous for low-risk, high-cadence content (e.g. daily
  "we're open" story) once the business explicitly wants that.
- **Cross-posting**: define which content is platform-native (shot for TikTok/Reels) vs.
  safely repurposed across platforms, so the pipeline doesn't recommend blind cross-posting
  everywhere.
- **Automation hooks**: reuse `05-automations-reminders.md` patterns — e.g. a 5-star review
  automatically queues a "customer love" post draft for approval; new inventory arrival
  triggers a "just dropped" post draft.

## Listening & engagement

- `listeningKeywords`: business name, common misspellings, key product/service terms, and
  competitor names if relevant — for a `review-response-agent` (or a dedicated
  `social-listening-agent`) to monitor mentions and comments.
- Response guardrails: auto-respond to simple/positive mentions (thanks, FAQ-style
  questions); escalate negative mentions or complaints to a human role immediately rather than
  auto-responding — reputational risk means this is one place autonomy should be conservative
  by default.

## Analytics

Minimum KPI set to add to the BIR `kpis` if not already covered: engagement rate per
platform, follower growth, click-through to booking/site, social-attributed
bookings/revenue (requires a UTM or promo-code tie-back into the `Order`/`Appointment`
entity — specify that link explicitly).

## Output format

Platforms table (platform/reason/cadence), pillars list, publishing pipeline description,
listening/engagement rules, analytics KPI table.
