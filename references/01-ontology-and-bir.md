# Discovery, Ontology, and the BIR

This is Stage 1–2 of the pipeline: turning a business description into the shared model
(`assets/bir-schema.json`) that every later section compiles from.

## 1. Discover the Business DNA

An experienced operator in any given industry already knows most of its shape. Act like one.
Before asking anything, infer:

- **Core objects**: what gets tracked (customers, jobs/orders, inventory, staff, assets,
  appointments...) and what the universal-to-domain mapping is (every business has a
  `Customer` and an `Order`-shaped thing, even if it's called `Patient`/`Encounter` or
  `Member`/`Booking`).
- **Value flow**: how money enters and leaves — one-time sale, subscription, project billing,
  usage metering, mixed.
- **Primary lifecycle**: the one sequence that IS the business (intake → fulfill → bill →
  collect, or plant → grow → harvest → sell, etc.).
- **Scale signal**: words like "multi-branch", "chain", "solo", "just me and one employee"
  tell you `meta.scale` directly — use them.
- **Regulatory/compliance flavor**: health, food, alcohol, childcare, finance-adjacent
  businesses carry known compliance concerns (HIPAA-like privacy, food safety logs, PCI for
  payments) — bake these into the security section by default, don't wait to be told.

### When to ask vs. assume

Ask **only** when a fork changes the shape of the model in a way a wrong guess would be
expensive to unwind, and there's genuinely no signal in what the user said. Good examples:

- "Is this single-location or will it span multiple branches?" (changes almost every entity)
- "Are your customers mostly individuals or businesses?" (changes CRM/marketing entirely)

Bad examples (don't ask — just assume and note it): "What should the primary color of the
dashboard be?", "Do you want reminders in English?", "Should orders have an ID field?". For
anything like that, pick the sensible default and record it in `meta.assumptions` so the user
can correct it in one line later ("actually no loyalty program") without you having blocked
on it.

Cap yourself at 0–3 questions, asked together, not interrogation-style one at a time.

## 2. Build the Ontology

Fill `ontology` in the BIR:

- `coreObjects`: list the universal→domain mappings, e.g. `["Customer -> Client", "Order -> WashJob", "Location -> ServiceBay"]`.
- `valueFlow`: one sentence.
- `primaryLifecycle`: the named sequence, e.g. `"Booking -> ServiceDelivery -> Invoice -> Payment"`.

This ontology is what keeps section generation domain-flavored instead of generic — every
later reference file should render entity names using the domain terms you chose here, not
the generic "Customer/Order" placeholders.

## 3. Compile the BIR

Populate the rest of `assets/bir-schema.json`'s top-level keys:

- `entities` — see `references/02-data-model-workflows.md` for how deep to go.
- `roles` — every human role (owner, manager, front-desk, technician, driver...) *and* every
  AI-agent role gets a `role` entry with `isHuman: false` for agents, so permissions and
  workflow `actor` fields can reference agents and humans uniformly.
- `workflows` — the primary lifecycle plus any secondary ones (returns/refunds, onboarding a
  new staff member, restocking).
- Leave `aiAgents`, `automations`, `reminders`, `whatsapp`, `socialMedia`, `marketing`,
  `integrations`, `security`, `simulation` to be filled during Stage 3 as each section is
  compiled — but reserve the entity/role IDs those sections will need now, while you have the
  full picture, so they don't invent conflicting ones later.

## 4. Naming conventions (keep these stable across the whole compile)

- Entity IDs: `PascalCase`, singular (`Appointment`, not `Appointments`).
- Field IDs: `camelCase`.
- Role IDs: `kebab-case` (`front-desk`, `branch-manager`).
- Agent IDs: `kebab-case`, ending in a noun that names its job (`reminder-agent`,
  `inventory-forecaster`, `whatsapp-concierge`).
- Workflow/automation IDs: `kebab-case`, verb-first (`book-appointment`,
  `send-pickup-reminder`).

Reuse these IDs verbatim in every downstream section. A dashboard KPI, a WhatsApp template
variable, and an automation trigger should all say `Appointment.status`, not three different
spellings of "appointment status."

## 5. Recompiling

On a follow-up change request, load the existing `bir.json` if present, bump `meta.version`,
patch only the affected entities/roles/workflows, and re-run Stage 3 only for the sections
that reference what changed (e.g. adding a `LoyaltyPoints` field to `Customer` means
recompiling the data model, the CRM/marketing section, and any dashboard showing customer
value — not the WhatsApp templates unless they also change).
