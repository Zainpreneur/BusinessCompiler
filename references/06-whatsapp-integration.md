# WhatsApp Integration

Compiles `whatsapp` in the BIR: how this business uses WhatsApp Business as a real channel,
not just "send a WhatsApp message" hand-waving.

## Platform basics to specify concretely

- **API tier**: WhatsApp Business Platform (Cloud API) directly, or via a BSP (Business
  Solution Provider — e.g. Twilio, 360dialog, MessageBird, Meta's own onboarding). Default to
  recommending the Cloud API direct for cost-sensitive/simple setups and a BSP when the
  business already uses that provider for SMS/other channels or needs multi-agent shared
  inbox tooling.
- **Sender identity**: business display name, category (must match Meta's business
  verification categories), and profile (about text, address, hours).
- **Number**: a dedicated number, ported or new — not a founder's personal number.

## Message templates (`whatsapp.templates`)

WhatsApp requires pre-approved templates for any business-initiated message outside a 24-hour
customer service window. For each template define: `id`, `category` (UTILITY, MARKETING, or
AUTHENTICATION per Meta's classification — this affects approval and cost), and `variables`.
Cover at minimum, for any business with a booking/order lifecycle:

- Booking/order confirmation (UTILITY)
- Reminder before fulfillment (UTILITY) — reuse the `reminderRule` from
  `05-automations-reminders.md` that fires it
- Status update / ready-for-pickup (UTILITY)
- Payment/receipt (UTILITY)
- Review request post-fulfillment (UTILITY, sent once, respecting opt-out)
- Win-back / promotional (MARKETING) — must respect explicit marketing opt-in, separate from
  transactional consent
- OTP/verification, if the business needs identity verification (AUTHENTICATION)

## Conversational flows (`whatsapp.flows`)

Beyond one-shot templates, define the actual back-and-forth flows the `whatsapp-concierge`
agent (see `04-ai-agents.md`) handles inside the 24-hour session window:

- Book/reschedule/cancel via chat (map each user intent to the workflow it invokes from
  `02-data-model-workflows.md`).
- FAQ answering grounded in the business's actual policies (hours, pricing, location).
- Order status lookup by reference number.
- Human handoff: a clear trigger (customer asks for a person, or agent confidence is low)
  that routes to a real role's inbox, per the agent's `escalatesTo`.
- Use WhatsApp Flows (structured forms inside chat) for anything better as a form than free
  text — e.g. picking a service package, choosing a time slot.

## Consent & compliance

- Name the BIR entity holding consent state (`whatsapp.consentEntity`, usually a field on
  `Customer`) — separate **transactional** consent (implied by doing business) from
  **marketing** consent (opt-in required, and must support one-tap opt-out, e.g. replying
  "STOP").
- Respect Meta's messaging window and template rules — never assume free-form messaging is
  always available.
- Log every outbound template send against the entity/workflow that triggered it, so support
  can trace "why did the customer get this."

## Output format

A short platform-setup block, then the templates table (id/category/variables/triggering
reminder-or-workflow), then the flows list (intent → workflow → handoff condition).
