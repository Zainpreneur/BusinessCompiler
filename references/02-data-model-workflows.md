# Data Model & Workflows

Compiles `entities` and `workflows` from the BIR into a concrete, buildable model.

## Data model

For each entity in the BIR, render:

1. **Fields table**: id, type, required?, notes. Include audit fields by default
   (`createdAt`, `updatedAt`, `createdBy`) — don't list them for every entity in prose, just
   note once that they're implied.
2. **Relationships**: a short diagram-in-text or list (`Appointment.customerId -> Customer`,
   `Appointment.staffId -> Staff`). Flag one-to-many vs many-to-many explicitly (e.g. a
   `ServicePackage` many-to-many with `Order` needs a join entity — name it).
3. **State machine** (if the entity has a lifecycle): states in order plus the transitions
   table (`from`, `to`, `trigger`). Mark terminal states. This state machine is what
   automations (`references/05-automations-reminders.md`) hook into — every transition is a
   potential automation trigger, so don't skip transitions that "obviously" don't need one
   (e.g. `Appointment: booked -> confirmed` still deserves a trigger id even if no automation
   uses it yet).
4. **Sensitive fields**: mark `piiOrSensitive: true` for anything like health data, payment
   details, government IDs — this feeds the security section's field-level policies.

Keep the model normalized but pragmatic — an entity that exists only to hold two fields and is
never queried independently should probably be an embedded/json field instead, not a full
entity. Match complexity to `meta.scale`: a solo operator's model should be short enough to
read in one sitting; a franchise's model can be large but should still be organized by
subdomain (Core / Inventory / Staffing / Finance / CRM) with headers.

## Workflows

A workflow is an executable sequence, not a diagram for its own sake. For each workflow:

- **Trigger**: what starts it (a UI action, an inbound webhook, a schedule, another workflow
  completing).
- **Steps**: ordered, each with an `actor` (a role or AI-agent id — reuse BIR ids), the
  `action` taken, the `entity` it operates on, and `onFailure` (retry? escalate to a role?
  fail silently and log?).
- Write steps the way you'd write a runbook a new employee could follow, but tag each step
  with which parts a human currently must do vs. which are automatable/already automated by
  an agent in this compile — this becomes the seed for the AI-agent and automation sections,
  which should pick up as many of the "automatable" steps as make sense.

### Minimum workflow set (compile all that apply, add domain-specific ones)

- Primary lifecycle workflow (from the ontology).
- Cancellation / refund / return.
- Staff onboarding and shift/schedule assignment, if the business has employees.
- Inventory reorder, if the business holds stock.
- New customer onboarding / first-purchase.
- Escalation/complaint handling.

## Output format

Render as Markdown with one `##` section per entity/workflow, tables for fields and steps.
This is the file most likely to be read by a human engineer, so favor clarity over cleverness.
