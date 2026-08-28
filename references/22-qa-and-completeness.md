# Comprehensive QA & Completeness Check

This is Stage 4 of the pipeline: after every requested section is compiled, walk the whole
output back through this checklist *before* presenting the compile as finished. `scripts/
validate_bir.py` catches broken cross-references mechanically (an ID that doesn't resolve);
this pass catches the harder failure mode — logic that's internally consistent but still
wrong, missing, or contradictory, which no script can fully check because it requires
judgment about whether the *content* makes sense, not just whether the *references* resolve.

Do this for every full compile. For a narrowed `/include-sections` compile, run only the
checks relevant to the sections actually produced. Write findings (and what you fixed) to
`07-delivery/qa-report.md` alongside the other output files — a compile that was checked and found clean
is a stronger deliverable than one that was never checked, and the report proves which one
this is.

## 1. Business logic

- **Every lifecycle is actually traversable.** For each entity with `states`
  (`02-data-model-workflows.md`), confirm every non-terminal state has at least one outgoing
  transition, and every transition's trigger is either a human UI action, an automation, or
  an agent — not left implicit. A state nothing can leave is a dead end a real order will get
  stuck in.
- **Every workflow's unhappy path is defined.** A workflow step with no `onFailure` is only
  acceptable when failure there is genuinely inconsequential (a non-critical notification) —
  for anything touching money, inventory, or a customer commitment, an undefined failure path
  is a gap, not a simplification.
- **Every KPI and analytics measure is computable.** Walk each `kpis` entry and each measure
  in `13-analytics-and-reporting.md` back to the actual entity fields it's built from — if a
  formula references something no entity has (e.g. "customer satisfaction score" with no
  field anywhere capturing it), either add the field to the data model or drop the metric;
  don't leave an unbacked number in the output.
- **Automations can't loop or spam.** Re-check the anti-spam/stacking rule from
  `05-automations-reminders.md` against the *final* automation + reminder + agent list (it's
  easy to satisfy in isolation and violate once every section is compiled) — trace one
  realistic event (an order becoming ready) through every rule that could fire on it and count
  how many messages a customer would actually receive.
- **Numbers agree across modules.** The commission basis in `19-hr-payroll.md` should be the
  exact same field the CRM pipeline (`17-crm-sales-support.md`) and analytics
  (`13-analytics-and-reporting.md`) report against; the revenue figure driving the P&L in
  `16-accounting-finance.md` should be the same figure the health score in
  `13-analytics-and-reporting.md` uses. Two modules computing "the same" number two different
  ways is a bug even if each is individually correct.
- **Financial logic actually balances.** Every auto-posted journal entry in
  `16-accounting-finance.md` debits and credits equal amounts; tax collected posts to a
  liability account, never revenue; an entity's `money` field used in more than one financial
  statement means the same thing in both (don't let "revenue" silently mean gross in one place
  and net-of-refunds in another).

## 2. AI logic

- **Every agent is complete.** `purpose`, concrete `tools` (from the standard vocabulary or a
  clearly-named custom one), `triggers`, `entitiesTouched`, and at least one real `guardrail`
  — an agent missing any of these isn't ready to hand to an engineering team, it's a stub.
- **Every escalation and reporting-line target exists and makes sense.** `escalatesTo` should
  be a role that would plausibly want that escalation (not just any role); `reportsTo` should
  resolve to an orchestrator/advisor that actually exists.
- **No agent has unchecked authority over an irreversible action.** Re-read every agent's
  guardrails specifically hunting for a gap: can it, as specified, issue a refund, cancel a
  contract, take equipment offline, or contact a customer who opted out, without a human in
  the loop? If yes and that wasn't a deliberate, stated decision, tighten the guardrail.
- **Advisor reasoning is real, not decorative.** Every `advisor`-tier agent should have at
  least one named `reasoningPatterns` entry from `04-ai-agents.md`'s list, and its purpose
  should describe producing a structured recommendation (question, pattern used, data,
  recommendation, confidence, next step) — not just "answers questions."
- **Confidence and escalation thresholds are stated, not implied.** "Hands off to a human when
  unsure" is a placeholder; "hands off when confidence is below 70%, or the question touches
  health/legal/payment data regardless of confidence" is a real guardrail. Fix any agent still
  written the vague way.
- **The agent roster is right-sized.** Recheck against `meta.scale` one more time now that
  every section is compiled — a roster that grew section-by-section can end up bigger than the
  business actually needs; cut or merge agents that ended up with genuinely overlapping jobs.

## 3. Integrations, API & security logic

- **Every integration's `entitiesSynced` and every webhook's `sourceEntity`/
  `sourceTransition`** (`09-integrations-framework.md`, `20-api-and-webhooks.md`) resolve to
  real entities and real transitions — `scripts/validate_bir.py` checks the entity side
  mechanically; manually confirm the *transition* names match what
  `02-data-model-workflows.md` actually defined, since the script doesn't parse workflow
  transitions.
- **Every API scope maps to a real RBAC role**, and that role's permissions in
  `10-security-rbac-abac.md` are themselves defined — a scope pointing at an undefined or
  overly-broad role defeats the purpose of scoping at all.
- **Every sensitive field has a stated access rule.** Cross-check every `piiOrSensitive: true`
  field against `10-security-rbac-abac.md` — a field flagged sensitive with no corresponding
  masking/access restriction anywhere is a compliance gap, not just a modeling oversight.
- **Every role that appears anywhere (workflow actor, agent `escalatesTo`, KPI `targetRoles`,
  API scope) has at least one permission entry.** An orphaned role that nothing grants access
  to can't actually do the job it was assigned.

## 4. Coverage against the original ask

Re-read the business description the user actually gave (and any assumptions logged in
`meta.assumptions`) and confirm the compile addresses everything they mentioned — it's easy
for a specific detail from the original request to get lost across 15+ compiled files. If
something they asked for isn't reflected anywhere, that's the highest-priority fix of this
whole pass.

## Output format

Write `07-delivery/qa-report.md`: one short subsection per category above, each either "✅ checked, no
issues" or "⚠️ found X, fixed by Y" (or "flagged, needs a decision" for anything that isn't
safe to fix unilaterally — e.g. a genuine ambiguity in what the user wants). End with the
`validate_bir.py` output. A qa-report with zero findings across a large compile is a signal to
re-check your own thoroughness, not a badge of honor — most real compiles surface at least a
few things worth tightening.
