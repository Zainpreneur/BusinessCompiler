# Advanced CRM: Sales Pipeline & Support

Compiles `crm`. `08-marketing-crm.md` covers segmentation, campaigns, and loyalty — the
marketing side of customer relationships. This section is the operational side: turning a
lead into a paying customer through a real sales process, and keeping an existing customer
supported afterward. Skip the full pipeline for a pure walk-in retail/service business with no
sales cycle (a car wash doesn't need deal stages) — though see the note below on a lighter,
lead-scoring-only middle path for a mostly-walk-in business with a genuine minority case that
still benefits from follow-up. Keep the support half for almost everyone.

## Sales pipeline

Relevant whenever a sale isn't instant — B2B, higher-ticket services, anything with a quote
or proposal step. Also relevant, in a lighter form, for a mostly-walk-in business that still
has a real minority case needing follow-up (a mostly-instant retail/service business with an
occasional large or custom order — multi-unit bookings, a bespoke request — that genuinely
benefits from a human noticing and following up). Don't force the full pipeline onto that
minority case: keep `leadScoring` signals (so the relevant lead surfaces at all) without
defining `pipelineStages`/`dealEntity` — a flagged lead with a follow-up task is enough; add
the full staged pipeline only once enough of the business's revenue actually moves through a
multi-step sales process to justify tracking stages formally. For the full pipeline, define:

- `crm.pipelineStages`: ordered stages a `Lead` or `Deal` (name `crm.dealEntity` in the BIR,
  usually `Deal` or `Opportunity`) moves through, e.g. `Lead -> Qualified -> Proposal Sent ->
  Negotiation -> Won/Lost`. This is a state machine like any entity's in
  `02-data-model-workflows.md` — give it the same `transitions` treatment, including what
  triggers each move (a human action, or an automation like "no reply in 7 days →
  auto-nurture").
- `crm.leadScoring`: signals that bump a lead's priority (requested a quote, engaged with 3+
  WhatsApp messages, matches an ideal-customer profile) — feeds a
  `next-best-action`-style specialist agent (`04-ai-agents.md`) that tells sales reps who to
  call next instead of working leads in raw creation order.
- `crm.quotaModel`: how targets are set and tracked per rep/team, surfaced on the Team/HR
  View (`14-business-views.md`) and rolled into the demand/revenue forecast
  (`11-simulation-forecasting.md`).
- Pipeline value (sum of open deals × win probability by stage) is itself a forecasting
  input — cross-reference it in the simulation section's revenue model rather than treating
  pipeline and forecast as separate things.

## Support / ticketing

Relevant for nearly every business — anyone who takes customer complaints, questions, or
issues needs at least a lightweight version of this:

- `crm.ticketEntity` (usually `Ticket`): state machine `Open -> In Progress -> Waiting on
  Customer -> Resolved -> Closed`, linked to the `Customer` and, where relevant, the
  `Order`/`Appointment` it concerns.
- `crm.supportChannels`: where tickets originate — WhatsApp (the `whatsapp-concierge` agent
  from `04-ai-agents.md` should create a ticket when it can't resolve something itself rather
  than the conversation just trailing off), email, social DMs/comments
  (`07-social-media-suite.md`'s listening layer), in-app.
- `crm.slaPolicies`: first-response and resolution targets per ticket type/priority. Breach
  risk is a reminder (`05-automations-reminders.md`) escalating to a human role before the SLA
  is actually missed, not after.
- Route negative/urgent tickets to a human by default — this is the same conservative
  guardrail as social-media negative-mention handling in `07-social-media-suite.md`; don't let
  an AI agent auto-close or auto-resolve a complaint.

## Customer 360

Define `crm.customer360Includes`: the single aggregate view of one customer pulling together
every entity that touches them — order/appointment history, open and past tickets, deal
history if applicable, marketing segment and campaign engagement (`08-marketing-crm.md`),
loyalty status, lifetime value. This is what a support rep or account manager should see the
instant they open a customer record — not five separate screens. It's a natural fit for the
Customer/CRM View in `14-business-views.md`; cross-reference rather than redefine.

## Output format

Pipeline stages with transition triggers (if applicable), lead-scoring signals, ticket state
machine, SLA table (ticket type/first response/resolution), support channel list, and the
customer-360 field list.
