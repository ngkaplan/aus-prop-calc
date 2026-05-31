from src.domain.scenarios.scenario_calculator import ScenarioCalculator
from src.ui.components.summary_tables import SummaryTableManager


def _build_after_tax_scenarios(analysis_years: int = 20):
    calc = ScenarioCalculator()

    btl = calc.calculate_buy_to_live_scenario(
        property_price=800_000,
        deposit_percent=0.2,
        interest_rate=0.06,
        loan_term=30,
        annual_property_growth_rate=0.03,
        annual_property_expenses_percent=0.01,
        upfront_costs=3_000,
        is_first_home_buyer=False,
        analysis_years=analysis_years,
    )

    btr = calc.calculate_buy_to_rent_scenario(
        investment_property_price=650_000,
        deposit_percent=0.2,
        interest_rate=0.06,
        loan_term=30,
        weekly_rental_income=620,
        your_weekly_rent=500,
        annual_property_growth_rate=0.03,
        annual_rental_inflation_rate=0.025,
        annual_property_expenses_percent=0.01,
        upfront_costs=3_000,
        is_first_home_buyer=False,
        analysis_years=analysis_years,
        annual_gross_income=120_000,
        salary_growth_rate=0.03,
    )

    btl_housing_costs = [row["annual_housing_cost"] for row in btl["yearly_analysis"]]
    ri = calc.calculate_rent_and_invest_scenario(
        equivalent_property_price=800_000,
        deposit_percent=0.2,
        your_weekly_rent=500,
        annual_stock_return_rate=0.07,
        annual_rental_inflation_rate=0.025,
        upfront_costs=3_000,
        is_first_home_buyer=False,
        analysis_years=analysis_years,
        btl_housing_costs=btl_housing_costs,
    )

    return calc.apply_capital_gains_tax(
        btl_analysis=btl,
        btr_analysis=btr,
        ri_analysis=ri,
        annual_gross_income=120_000,
        salary_growth_rate=0.03,
    )


def test_export_dataframes_and_workbook_have_expected_shape():
    btl, btr, ri = _build_after_tax_scenarios(analysis_years=20)
    summary_manager = SummaryTableManager()

    summary_df = summary_manager.build_final_summary_dataframe(btl, btr, ri)
    milestone_df = summary_manager.build_milestone_dataframe(btl, btr, ri)
    cash_flow_df = summary_manager.build_cash_flow_dataframe(btl, btr, ri)
    workbook_bytes = summary_manager._build_export_workbook(summary_df, milestone_df, cash_flow_df)

    assert list(summary_df["Scenario"]) == ["Buy to Live", "Buy to Rent", "Rent & Invest"]
    assert milestone_df["Year"].tolist() == [5, 10, 15, 20]
    assert len(cash_flow_df) == 21  # includes year 0
    assert cash_flow_df.iloc[0]["Buy to Live Net Worth"] == 0
    assert len(workbook_bytes) > 1000


def test_real_life_reasonableness_for_growth_and_debt_progression():
    btl, btr, ri = _build_after_tax_scenarios(analysis_years=25)

    btl_years = btl["yearly_analysis"]
    btr_years = btr["yearly_analysis"]
    ri_years = ri["yearly_analysis"]

    # With positive property growth assumptions, property values should increase over time
    assert btl_years[0]["property_value"] < btl_years[-1]["property_value"]
    assert btr_years[0]["property_value"] < btr_years[-1]["property_value"]

    # Remaining balance should decrease as mortgage principal is paid down
    assert btl_years[0]["remaining_balance"] > btl_years[-1]["remaining_balance"]
    assert btr_years[0]["remaining_balance"] > btr_years[-1]["remaining_balance"]

    # Stock portfolio should grow over a long horizon with positive expected return
    assert ri_years[-1]["stock_portfolio_value"] > ri_years[0]["stock_portfolio_value"]

    # After-tax value should not exceed before-tax value for taxable scenarios
    assert btr_years[-1]["net_worth_after_tax"] <= btr_years[-1]["net_worth"]
    assert ri_years[-1]["net_worth_after_tax"] <= ri_years[-1]["net_worth"]
