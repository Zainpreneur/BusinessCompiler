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
- **Advisor agents** (`tier: advisor`) — do multi-step business *reasoning* rather than
  executing transactional work: a `strategy-advisor` that answers open-ended questions
  ("should we open a second location?"), synthesizes analytics with market context, and
  produces structured recommendations. See "The Business Reasoning Layer" below — this tier
  is what separates a compiler that automates tasks from one that actually reasons about the
  business.
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
  knowledge-base answering, multilingual support (translate outbound messages and understand
  inbound ones in the customer's language rather than assuming everyone types in the
  business's default one), WhatsApp/chat concierge (see `06-whatsapp-integration.md`), and a
  **voice agent** for businesses that still take phone calls — answers or triages inbound
  calls, transcribes and summarizes them onto the relevant entity (an `Appointment` note, a
  `Ticket`), and can place outbound calls for anything that genuinely needs a voice (a missed
  high-value delivery, an overdue-payment call escalated from `whatsapp-concierge`). Treat
  phone as one more channel into the same customer conversation history as WhatsApp/chat, not
  a separate silo — a customer who called yesterday and messages today shouldn't have to
  repeat themselves.
- **Operations**: demand/staffing forecaster, route/dispatch optimizer, inventory reorder
  predictor, quality-control anomaly detector (e.g. flagging unusual service times), and — for
  any business with tracked equipment — a **predictive-maintenance agent** watching asset
  telemetry to catch failures before they happen (see `21-assets-equipment-iot.md`).
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

Every agent needs at least one guardrail beyond "be helpful." Write the actual number at the
point you write the guardrail — don't write "escalates below a confidence threshold" and plan
to fill in the number later, or during a QA pass; write "escalates below 70% confidence" the
first time, every time. A guardrail that names a threshold without a value isn't a weaker
version of a real guardrail, it's not a guardrail yet — nothing can be checked or enforced
against "a threshold." Common patterns to reuse, each shown with the concreteness they need:

- Spend/refund/discount ceilings requiring human approval above a threshold — e.g. "auto-
  approves refunds up to $50; anything above requires `branch-manager` sign-off," not "requires
  approval above a threshold."
- Opt-out and consent respect (never contact a customer who has withdrawn consent — cross-
  reference `whatsapp.consentEntity`).
- Confidence thresholds — e.g. "hands off to a human below 70% confidence, or immediately
  regardless of confidence when the question touches health, legal, or payment data" — critical
  for anything touching those domains.
- Rate limits on outbound customer contact per agent, to avoid spammy automation stacking — e.g.
  "at most 1 proactive message per customer per 24h across all agents/automations," not just
  "avoid over-messaging" (an agent and an automation both messaging the same customer the same
  day is exactly the failure this needs a real number to prevent).

## The Business Reasoning Layer

Task and specialist agents execute; this layer is about *judgment* — the difference between
"send the reminder" and "figure out whether we should hire another technician." Every compile
with `meta.scale` beyond solo should include at least one advisor agent, typically
`strategy-advisor`, reporting to the orchestrator if one exists.

**What an advisor agent does that a specialist doesn't:**
- Answers open-ended natural-language business questions by pulling from the BIR, the
  analytics layer (`13-analytics-and-reporting.md`), the simulation models
  (`11-simulation-forecasting.md`), and — via the `web_search`/`market_research` tools below —
  external context the business's own data can't provide (competitor pricing, local market
  conditions, industry trends).
- Produces a **structured recommendation**, not just an answer: the question restated, the
  reasoning pattern used, the data it drew on, the recommendation, a confidence level, and the
  concrete next step. A bare opinion isn't useful to a founder deciding whether to spend money;
  a traceable one is.
- Still respects guardrails: an advisor recommends, it doesn't unilaterally execute anything
  irreversible (opening a branch, changing prices, firing staff) — that's always handed to
  `escalatesTo`.

### Reasoning patterns (`aiAgent.reasoningPatterns`)

Name the structured frameworks an advisor (or a specialist making a non-trivial judgment call)
applies, so its reasoning is reproducible rather than ad hoc. Reuse these standard patterns
rather than inventing new ones per business:

- **`unit-economics`** — CAC vs. LTV, contribution margin per order/customer; the default
  lens for "should we spend more on X" questions.
- **`scenario-comparison`** — run 2+ named scenarios through the simulation models
  (`11-simulation-forecasting.md`) and compare outcomes side by side rather than answering
  from intuition alone.
- **`root-cause-5-whys`** — for "why did X happen" questions (a bad week, a spike in
  refunds), chain from the symptom to the underlying cause using the analytics/anomaly data
  before recommending a fix.
- **`swot`** — for genuinely open strategic questions (new market, new service line) where
  there isn't yet enough of the business's own data to run a quantitative scenario.
- **`decision-matrix`** — when comparing 3+ discrete options (which POS system, which branch
  location) against weighted criteria.

Each reasoning pattern should end in a recommendation with a stated confidence and, where the
decision is reversible and cheap to test, a suggested small experiment before committing fully
— advisors should default to "here's a cheap way to find out" over "here's my best guess," when
one exists.

## Standard tool vocabulary

Keep agent `tools` lists concrete and drawn from a shared vocabulary rather than each agent
inventing its own naming — this makes the agent roster auditable at a glance and maps cleanly
onto real implementation (Claude Agent SDK tool definitions, MCP connectors already available
in this environment, or custom functions). Reuse these names:

| Tool | Purpose |
|---|---|
| `<Entity>.read` / `<Entity>.update` / `<Entity>.create` | Direct BIR entity access, scoped per agent |
| `web_search` | External/market research — competitor info, industry benchmarks, local conditions |
| `financial_model` | Runs the simulation models from `11-simulation-forecasting.md` with given inputs |
| `analytics.query` | Ad-hoc cube query against `13-analytics-and-reporting.md`'s dimensions/measures |
| `document_generator` | Renders a document from a template + entity data (`15-knowledge-and-documents.md`) |
| `knowledge_base.search` | Retrieves grounding articles before answering a policy/FAQ question |
| `whatsapp.send` / `email.send` / `sms.send` | Outbound messaging on a specific channel |
| `automation.trigger` | Fires a named automation from `05-automations-reminders.md` |
| `notify_role` | Escalates/alerts a human role without taking further action |
| `calendar.read` / `calendar.write` | Scheduling, via the calendar integration |
| `<integration>.sync` | Named third-party sync from `09-integrations-framework.md` |
| `voice.call` / `voice.transcribe` | Place/receive a phone call, or transcribe+summarize one onto an entity |
| `iot.read_telemetry` | Reads sensor signals for an `Asset` from `21-assets-equipment-iot.md`'s IoT integration |
| `agent_metrics.read` | Reads another agent's/automation's run history — used only by the system-health agent below |

Add a business-specific tool only when none of the above fits — and when you do, keep the same
`noun.verb` naming convention.

## Memory

Most task/specialist agents should be stateless (each invocation is self-contained) — it's
simpler and easier to audit. Set `aiAgent.memory` only where statefulness genuinely earns its
keep: a concierge agent remembering a customer's conversation history within a support window,
or the `strategy-advisor` remembering past recommendations so it doesn't contradict itself
quarter to quarter. State what's remembered and for how long — unbounded, undefined memory is
a privacy and drift risk, not a feature.

## AI Operations: the system-health agent

An AI workforce that nobody watches degrades silently — an agent's confidence threshold drifts
out of calibration, an automation starts double-firing, guardrail escalations spike because a
threshold was set wrong at compile time. Rather than leaving that to be discovered by an
angry customer, compile a `system-health-agent` (tier: `advisor`, reports to the
orchestrator if one exists) for any business with more than a handful of agents/automations
(roughly: worth adding once the roster passes ~4-5 agents).

It doesn't touch customers or transactional entities at all — its only inputs are the AI
workforce's own operational data: agent escalation rates (an agent escalating on 60% of
invocations is either miscalibrated or doing a job that shouldn't be autonomous yet),
automation failure/retry rates, how often each anomaly rule from
`13-analytics-and-reporting.md` fires (a rule that never fires might be miscalibrated too
loose; one that fires constantly has become noise everyone ignores), and whether the
anti-spam/stacking rule from `05-automations-reminders.md` is actually holding (are customers
getting multiple messages for one event despite the rule saying they shouldn't).

Output: a recurring **AI system health report** (weekly is a reasonable default cadence) —
surfaced on the Executive View (`14-business-views.md`) — naming what's healthy, what's
drifting, and a concrete suggested fix per issue (raise/lower a specific threshold, retire an
agent nobody's escalations justify, fix a stacking automation). It recommends, it doesn't
self-modify — like any advisor, tuning an agent's guardrails is a human decision, routed to
`escalatesTo`, not something it does to itself.

This is also the mechanism that keeps the QA pass in `22-qa-and-completeness.md` honest over
time: that pass checks the compile is logically sound *at compile time*; the system-health
agent is what catches logic that was sound at compile time but has drifted since, once the
system has been running against real data.

## Output format

Markdown org-chart-style: orchestrator first (if present), then advisor agents, then
specialists grouped by domain, then task agents. For each, a compact block: Purpose /
Triggers / Tools / Reasoning patterns (advisors only) / Touches / Guardrails / Memory (if any)
/ Escalates to. Close with a short "why this roster" paragraph tying the agent count and mix
back to `meta.scale`.
