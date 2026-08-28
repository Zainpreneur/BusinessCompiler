# Security: RBAC / ABAC

Compiles `security`: who can do what, both by role and by attribute/context, plus audit and
compliance notes. AI agents are first-class principals here too — an agent's `guardrails`
from `04-ai-agents.md` should be enforceable as real permission entries, not just prose.

## RBAC — role-based permissions

For each role (human and agent) from the BIR, a permissions table: role, entity, allowed
actions (`create`/`read`/`update`/`delete`/`approve`). Defaults to apply unless the business
says otherwise:

- Front-line/customer-facing roles: read/update their own scope (their branch, their
  assigned jobs) — not global read.
- Manager roles: full read within their branch/department, update, approve; delete reserved
  for owner/admin only on financial and staff records.
- AI agents: scoped strictly to `entitiesTouched` from their agent definition, and only the
  actions their guardrails allow autonomously — anything above a guardrail threshold is
  `approve`-gated to a human role, not silently permitted.
- Owner/admin: full access, but still logged (see audit below) — "can do anything" should not
  mean "does so invisibly."

## ABAC — attribute-based policies

Layer on conditions RBAC alone can't express, as plain-language policy statements tied to BIR
fields, e.g.:

- "A branch manager can only approve refunds for orders where `order.branchId ==
  staff.branchId`."
- "A support agent can view `Customer.paymentMethod` only when handling an active support
  ticket for that customer, not for browsing." (time/context-bound access)
- "Marketing campaigns can only target customers where `customer.marketingConsent == true`."
  (directly enforces the consent rule from `06-whatsapp-integration.md`/`08-marketing-crm.md`
  at the security layer, not just as a marketing-team convention.)

List `abacPolicies` as this kind of readable rule — precise enough to implement as a policy
check, not vague ("be careful with sensitive data").

## Sensitive data handling

Cross-reference every entity field marked `piiOrSensitive` in the data model:
- Encrypt at rest and in transit (state this as a requirement, not optional).
- Restrict which roles/agents can read it in full vs. masked (e.g. front-desk sees last-4 of
  a payment method, not the full number).
- Log every access to fields marked sensitive, not just every write.

## Audit

Specify: every create/update/delete on financially or legally significant entities
(`Order`/`Invoice`/`Payment`/anything health- or compliance-tagged) is written to an
append-only audit log with actor (role or agent id), timestamp, before/after diff. AI-agent
actions are logged the same way as human ones — this is what makes "the agent did X
autonomously" reviewable after the fact.

## Compliance notes

Populate `complianceNotes` based on the business category flagged during discovery (Stage 1):
health-adjacent → note patient-privacy-equivalent handling; food service → food-safety
logging; anything taking payments → PCI-DSS scope minimization (prefer tokenized payment
integration over storing card data at all, per `09-integrations-framework.md`'s payments
category); anything with EU/CA customers → note data-subject rights (access/delete requests)
need a supported path against the data model, not just a policy statement.

## Output format

RBAC table, ABAC policy list, sensitive-field handling notes, audit scope statement,
compliance notes list.
