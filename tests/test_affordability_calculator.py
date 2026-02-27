from src.domain.property.affordability import AffordabilityCalculator


def test_affordability_solver_respects_constraints():
    calc = AffordabilityCalculator()

    result = calc.solve_max_property_price(
        cash_available=150000,
        max_borrowing=977000,
        allowed_lvr=0.90,
        upfront_costs=3000,
        is_first_home_buyer=False,
        include_lmi=False,
    )

    assert result["feasible"] is True
    assert result["property_price"] > 0
    assert result["loan_amount"] <= 977000 + 1e-6
    assert result["achieved_lvr"] <= 0.90 + 1e-6
    assert result["cash_used"] <= 150000 + 1e-6


def test_lmi_cost_reduces_affordable_price_when_high_lvr():
    calc = AffordabilityCalculator()

    no_lmi = calc.solve_max_property_price(
        cash_available=150000,
        max_borrowing=977000,
        allowed_lvr=0.90,
        upfront_costs=3000,
        include_lmi=False,
    )
    with_lmi = calc.solve_max_property_price(
        cash_available=150000,
        max_borrowing=977000,
        allowed_lvr=0.90,
        upfront_costs=3000,
        include_lmi=True,
    )

    assert no_lmi["feasible"] is True
    assert with_lmi["feasible"] is True
    assert with_lmi["lmi_cost"] > 0
    assert with_lmi["property_price"] < no_lmi["property_price"]


def test_solver_returns_infeasible_for_too_little_cash_and_borrowing():
    calc = AffordabilityCalculator()

    result = calc.solve_max_property_price(
        cash_available=0,
        max_borrowing=100000,
        allowed_lvr=0.50,
        upfront_costs=10000,
    )

    assert result["feasible"] is False
    assert "Insufficient" in result["reason"]


def test_no_lmi_when_disabled_even_at_95_lvr():
    calc = AffordabilityCalculator()

    result = calc.solve_max_property_price(
        cash_available=150000,
        max_borrowing=977000,
        allowed_lvr=0.95,
        upfront_costs=3000,
        is_first_home_buyer=True,
        include_lmi=False,
    )

    assert result["feasible"] is True
    assert result["lmi_cost"] == 0
