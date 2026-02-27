# Roadmap

Canonical planning file for feature delivery in this repo.

## Now

### 1) What I Can Afford Switch
- Status: In Progress (core complete, polish/testing remaining)
- Owner: Noah
- Target date: TBD
- Why:
  - Current flows require manual property-price inputs.
  - You want an affordability-first workflow based on borrowing constraints and available cash.
- Feature:
  - Add a switch named `What I can afford switch`.
  - When enabled, replace direct property-price inputs with:
    - `Cash available today ($)`
    - `Maximum bank borrowing ($)`
    - `Allowed LVR (%)`
    - `Include LMI above 80% LVR` toggle (investment scenario)
    - `Upfront costs ($)` (legal, conveyancing, inspections, etc.)
  - Back-solve maximum purchasable property value for Buy to Live and Buy to Rent.
  - Use those solved property values as scenario inputs for downstream projection.
- Acceptance criteria:
  - With switch off, current manual property-price workflow remains unchanged.
  - With switch on, app computes property value instead of asking for direct value entry.
  - If `cash + borrowing` cannot cover stamp duty + upfront costs + required equity, app shows a clear infeasible-state message.
  - Investment scenario supports LVR > 80% only when LMI toggle is enabled, and includes LMI in acquisition cost.
  - Computed property values are visible in the summary section and used by all charts/tables.
  - Unit tests cover affordability solver edge cases and infeasible states.

### 2) Household Cashflow Stress (Bankruptcy Guard)
- Status: Planned
- Owner: Noah
- Target date: TBD
- Why:
  - Current model compares net worth but does not explicitly fail scenarios with unsustainable monthly cashflow.
- Feature:
  - Add `Other Monthly Expenses ($)` slider/input to represent non-housing living costs.
  - Inflate this cost annually using inflation assumptions.
  - Include this cost in yearly cashflow projections for all scenarios.
  - Flag potential bankruptcy/insolvency when cumulative cash buffer goes negative.
- Acceptance criteria:
  - New expense input appears in assumptions.
  - Expense amount increases yearly by inflation rate in all scenario calculations.
  - Scenario output includes bankruptcy flag and first year/month of insolvency (if any).
  - UI clearly warns when a scenario goes insolvent.
  - Tests verify inflation indexation and insolvency detection behavior.

### 3) Portfolio Growth Tab (Serviceability + Repeat Purchases)
- Status: Planned
- Owner: Noah
- Target date: TBD
- Why:
  - Need to model how many investment properties can be acquired over time based on realistic lending constraints.
  - Preserve existing dashboard while introducing a dedicated advanced strategy workflow.
- Scope constraints:
  - Must live on a separate dashboard tab so original comparison flow is unchanged.
  - Build and merge in incremental stages on short-lived feature branches.

#### Stage 1: New Tab + Inputs Scaffold
- Status: Planned
- Deliverables:
  - Add `Portfolio Growth (Serviceability)` tab.
  - Add inputs for assessment buffer, rental income haircut, expense floor, cash buffer months, and acquisition assumptions.
  - No portfolio simulation yet; UI scaffolding only with placeholder summary.
- Acceptance criteria:
  - Existing tab behavior remains unchanged.
  - New tab renders with persisted inputs and clear sectioning.

#### Stage 2: Serviceability Engine
- Status: Planned
- Deliverables:
  - Implement repayment-based capacity with assessment rate = `actual rate + 3%`.
  - Include salary + haircut rental income.
  - Include user expenses with lender-style minimum floor.
  - Include existing debt commitments in serviceability.
- Acceptance criteria:
  - Capacity outputs produced year-by-year.
  - Tests verify debt/income/expense interactions and edge cases.

#### Stage 3: Multi-Purchase Simulator
- Status: Planned
- Deliverables:
  - Add yearly purchase loop for additional investment properties.
  - Purchase only when serviceability, deposit/costs, and post-purchase cash buffer pass.
  - Include stamp duty, legal costs, and LMI rules for each purchase.
- Acceptance criteria:
  - Deterministic purchase timeline generated.
  - Tests verify stop/go purchase conditions.

#### Stage 4: Stop Conditions + Risk Guards
- Status: Planned
- Deliverables:
  - Bankruptcy/insolvency and eroded-buffer stop conditions.
  - Reason codes for blocked purchases (capacity, cash, buffer, serviceability).
- Acceptance criteria:
  - Simulation halts correctly on failure conditions.
  - UI shows first failure point and reason.

#### Stage 5: Portfolio Analytics + Charts
- Status: Planned
- Deliverables:
  - Charts for borrowing capacity, serviceability surplus/deficit, DTI, portfolio LVR, debt/equity, and property count.
  - Purchase timeline table (year, price, loan, costs, cash remaining).
- Acceptance criteria:
  - Charts/tables align with simulation output.
  - Export-ready summary table included.

## Next

### 3) Sensitivity Analysis
- Status: Planned
- Owner: Noah
- Target date: TBD
- Why:
  - Need confidence in recommendations under uncertain rates/growth assumptions.
- Acceptance criteria:
  - Vary key assumptions across ranges (at minimum interest rate, growth, and rent inflation).
  - Show scenario rank stability and outcome spread.
  - Add visualization and exportable summary table.

## Later

### 4) Data Export and Scenario Save/Load
- Status: Planned
- Owner: Noah
- Target date: TBD
- Why:
  - Improve repeatability and sharing of analyses.
- Acceptance criteria:
  - Export results to CSV.
  - Save and reload named scenario input sets.
