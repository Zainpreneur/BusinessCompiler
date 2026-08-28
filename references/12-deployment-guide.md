# Deployment Guide

The final compiled artifact: a concrete path from the spec to a running system. Write this as
a guide a small team (or a solo founder using Claude Code) could actually follow, not a
generic "choose a tech stack" essay.

## 1. Stack recommendation

Recommend a concrete, boring, well-supported stack sized to `meta.scale` — don't
over-engineer a solo business into microservices, and don't under-spec a franchise into a
single SQLite file. A reasonable default to adapt rather than reinvent each time:

- **Data**: Postgres (Supabase is a good default when the compile also needs auth, storage,
  and edge functions out of the box — this session has a Supabase MCP connector if the user
  wants it provisioned directly).
- **Backend**: whatever the team already knows; if unspecified, a typed backend (Node/
  TypeScript or Python) with the data model in `02-data-model-workflows.md` as the schema
  source of truth.
- **Frontend**: a component framework matching the UI spec's mobile/desktop split in
  `03-ui-dashboards.md`.
- **AI agents**: implement via the Claude Agent SDK / Claude API, each agent from
  `04-ai-agents.md` as a scoped tool-use loop with its guardrails enforced in code, not just
  in the prompt.
- **Automations**: a workflow/automation runner (e.g. queue + scheduled jobs, or a no-code
  layer like the connected Make/Zapier/IFTTT MCPs if this session has them) driven off entity
  state-change events.
- **WhatsApp**: Cloud API or BSP per `06-whatsapp-integration.md`'s recommendation.
- **Hosting**: match to team familiarity — Railway/Vercel/Netlify are all available as
  connectors in this session if the user wants direct provisioning.

## 2. Build order

Sequence that keeps the system demoable at every step, front-loading the part of the business
that most needs the system first:

1. Data model + core lifecycle workflow (the primary lifecycle from the ontology) — get one
   entity end-to-end working before breadth.
2. Role-based UI for the primary workflow.
3. Security (RBAC minimum) — not deferred to "later," since retrofitting permissions onto a
   built system is expensive.
4. Automations + reminders for the primary lifecycle.
5. Integrations required for the business to actually operate (payments first if money moves
   through the system, then whichever else is load-bearing).
6. AI agents, starting with the highest-leverage one (usually the customer-facing concierge
   or the highest-toil manual task).
7. WhatsApp, social suite, marketing/CRM.
8. Simulation/forecasting (benefits from having real data flowing already).

## 3. Rollout plan

- Pilot with a subset (one branch, a limited customer segment, or a time-boxed period) before
  full rollout, especially for anything customer-facing (WhatsApp templates, automations) —
  bad automation firing at full customer volume is expensive to walk back.
- Data migration plan if replacing an existing system: map old records to the new entities
  before cutover, and run both systems in parallel for a defined window if the business can't
  tolerate downtime.
- Define the go/no-go checklist before flipping any automation or AI agent to fully
  autonomous (vs. human-approval-required) mode.

## 4. Output format

A short "Recommended stack" table, a numbered build order (as above, adapted to what was
actually compiled — skip steps for sections the user excluded via `/include-sections`), and a
rollout checklist.
