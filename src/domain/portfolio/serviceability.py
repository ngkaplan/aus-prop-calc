"""
Serviceability projection engine for portfolio-growth planning.
"""

from typing import Dict, Any, List
from ..property.mortgage import MortgageCalculator


class ServiceabilityCalculator:
    """Calculate year-by-year borrowing capacity under lender-style assessment rules."""

    def __init__(self):
        self.mortgage_calc = MortgageCalculator()

    def project_capacity(
        self,
        annual_gross_income: float,
        salary_growth_rate: float,
        existing_weekly_rental_income: float,
        rental_income_growth_rate: float,
        monthly_living_expenses: float,
        monthly_expense_growth_rate: float,
        bank_expense_floor_monthly: float,
        other_monthly_debt_commitments: float,
        current_interest_rate: float,
        assessment_buffer_rate: float,
        assessment_rate_floor: float,
        rental_income_haircut: float,
        existing_home_loan_balance: float,
        existing_home_loan_term_remaining: int,
        existing_investment_loan_balance: float,
        existing_investment_loan_term_remaining: int,
        new_loan_term_years: int,
        analysis_years: int,
    ) -> Dict[str, Any]:
        """Build yearly serviceability metrics and additional borrowing capacity."""
        assessment_rate = max(current_interest_rate + assessment_buffer_rate, assessment_rate_floor)
        yearly_projection: List[Dict[str, Any]] = []

        for year in range(1, analysis_years + 1):
            years_elapsed = year - 1
            salary = annual_gross_income * ((1 + salary_growth_rate) ** years_elapsed)
            gross_rent = (existing_weekly_rental_income * 52) * (
                (1 + rental_income_growth_rate) ** years_elapsed
            )
            shaded_rent = gross_rent * rental_income_haircut
            assessed_income = salary + shaded_rent

            living_expenses_monthly = monthly_living_expenses * (
                (1 + monthly_expense_growth_rate) ** years_elapsed
            )
            assessed_living_monthly = max(living_expenses_monthly, bank_expense_floor_monthly)

            home_repayment = self._assessed_repayment_for_year(
                principal=existing_home_loan_balance,
                actual_rate=current_interest_rate,
                original_term_remaining=existing_home_loan_term_remaining,
                years_elapsed=years_elapsed,
                assessment_rate=assessment_rate,
            )
            investment_repayment = self._assessed_repayment_for_year(
                principal=existing_investment_loan_balance,
                actual_rate=current_interest_rate,
                original_term_remaining=existing_investment_loan_term_remaining,
                years_elapsed=years_elapsed,
                assessment_rate=assessment_rate,
            )

            total_monthly_commitments = (
                assessed_living_monthly
                + home_repayment["monthly_assessed_repayment"]
                + investment_repayment["monthly_assessed_repayment"]
                + other_monthly_debt_commitments
            )
            monthly_income = assessed_income / 12
            monthly_surplus = monthly_income - total_monthly_commitments

            additional_borrowing_capacity = self._principal_from_payment(
                monthly_payment=max(0.0, monthly_surplus),
                annual_rate=assessment_rate,
                years=new_loan_term_years,
            )

            existing_total_debt = (
                home_repayment["current_balance"] + investment_repayment["current_balance"]
            )
            dti_existing = existing_total_debt / salary if salary > 0 else 0.0
            dti_with_capacity = (
                (existing_total_debt + additional_borrowing_capacity) / salary if salary > 0 else 0.0
            )

            yearly_projection.append(
                {
                    "year": year,
                    "assessment_rate": assessment_rate,
                    "salary_income": salary,
                    "gross_rental_income": gross_rent,
                    "shaded_rental_income": shaded_rent,
                    "assessed_income": assessed_income,
                    "monthly_income": monthly_income,
                    "monthly_living_expenses_assessed": assessed_living_monthly,
                    "monthly_home_repayment_assessed": home_repayment["monthly_assessed_repayment"],
                    "monthly_investment_repayment_assessed": investment_repayment[
                        "monthly_assessed_repayment"
                    ],
                    "other_monthly_debt_commitments": other_monthly_debt_commitments,
                    "total_monthly_commitments": total_monthly_commitments,
                    "monthly_surplus": monthly_surplus,
                    "additional_borrowing_capacity": additional_borrowing_capacity,
                    "existing_total_debt": existing_total_debt,
                    "dti_existing": dti_existing,
                    "dti_with_capacity": dti_with_capacity,
                }
            )

        return {
            "assessment_rate": assessment_rate,
            "yearly_projection": yearly_projection,
        }

    def _assessed_repayment_for_year(
        self,
        principal: float,
        actual_rate: float,
        original_term_remaining: int,
        years_elapsed: int,
        assessment_rate: float,
    ) -> Dict[str, float]:
        if principal <= 0 or original_term_remaining <= 0 or years_elapsed >= original_term_remaining:
            return {"current_balance": 0.0, "monthly_assessed_repayment": 0.0}

        current_balance = self.mortgage_calc.calculate_remaining_balance(
            principal=principal,
            annual_rate=actual_rate,
            years=original_term_remaining,
            years_paid=years_elapsed,
        )
        term_remaining = max(1, original_term_remaining - years_elapsed)
        monthly_assessed_repayment = self.mortgage_calc.calculate_monthly_payment(
            principal=current_balance,
            annual_rate=assessment_rate,
            years=term_remaining,
        )
        return {
            "current_balance": current_balance,
            "monthly_assessed_repayment": monthly_assessed_repayment,
        }

    def _principal_from_payment(self, monthly_payment: float, annual_rate: float, years: int) -> float:
        if monthly_payment <= 0 or years <= 0:
            return 0.0

        n = years * 12
        if annual_rate == 0:
            return monthly_payment * n

        r = annual_rate / 12
        factor = (1 + r) ** n
        return monthly_payment * ((factor - 1) / (r * factor))
