# Advanced Accounting & Finance

Compiles `accounting`. Until now, accounting only existed as an external integration
(`09-integrations-framework.md`'s accounting category) and as derived financial statements in
`13-analytics-and-reporting.md`. This section is the native ledger underneath both — whether
the business ultimately posts to QuickBooks/Xero or runs its own books inside the compiled
system, the ledger model here is what keeps every dollar traceable.

## Chart of accounts

Define `accounting.chartOfAccounts`: a right-sized list per `type`
(asset/liability/equity/revenue/expense), not a generic textbook chart. Start from the
business's real transactions — a laundry needs `Cash`, `Accounts Receivable`, `Detergent
Inventory`, `Wash Revenue`, `Dry-Clean Revenue`, `Supplier Payables`, `Payroll Expense`,
`Rent Expense`; a SaaS business needs `Deferred Revenue`, `MRR`, `Hosting Expense`. Keep it as
short as the business can operate with — a solo operator might need 15 accounts, a franchise
80+, organized by branch/cost-center if multi-location.

## The ledger

Every financial event in the business (a payment received, an expense incurred, a payroll
run, an inventory write-off) should be expressible as a double-entry journal entry:
`accounting.ledgerEntity` names the BIR entity (typically `JournalEntry`, with a
`JournalLine` child holding account/debit/credit) that records it. Tie journal entries back to
the source: a `JournalEntry` created from an `Order` being paid should reference the
`Order.id`, not stand alone — this is what makes the P&L in `13-analytics-and-reporting.md`
auditable down to the originating transaction rather than a black box.

**Auto-posting rule**: every workflow step in `02-data-model-workflows.md` that moves money
(payment received, refund issued, payroll run, inventory received) should generate its
journal entry automatically via an automation (`05-automations-reminders.md`), not require
manual bookkeeping — that's the entire point of compiling accounting into the system rather
than bolting it on afterward.

## Multi-currency

If `accounting.additionalCurrencies` is non-empty: every `money`-typed field
(`02-data-model-workflows.md`) needs a currency alongside the amount, transactions convert at
the rate on their transaction date (store the rate used, don't recompute historical entries
at today's rate), and reporting (`13-analytics-and-reporting.md`) rolls up to `baseCurrency`
with FX gain/loss tracked as its own line. Skip this section entirely for single-currency
businesses — don't add complexity that isn't needed.

## Tax

Define `accounting.taxRules` per jurisdiction the business actually operates in (sales tax by
state, VAT by country, or none if genuinely not applicable) — each rule names its rate and
what it applies to (`Order` line items, service fees). Tax collected is a liability
(`Sales Tax Payable`), not revenue — make sure the chart of accounts and journal-posting rule
reflect that, it's a common and costly modeling mistake.

## Banking & reconciliation

`accounting.bankAccounts`: link each to an integration (`09-integrations-framework.md`) that
feeds transaction data in. Bank reconciliation is the process of matching ledger entries
against actual bank transactions — spec it as a periodic workflow (`02-data-model-workflows.md`
style: trigger, steps, actor) rather than leaving it implicit, with unmatched transactions
flagged for a human (or the `strategy-advisor`/an accounting specialist agent) to investigate.

## Budgets

`accounting.budgets`: a budget is a planned amount per account per period per scope
(business-wide or per-branch). Compare actuals (from the ledger) against budget in the
Financial View (`14-business-views.md`) — this is what turns the ledger from bookkeeping into
a planning tool. Feed budget-vs-actual variance beyond a threshold into
`13-analytics-and-reporting.md`'s anomaly rules.

## Period close

`accounting.closeChecklist`: the ordered steps to close a period (reconcile bank accounts,
post accrued expenses, review AR/AP aging, lock the period from further edits). Automate what
can be automated (reconciliation matching, accrual posting from known recurring costs) and
leave a clear human sign-off step for anything judgment-based.

## Payroll linkage

If `accounting.payrollLinked` is true, payroll runs from `19-hr-payroll.md` post directly to
the ledger (wages to `Payroll Expense`, withholdings to the relevant liability accounts) —
name that link explicitly so the two modules don't silently duplicate or contradict each
other's numbers.

## Output format

Chart of accounts table (code/name/type), ledger entity description with an example
auto-posted journal entry, currency/tax notes if applicable, bank accounts and reconciliation
workflow, budgets list, close checklist, and the payroll-linkage note.
