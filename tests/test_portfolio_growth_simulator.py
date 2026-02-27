from src.domain.portfolio.simulator import PortfolioGrowthSimulator


def _base_params(**overrides):
    params = {
        "annual_gross_income": 180000,
        "salary_growth_rate": 0.03,
        "existing_weekly_rental_income": 0,
        "rental_income_growth_rate": 0.025,
        "average_vacancy_rate": 0.03,
        "use_property_manager": True,
        "property_management_fee_rate": 0.07,
        "monthly_living_expenses": 3500,
        "monthly_expense_growth_rate": 0.02,
        "bank_expense_floor_monthly": 3000,
        "other_monthly_debt_commitments": 0,
        "current_interest_rate": 0.06,
        "assessment_buffer_rate": 0.03,
        "assessment_rate_floor": 0.09,
        "rental_income_haircut": 0.8,
        "existing_home_loan_balance": 0,
        "existing_home_loan_term_remaining": 25,
        "existing_investment_loan_balance": 0,
        "existing_investment_loan_term_remaining": 25,
        "existing_investment_equity": 0,
        "new_loan_term_years": 30,
        "starting_cash_available": 180000,
        "allowed_lvr": 0.90,
        "include_lmi_above_80": True,
        "upfront_costs_per_purchase": 3000,
        "cash_buffer_months": 6,
        "base_investment_purchase_price": 450000,
        "new_purchase_price_growth_rate": 0.03,
        "new_purchase_gross_rental_yield": 0.055,
    }
    params.update(overrides)
    return params


def test_simulator_executes_purchase_when_constraints_pass():
    sim = PortfolioGrowthSimulator()
    result = sim.simulate(_base_params(), analysis_years=5)
    assert len(result["purchases"]) >= 1


def test_simulator_blocks_purchase_when_cash_is_insufficient():
    sim = PortfolioGrowthSimulator()
    result = sim.simulate(
        _base_params(
            starting_cash_available=1000,
            annual_gross_income=80000,
            monthly_living_expenses=5000,
            base_investment_purchase_price=700000,
        ),
        analysis_years=3,
    )
    assert len(result["purchases"]) == 0
    assert any(
        "Insufficient cash" in row["purchase_reason"] or "buffer" in row["purchase_reason"]
        for row in result["yearly_projection"]
    )


def test_simulator_caps_lvr_to_80_when_lmi_disabled():
    sim = PortfolioGrowthSimulator()
    result = sim.simulate(
        _base_params(
            allowed_lvr=0.95,
            include_lmi_above_80=False,
        ),
        analysis_years=2,
    )
    assert abs(result["effective_lvr"] - 0.80) < 1e-9


def test_vacancy_and_management_reduce_final_cash():
    sim = PortfolioGrowthSimulator()
    low_cost = sim.simulate(
        _base_params(
            average_vacancy_rate=0.0,
            use_property_manager=False,
            property_management_fee_rate=0.0,
        ),
        analysis_years=5,
    )
    high_cost = sim.simulate(
        _base_params(
            average_vacancy_rate=0.10,
            use_property_manager=True,
            property_management_fee_rate=0.10,
        ),
        analysis_years=5,
    )
    assert high_cost["final_cash_balance"] < low_cost["final_cash_balance"]


def test_simulator_stops_early_on_bankruptcy():
    sim = PortfolioGrowthSimulator()
    result = sim.simulate(
        _base_params(
            annual_gross_income=50000,
            monthly_living_expenses=9000,
            starting_cash_available=5000,
            base_investment_purchase_price=1000000,
        ),
        analysis_years=10,
    )
    assert result["stopped_early"] is True
    assert result["stop_reason_code"] == "BANKRUPTCY_NEGATIVE_CASH"
    assert result["stop_year"] is not None


def test_simulator_stops_early_on_eroded_buffer():
    sim = PortfolioGrowthSimulator()
    result = sim.simulate(
        _base_params(
            annual_gross_income=100000,
            monthly_living_expenses=3500,
            bank_expense_floor_monthly=8000,
            starting_cash_available=60000,
            cash_buffer_months=18,
            base_investment_purchase_price=700000,
            include_lmi_above_80=False,
            allowed_lvr=0.8,
        ),
        analysis_years=10,
    )
    assert result["stopped_early"] is True
    assert result["stop_reason_code"] == "ERODED_BUFFER"


def test_existing_equity_reduces_initial_weighted_lvr():
    sim = PortfolioGrowthSimulator()
    no_equity = sim.simulate(
        _base_params(
            existing_investment_loan_balance=400000,
            existing_investment_equity=0,
        ),
        analysis_years=1,
    )
    with_equity = sim.simulate(
        _base_params(
            existing_investment_loan_balance=400000,
            existing_investment_equity=400000,
        ),
        analysis_years=1,
    )
    lvr_no_equity = no_equity["yearly_projection"][0]["weighted_portfolio_lvr"]
    lvr_with_equity = with_equity["yearly_projection"][0]["weighted_portfolio_lvr"]
    assert lvr_with_equity < lvr_no_equity
