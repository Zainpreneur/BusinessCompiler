# Actions, Automations & Reminders

The automation engine is the business's nervous system: event → condition → action, plus a
dedicated reminders/scheduling layer for anything time-based. AI agents (previous section)
are for judgment calls; automations are for deterministic "always do X when Y" rules — use
an automation instead of an agent whenever the rule is simple and deterministic, it's cheaper,
more predictable, and easier to audit.

## Automation rules

Each automation compiles to the BIR `automation` shape:

- `trigger.event` + `trigger.entity`: reuse a state transition or field-change from the data
  model's state machines wherever possible (e.g. `Appointment: booked -> confirmed`), so the
  automation catalog and the data model never drift apart.
- `condition`: a plain expression over entity fields (e.g. `order.total > 200 && customer.tier == 'new'`). Omit if unconditional.
- `action`: typed (`send-whatsapp`, `send-email`, `send-sms`, `create-task`, `update-entity`,
  `call-webhook`, `notify-role`, `invoke-agent`) with concrete `params`.
- `owner`: which role or agent monitors/can disable this automation.

### Automations to consider by lifecycle stage (compile what fits)

- **Acquisition**: new lead → auto-assign to sales role / CRM segment; abandoned booking →
  reminder to complete.
- **Fulfillment**: status change → notify customer; overdue job (in a status too long) →
  alert the responsible role; low stock on a required item → reorder task.
- **Billing**: invoice created → send; payment overdue → dunning sequence (escalating: email →
  WhatsApp → phone-call task for a human); payment received → receipt + thank-you.
- **Retention**: N days since last visit with no repeat booking → win-back campaign trigger
  (hands off to `08-marketing-crm.md`); milestone (10th visit, 1-year anniversary) → loyalty
  reward.
- **Internal ops**: shift starts with no staff confirmed → alert manager; a required
  compliance log not filed by end of day → escalate.

## Reminders & scheduling

Reminders are automations specialized around time offsets from an entity's timestamp, using
the BIR `reminderRule` shape (`entity`, `offset`, `channel`, `escalation`).

- Offsets can be relative (`-2h` before an appointment) or recurring (`RRULE:FREQ=WEEKLY` for
  a recurring service).
- Always define an `escalation` chain for anything the business depends on being acknowledged
  (a missed pickup reminder should escalate from WhatsApp → SMS → a human call task, not just
  fire once into the void).
- Default reminder set to consider for any business with appointments/orders: pre-visit
  reminder, day-of reminder, post-visit follow-up/review request, renewal/re-order reminder.
- Respect quiet hours and the customer's channel preference/consent — never schedule outbound
  messages outside a sane local-time window (default 8am–8pm unless told otherwise).

## Anti-spam / stacking rule

Before finalizing the automation + reminder list, check for a customer receiving multiple
messages for the same event from different rules (an automation *and* a reminder *and* an
agent all firing on the same booking). Consolidate into one message with the richest content,
or explicitly sequence them with enough gap to not feel like spam.

## Output format

A table: ID | Trigger | Condition | Action | Owner, split into "Automations" and "Reminders"
subsections. Note any escalation chains inline or in a short follow-up list.
