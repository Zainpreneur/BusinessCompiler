# AI Agents

This is the section most likely to get generic if you're not careful ("an AI agent that helps
with customer service") — fight that. Every agent should be scoped to real BIR entities, real
tools, and a real trigger, with an explicit human it escalates to.

## Agent hierarchy

Organize as a small org chart, not a flat list:

- **Orchestrator agent** (`tier: orchestrator`) — one per business, e.g. `ops-orchestrator`.
  Owns understanding the day's state across the business and routing work to specialists. Not
  strictly required for a solo/small-team business — skip it if there's only 1–2 specialist
  agents total and add it back once the business scales past ~4 agents.
- **Specialist agents** (`tier: specialist`) — own a domain end to end (e.g.
  `inventory-forecaster`, `whatsapp-concierge`, `collections-agent`, `scheduling-agent`,
  `review-response-agent`, `intake-triage-agent`). Most of the exhaustive value lives here —
  see the catalog below.
- **Task agents** (`tier: task`) — narrow, single-purpose, usually invoked by a specialist or
  an automation rather than standing on their own (e.g. `receipt-ocr-agent`,
  `sentiment-classifier`).

For each agent, fill the BIR `aiAgent` shape:

- `purpose`: one sentence, specific to this business's domain terms.
- `tools`: concrete — name the systems/APIs it calls (e.g. `["calendar.read", "whatsapp.send", "Inventory.update"]`), not "various tools."
- `triggers`: what wakes it up — an entity state transition, a schedule, an inbound message, another agent's handoff.
- `entitiesTouched`: BIR entity ids it reads/writes.
- `guardrails`: what it must never do autonomously (e.g. "never issues a refund over $50 without `branch-manager` approval", "never messages a customer who has opted out").
- `escalatesTo`: the human role that gets pulled in when the agent is unsure or guardrails block it.

## Catalog of AI feature domains to consider (pick what fits the business, don't force all)

Draw the agent roster from whichever of these are relevant — most real businesses end up with
5–12 agents/features across these domains:

- **Front-of-house / conversational**: intake triage, appointment booking assistant, FAQ/
  knowledge-base answering, multilingual support, WhatsApp/chat concierge (see
  `06-whatsapp-integration.md`).
- **Operations**: demand/staffing forecaster, route/dispatch optimizer, inventory reorder
  predictor, quality-control anomaly detector (e.g. flagging unusual service times).
- **Finance**: invoice/receipt OCR and reconciliation, collections/dunning agent, fraud/
  anomaly flagging, pricing/discount recommendation.
- **CRM & retention**: churn-risk scorer, next-best-action recommender, review-response
  drafting, personalized upsell suggestions.
- **Marketing**: content-generation agent for social posts/campaigns (feeds
  `07-social-media-suite.md` / `08-marketing-crm.md`), ad-spend optimizer, A/B test analyzer.
- **HR/staffing** (if the business has employees): shift-scheduling optimizer, onboarding
  assistant, performance-summary generator.
- **Knowledge & reporting**: natural-language business-question answering over the data model
  ("how did branch 2 do last week"), automated weekly/monthly report generation.
- **Compliance/safety** (domain-dependent — health, food, childcare, finance): document/log
  completeness checker, regulatory-deadline tracker.

## Guardrails as a first-class concept

Every agent needs at least one guardrail beyond "be helpful." Common patterns to reuse:

- Spend/refund/discount ceilings requiring human approval above a threshold.
- Opt-out and consent respect (never contact a customer who has withdrawn consent — cross-
  reference `whatsapp.consentEntity`).
- Confidence thresholds: below X, hand off to a human rather than guess (critical for
  anything touching health, legal, or payment data).
- Rate limits on outbound customer contact per agent, to avoid spammy automation stacking (an
  agent and an automation both messaging the same customer the same day).

## Output format

Markdown org-chart-style: orchestrator first (if present), then specialists grouped by
domain, then task agents. For each, a compact block: Purpose / Triggers / Tools / Touches /
Guardrails / Escalates to. Close with a short "why this roster" paragraph tying the agent
count and mix back to `meta.scale`.
