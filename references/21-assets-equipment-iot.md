# Assets, Equipment & IoT / Predictive Maintenance

Compiles `assets`. Distinct from `18-inventory-supply-chain.md`, which tracks *consumable*
stock (detergent, food, retail products) — this section tracks *durable, non-consumable*
equipment (washing machines, wash bays, HVAC/climate-control systems, vehicles, medical
equipment, irrigation systems) whose failure or downtime directly costs the business money.
This closes a real gap: several of the compiler's own worked examples (a car wash's service
bays, an urban farm's climate control) depend on equipment that was never modeled anywhere.
Skip this file entirely for asset-light businesses (a pure SaaS or a service business that
rents its space and owns little equipment) — say so rather than inventing assets to track.

## Asset registry

`assets.assetEntity` (usually `Asset` or a domain name like `Machine`/`Bay`/`Vehicle`): fields
per the standard entity pattern in `02-data-model-workflows.md` — type, location/branch,
purchase date, warranty expiry, current status (`operational`/`degraded`/`down`/`retired`).
`assets.assetTypes`: name the actual categories this business owns (wash bays and dryers for
a laundry; grooming tables and dryers for a pet groomer; irrigation pumps and climate
controllers for a farm) — generic "equipment" isn't specific enough to generate a real
maintenance plan from.

## Preventive maintenance

`assets.maintenanceSchedules`: per asset type, the cadence and task (e.g. "wash-bay pump:
lubricate monthly, replace seals annually"). A maintenance due date is exactly the same
pattern as a customer reminder in `05-automations-reminders.md` — reuse `reminderRule`
against the `Asset` entity instead of inventing a separate scheduling mechanism, escalating
to the responsible role if a scheduled service is overdue.

## IoT telemetry

If the business has (or should have) connected sensors, define `assets.iotTelemetry` per
asset type: which signals are read (temperature, vibration, cycle count, runtime hours,
power draw) and which integration (`09-integrations-framework.md`'s new `iot-telemetry`
category — e.g. a sensor platform's API or MQTT broker) feeds them in. Not every business
needs this — a single-location business with 2-3 machines can run on manual inspection and
the preventive schedule alone; IoT telemetry earns its cost once the business has enough
equipment, or high enough downtime cost, that catching a failure early is worth the sensor
investment.

## Predictive maintenance (the AI-native part)

Set `assets.predictiveMaintenance: true` and add a `predictive-maintenance` specialist agent
to `04-ai-agents.md` when telemetry is in place: it watches signal trends against each asset's
normal operating range (not a fixed threshold — a slow drift over weeks reads very differently
from a sudden spike, and the agent should distinguish them), flags anomalies before a hard
failure occurs, and **auto-creates a maintenance work order** (linked to the affected `Asset`)
rather than just alerting — pulling in required parts from `18-inventory-supply-chain.md`'s
stock if the maintenance task consumes any. Guardrail: it can schedule and request parts
autonomously, but taking equipment fully offline during business hours needs the responsible
role's confirmation unless the asset is already failed/unsafe to keep running.

This is a case where the automation-vs-agent line from `05-automations-reminders.md` matters:
a fixed preventive schedule is a plain automation (deterministic, no judgment needed);
predicting failure from a noisy sensor trend before it's obvious is exactly the kind of
judgment call that belongs to an agent, not a rule.

## Downtime cost

Track downtime as a cost the business actually feels: an `Asset` going `down` should be
computable against the revenue/capacity it represents (a wash bay down for 2 days at typical
utilization is a quantifiable lost-revenue figure) — feed this into
`13-analytics-and-reporting.md`'s anomaly rules and the capacity simulator in
`11-simulation-forecasting.md`, so "how much did that breakdown actually cost us" is an
answerable question, not a shrug.

## Output format

Asset types and registry entity notes, maintenance schedule table (asset type/cadence/task),
IoT telemetry table (asset type/signals/integration) if applicable, predictive-maintenance
agent summary (or a note that fixed scheduling alone is sufficient at this scale), and a
downtime-cost tie-in note.
