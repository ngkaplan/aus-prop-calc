from src.domain.scenarios.scenario_calculator import ScenarioCalculator


def test_scenarios_respect_analysis_years():
    calc = ScenarioCalculator()

    btl = calc.calculate_buy_to_live_scenario(
        property_price=800_000,
        deposit_percent=0.1,
        interest_rate=0.06,
        loan_term=30,
        annual_property_growth_rate=0.03,
        annual_property_expenses_percent=0.01,
        upfront_costs=3_000,
        is_first_home_buyer=False,
        analysis_years=12,
    )

    btr = calc.calculate_buy_to_rent_scenario(
        investment_property_price=600_000,
        deposit_percent=0.1,
        interest_rate=0.06,
        loan_term=30,
        weekly_rental_income=500,
        your_weekly_rent=450,
        annual_property_growth_rate=0.03,
        annual_rental_inflation_rate=0.025,
        annual_property_expenses_percent=0.01,
        upfront_costs=3_000,
        is_first_home_buyer=False,
        analysis_years=12,
        annual_gross_income=100_000,
        salary_growth_rate=0.03,
    )

    btl_housing_costs = [row['annual_housing_cost'] for row in btl['yearly_analysis']]
    ri = calc.calculate_rent_and_invest_scenario(
        equivalent_property_price=800_000,
        deposit_percent=0.1,
        your_weekly_rent=450,
        annual_stock_return_rate=0.07,
        annual_rental_inflation_rate=0.025,
        upfront_costs=3_000,
        is_first_home_buyer=False,
        analysis_years=12,
        btl_housing_costs=btl_housing_costs,
    )

    assert len(btl['yearly_analysis']) == 12
    assert len(btr['yearly_analysis']) == 12
    assert len(ri['yearly_analysis']) == 12
