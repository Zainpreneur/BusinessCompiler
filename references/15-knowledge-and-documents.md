# Knowledge Base & Documents

Compiles `knowledgeBase`. Added because every real business runs on documents and shared
knowledge as much as it runs on transactional data — contracts, SOPs, policies, quotes,
receipts, an internal wiki — and because the conversational/customer-facing AI agents
(`04-ai-agents.md`) are only trustworthy if they answer from a real source of truth instead of
improvising policy on the spot.

## Document types

For each, define `id`, `category`, and (for generated documents) `generatedFrom` — the BIR
entities whose fields populate it:

- **Customer-facing**: quote/proposal, invoice/receipt (usually auto-generated from
  `Invoice`/`Order` at the automation layer — see `05-automations-reminders.md`), service
  agreement/contract, warranty/return policy handed out at point of sale.
- **Internal**: SOPs/standard procedures (opening/closing checklist, safety procedure,
  quality-check steps), employee handbook excerpts, compliance logs (the ones flagged in
  `10-security-rbac-abac.md`'s compliance notes — a food-safety log, a controlled-substance
  log).
- **Knowledge-base articles**: FAQ entries, policy explanations, troubleshooting guides — the
  material that backs the WhatsApp concierge, social-listening responses, and any customer-
  facing agent's answers.

Right-size this list to the business: a solo operator needs a handful of documents (an
invoice template, a couple of SOPs, a short FAQ); a franchise needs a real document library
organized by branch/department.

## Grounding AI agents in the knowledge base

Set `knowledgeBase.groundsAgents` to the agent ids (from `04-ai-agents.md`) that must answer
from KB articles rather than generating policy answers from general knowledge — this is
almost always the customer-facing/concierge agents and the review-response agent. Treat an
agent confidently answering a policy question that isn't in the KB as a bug: either the KB
is missing an article (write one) or the agent should escalate instead of guessing.

## Generation

Documents generated from entity data (invoices, receipts, contracts pre-filled with customer/
order details) should be specified as a template + variable list, the same pattern as the
WhatsApp templates in `06-whatsapp-integration.md` — variables map directly to BIR fields, so
"generate the invoice" is a deterministic render, not a fresh AI composition each time. Reserve
AI generation for documents that are genuinely bespoke per instance (a proposal tailored to a
specific customer's needs).

## Storage, versioning, and e-signature

- `knowledgeBase.sources`: where documents/KB articles actually live — usually a storage
  integration (`09-integrations-framework.md`'s storage category, e.g. Google Drive/Dropbox)
  or a lightweight internal wiki. Name it explicitly rather than leaving "the knowledge base"
  unlocated.
- Version documents and KB articles the same way the BIR itself is versioned (bump on
  material change, keep prior versions retrievable) — critical for contracts and compliance
  logs where "what did this document say on the date it was signed" matters.
- For anything requiring a signature (contracts, service agreements), specify e-signature as
  part of the flow rather than assuming a printed/manual process, unless the business's scale
  clearly doesn't warrant it.

## Output format

Document types table (id/category/generated-from-or-authored), the grounding list (which
agents must cite the KB), source/storage location, and a one-line versioning/e-sign note.
