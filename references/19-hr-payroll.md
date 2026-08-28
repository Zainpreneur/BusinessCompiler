# HR & Payroll

Compiles `hr`. Added as an "other module upgrade" — any business with employees (which is
most businesses past solo scale) has so far only had staff mentioned as a `role` and a
one-line onboarding workflow. This section makes people-management a real module. Skip
entirely for a genuinely solo operator with no employees or contractors.

## Employee lifecycle

`hr.employeeLifecycleStages`: e.g. `Applicant -> Hired -> Onboarding -> Active -> On Leave ->
Offboarded`. Add an `Employee` entity (distinct from `Staff`-as-a-role if the business
already has staff roles in `02-data-model-workflows.md` — `Employee` holds HR-specific fields
like hire date, compensation, and emergency contact; the role determines what they can do in
the system, the employee record is who they are as a person). Mark compensation and any
government-ID/tax fields `piiOrSensitive: true` — this data needs the field-level restrictions
in `10-security-rbac-abac.md` (a front-desk colleague shouldn't see another employee's pay
rate).

## Scheduling

`hr.schedulingEntity` (usually `Shift`): links `Employee` × time window × location/role. This
is what the staffing/capacity simulator (`11-simulation-forecasting.md`) and the "shift starts
with no staff confirmed" automation (`05-automations-reminders.md`) both key off. For
businesses with variable/seasonal demand, tie shift planning to the demand forecast so
scheduling isn't done blind to expected volume.

## Compensation & payroll

- `hr.compensationModel`: name each pattern in use — hourly wage, salary, commission (and on
  what — e.g. "10% commission on `Deal.value` for sales reps," reusing the `Deal` entity from
  `17-crm-sales-support.md`), tips, or a mix.
- `hr.payrollCadence`: weekly/biweekly/semimonthly/monthly.
- A payroll run is a workflow (`02-data-model-workflows.md` style): compute hours/commission
  from `Shift`/`Deal` records for the period → apply withholdings per the tax rules in
  `16-accounting-finance.md` → generate pay records → post to the ledger if
  `accounting.payrollLinked` → disburse (via a payments integration,
  `09-integrations-framework.md`) → generate pay-stub documents
  (`15-knowledge-and-documents.md`). Spec it as one traceable pipeline, not a black box that
  "runs payroll."

## Leave management

`hr.leavePolicies`: name each leave type and its accrual/allowance rule (e.g. "10 PTO days/
year, accrued monthly"). A leave request is a small workflow (request → manager approval →
calendar block via the calendar integration, `09-integrations-framework.md`, so scheduling
automatically respects it).

## Performance

`hr.performanceReviewCadence`: if the business is large enough to warrant formal reviews
(usually multi-location+/franchise scale — a 2-person team does this conversationally, don't
over-formalize it), define the cadence and what's tracked. This is where an AI "performance-
summary generator" agent from `04-ai-agents.md`'s catalog earns its place — drafting a
factual summary from real data (shifts covered, sales/tickets closed, customer feedback tied
to that employee) for a manager to review and add judgment to, never auto-finalized.

## Commission & incentive tie-back

Where `hr.compensationModel` includes commission, make sure the number it's computed from is
the same one the CRM pipeline (`17-crm-sales-support.md`) and analytics
(`13-analytics-and-reporting.md`) report — a commission dashboard showing different numbers
than the sales dashboard is a fast way to lose staff trust in the system.

## Output format

Employee lifecycle stages, `Employee`/`Shift` entity notes (fields beyond the standard set),
compensation models table (role/model/basis), payroll pipeline steps, leave policies list,
performance review cadence and what's tracked, and the commission tie-back note if applicable.
