# Platform API & Webhooks

Compiles `platformApi`. `09-integrations-framework.md` is about this business *consuming*
other platforms (Stripe, QuickBooks, Google Calendar). This section is the mirror image:
**other systems integrating INTO this one** — a franchise partner's own POS syncing sales
back to headquarters, a marketplace pulling live inventory, a custom mobile app built by the
business itself, a no-code automation platform (Zapier/Make/IFTTT-style) wiring the business
into a customer's own stack, or a future product nobody's built yet. Without this, the
business is a data island that can only ever be the client of other people's APIs, never a
platform others build on.

Compile this section for any business past solo/small-team scale, or any business whose
model depends on partners/franchisees/marketplaces integrating with it — skip it (note why)
for a genuinely single-operator business with no plausible third-party consumers yet.

## API surface

- `platformApi.style`: REST is the safe default (widest client support); add GraphQL only if
  the business's integrators clearly need flexible querying across many entities (a franchise
  dashboard pulling custom cross-entity reports) rather than fixed per-entity endpoints.
- `platformApi.exposedEntities`: not every BIR entity should be exposed — pick the ones a
  legitimate external system would need (`Order`, `Customer`, `Appointment`, `Inventory`/
  `Stock`, rarely `JournalEntry` or anything HR-related) and, per entity, which operations
  (`read`/`create`/`update`/`delete`) actually make sense externally. A `Customer` might be
  `read`+`create` (a partner registers new customers) but never externally `delete`.
- Auto-derive the API's shape from the data model in `02-data-model-workflows.md` rather than
  designing it separately — the entity fields, relations, and state machines are already the
  source of truth; the API is a compilation target from the same BIR like everything else.

## Authentication & scopes

`platformApi.authMethods`: API keys for simple server-to-server integrations (a franchisee's
backend), OAuth2 client-credentials for automated system-to-system access, OAuth2
authorization-code for anything acting on behalf of an individual user (a customer-facing
third-party app), HMAC-signed requests for webhook-adjacent use cases.

`platformApi.scopes`: every scope should map to a real RBAC role from
`10-security-rbac-abac.md` (`mapsToRole`) rather than inventing a parallel permission system —
an API key scoped to `branch-manager`-equivalent access should be constrained exactly like a
human `branch-manager` is, including the same ABAC policies (a partner's API key for branch 2
should not be able to read branch 5's data, the same way a human branch manager can't).
Never expose a scope broader than "full read/write to everything" without an explicit reason
— narrow, named scopes per integration purpose (`orders:read`, `inventory:read`,
`customers:write`) are what make this safe to hand out to third parties at all.

## Webhooks (outbound events)

`platformApi.webhookEvents`: for each event, name the `sourceEntity`, the `sourceTransition`
it fires on (reuse the exact transition names already defined in that entity's state machine
in `02-data-model-workflows.md` — don't invent parallel event names), and `payloadFields`
(keep payloads minimal — IDs and the fields that actually changed, not the whole entity, so
consumers fetch fresh detail via the API rather than trusting a possibly-stale payload for
anything sensitive).

Standard events worth exposing for most businesses: order/appointment created, status
changed, completed, cancelled; payment received/failed; customer created; stock level
crossed a threshold (useful for a partner's own reordering logic). Let subscribers pick which
events they want rather than firing everything at every endpoint.

**Delivery guarantees**: sign every payload (HMAC with a per-subscriber secret) so receivers
can verify authenticity; retry with exponential backoff on delivery failure; support replay
(a subscriber can request re-delivery of a missed event by ID) rather than leaving them to
reconstruct state by polling. This reuses the same failure-handling pattern as inbound
integrations in `09-integrations-framework.md` — retry/backoff/dead-letter logic shouldn't be
reinvented per direction.

## Rate limits & versioning

State `platformApi.rateLimits` concretely (e.g. "600 requests/min per API key, 429 with
`Retry-After` on breach") rather than leaving it unspecified — an unthrottled API is a
reliability and cost risk the moment a partner's integration has a bug. State
`platformApi.versioningStrategy` (URL-prefixed `/v1/`, or a header-based version) so future
BIR recompiles that change entity shapes don't silently break existing integrations —
breaking changes ship as a new version, existing integrations keep working against the old one
until they migrate.

## Developer experience

Generate API reference docs directly from `exposedEntities` (entity fields become the
resource schema, operations become the documented endpoints) and from `webhookEvents` (the
event catalog) — this should be a natural byproduct of the BIR being the single source of
truth, not a hand-written doc that drifts from the real API. For a business planning a real
partner ecosystem (franchise, marketplace), note that a lightweight self-serve developer
portal (API key generation, webhook subscription management, docs) is worth building; for a
business with 1-2 known integration partners, a shared doc and manually issued keys are
enough — right-size this like everything else.

## Output format

API style and rationale, exposed-entities table (entity/operations), auth methods and scopes
table (scope/maps-to-role), webhook events table (event/source entity/transition/payload
fields), rate limit and versioning statements, and a one-line developer-experience note.
