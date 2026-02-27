from src.domain.portfolio.serviceability import ServiceabilityCalculator


def _base_projection(**overrides):
    calc = ServiceabilityCalculator()
    params = {
        "annual_gross_income": 120000,
        "salary_growth_rate": 0.03,
        "existing_weekly_rental_income": 0,
        "rental_income_growth_rate": 0.025,
        "average_vacancy_rate": 0.03,
        "property_management_fee_rate": 0.07,
        "monthly_living_expenses": 4000,
        "monthly_expense_growth_rate": 0.025,
        "bank_expense_floor_monthly": 3000,
        "other_monthly_debt_commitments": 0,
        "current_interest_rate": 0.06,
        "assessment_buffer_rate": 0.03,
        "assessment_rate_floor": 0.09,
        "enforce_dti_cap": False,
        "dti_cap": 99.0,
        "rental_income_haircut": 0.80,
        "existing_home_loan_balance": 0,
        "existing_home_loan_term_remaining": 25,
        "existing_investment_loan_balance": 0,
        "existing_investment_loan_term_remaining": 25,
        "new_loan_term_years": 30,
        "analysis_years": 5,
    }
    params.update(overrides)
    return calc.project_capacity(**params)


def test_assessment_rate_uses_floor_when_needed():
    projection = _base_projection(current_interest_rate=0.04, assessment_buffer_rate=0.03, assessment_rate_floor=0.09)
    assert abs(projection["assessment_rate"] - 0.09) < 1e-9


def test_assessment_rate_uses_buffer_when_above_floor():
    projection = _base_projection(current_interest_rate=0.07, assessment_buffer_rate=0.03, assessment_rate_floor=0.09)
    assert abs(projection["assessment_rate"] - 0.10) < 1e-9


def test_expense_floor_reduces_capacity():
    low_floor = _base_projection(
        monthly_living_expenses=2000,
        bank_expense_floor_monthly=2000,
    )["yearly_projection"][0]["additional_borrowing_capacity"]
    high_floor = _base_projection(
        monthly_living_expenses=2000,
        bank_expense_floor_monthly=5000,
    )["yearly_projection"][0]["additional_borrowing_capacity"]
    assert high_floor < low_floor


def test_existing_debt_commitments_reduce_capacity():
    no_debt = _base_projection(
        existing_home_loan_balance=0,
        existing_investment_loan_balance=0,
    )["yearly_projection"][0]["additional_borrowing_capacity"]
    with_debt = _base_projection(
        existing_home_loan_balance=500000,
        existing_investment_loan_balance=350000,
    )["yearly_projection"][0]["additional_borrowing_capacity"]
    assert with_debt < no_debt


def test_rental_income_haircut_increases_capacity_when_rent_exists():
    low_haircut = _base_projection(
        existing_weekly_rental_income=900,
        rental_income_haircut=0.60,
    )["yearly_projection"][0]["additional_borrowing_capacity"]
    high_haircut = _base_projection(
        existing_weekly_rental_income=900,
        rental_income_haircut=0.80,
    )["yearly_projection"][0]["additional_borrowing_capacity"]
    assert high_haircut > low_haircut


def test_vacancy_and_management_reduce_capacity():
    low_cost = _base_projection(
        existing_weekly_rental_income=900,
        average_vacancy_rate=0.0,
        property_management_fee_rate=0.0,
    )["yearly_projection"][0]["additional_borrowing_capacity"]
    high_cost = _base_projection(
        existing_weekly_rental_income=900,
        average_vacancy_rate=0.08,
        property_management_fee_rate=0.08,
    )["yearly_projection"][0]["additional_borrowing_capacity"]
    assert high_cost < low_cost


def test_dti_cap_limits_capacity():
    uncapped = _base_projection(
        enforce_dti_cap=False,
        dti_cap=99.0,
        annual_gross_income=189000,
    )["yearly_projection"][0]
    capped = _base_projection(
        enforce_dti_cap=True,
        dti_cap=5.0,
        annual_gross_income=189000,
    )["yearly_projection"][0]
    assert capped["additional_borrowing_capacity"] <= uncapped["additional_borrowing_capacity"]
