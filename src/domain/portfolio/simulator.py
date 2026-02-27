"""
Stage 3 portfolio growth simulator with serviceability and purchase checks.
"""

from dataclasses import dataclass
from typing import Dict, Any, List

from ..property.mortgage import MortgageCalculator
from ..property.stamp_duty import StampDutyCalculator
from ..property.lmi import LmiCalculator


@dataclass
class LoanPosition:
    principal_at_start: float
    annual_rate: float
    term_years: int
    years_paid: int = 0

    def current_balance(self, mortgage_calc: MortgageCalculator) -> float:
        return mortgage_calc.calculate_remaining_balance(
            principal=self.principal_at_start,
            annual_rate=self.annual_rate,
            years=self.term_years,
            years_paid=self.years_paid,
        )

    def monthly_payment(self, mortgage_calc: MortgageCalculator) -> float:
        return mortgage_calc.calculate_monthly_payment(
            principal=self.principal_at_start,
            annual_rate=self.annual_rate,
            years=self.term_years,
        )

    def assessed_monthly_payment(
        self, mortgage_calc: MortgageCalculator, assessment_rate: float
    ) -> float:
        balance = self.current_balance(mortgage_calc)
        remaining_term = max(1, self.term_years - self.years_paid)
        return mortgage_calc.calculate_monthly_payment(
            principal=balance,
            annual_rate=assessment_rate,
            years=remaining_term,
        )

    def advance_year(self):
        if self.years_paid < self.term_years:
            self.years_paid += 1


class PortfolioGrowthSimulator:
    """Simulate additional investment purchases over time."""

    def __init__(self):
        self.mortgage_calc = MortgageCalculator()
        self.stamp_duty_calc = StampDutyCalculator()
        self.lmi_calc = LmiCalculator()

    def simulate(self, params: Dict[str, Any], analysis_years: int) -> Dict[str, Any]:
        assessment_rate = max(
            params["current_interest_rate"] + params["assessment_buffer_rate"],
            params["assessment_rate_floor"],
        )
        effective_lvr = params["allowed_lvr"]
        if effective_lvr > 0.80 and not params["include_lmi_above_80"]:
            effective_lvr = 0.80

        cash_balance = float(params["starting_cash_available"])
        investment_loans: List[LoanPosition] = []
        if params["existing_investment_loan_balance"] > 0:
            investment_loans.append(
                LoanPosition(
                    principal_at_start=params["existing_investment_loan_balance"],
                    annual_rate=params["current_interest_rate"],
                    term_years=params["existing_investment_loan_term_remaining"],
                )
            )
        home_loans: List[LoanPosition] = []
        if params["existing_home_loan_balance"] > 0:
            home_loans.append(
                LoanPosition(
                    principal_at_start=params["existing_home_loan_balance"],
                    annual_rate=params["current_interest_rate"],
                    term_years=params["existing_home_loan_term_remaining"],
                )
            )

        owned_investment_properties: List[Dict[str, Any]] = []
        yearly_projection: List[Dict[str, Any]] = []
        purchases: List[Dict[str, Any]] = []

        for year in range(1, analysis_years + 1):
            years_elapsed = year - 1
            salary_income = params["annual_gross_income"] * (
                (1 + params["salary_growth_rate"]) ** years_elapsed
            )
            living_expenses_monthly = params["monthly_living_expenses"] * (
                (1 + params["monthly_expense_growth_rate"]) ** years_elapsed
            )
            assessed_living_monthly = max(
                living_expenses_monthly, params["bank_expense_floor_monthly"]
            )

            existing_external_rent = (params["existing_weekly_rental_income"] * 52) * (
                (1 + params["rental_income_growth_rate"]) ** years_elapsed
            )
            portfolio_rent = sum(p["annual_rent"] for p in owned_investment_properties)
            total_rent = existing_external_rent + portfolio_rent
            shaded_rent = total_rent * params["rental_income_haircut"]
            assessed_income = salary_income + shaded_rent

            monthly_actual_mortgage = (
                sum(l.monthly_payment(self.mortgage_calc) for l in home_loans)
                + sum(l.monthly_payment(self.mortgage_calc) for l in investment_loans)
            )
            monthly_assessed_mortgage = (
                sum(
                    l.assessed_monthly_payment(self.mortgage_calc, assessment_rate)
                    for l in home_loans
                )
                + sum(
                    l.assessed_monthly_payment(self.mortgage_calc, assessment_rate)
                    for l in investment_loans
                )
            )

            annual_cashflow = (
                salary_income
                + total_rent
                - (monthly_actual_mortgage * 12)
                - (params["other_monthly_debt_commitments"] * 12)
                - (living_expenses_monthly * 12)
            )
            cash_balance += annual_cashflow

            monthly_surplus = (
                assessed_income / 12
                - assessed_living_monthly
                - monthly_assessed_mortgage
                - params["other_monthly_debt_commitments"]
            )
            additional_capacity = self._principal_from_payment(
                monthly_payment=max(0.0, monthly_surplus),
                annual_rate=assessment_rate,
                years=params["new_loan_term_years"],
            )

            target_price = params["base_investment_purchase_price"] * (
                (1 + params["new_purchase_price_growth_rate"]) ** years_elapsed
            )
            lvr_loan_cap = target_price * effective_lvr
            candidate_loan = min(lvr_loan_cap, additional_capacity)
            deposit = max(0.0, target_price - candidate_loan)
            stamp_duty = self.stamp_duty_calc.calculate_stamp_duty(target_price, False)
            lmi_cost = (
                self.lmi_calc.estimate_lmi(target_price, candidate_loan)
                if params["include_lmi_above_80"] and effective_lvr > 0.80
                else 0.0
            )
            acquisition_cost = (
                deposit + stamp_duty + params["upfront_costs_per_purchase"] + lmi_cost
            )
            new_loan_monthly = self.mortgage_calc.calculate_monthly_payment(
                principal=candidate_loan,
                annual_rate=params["current_interest_rate"],
                years=params["new_loan_term_years"],
            )
            required_buffer = params["cash_buffer_months"] * (
                assessed_living_monthly + monthly_actual_mortgage + new_loan_monthly
            )
            post_purchase_cash = cash_balance - acquisition_cost

            purchase_reason = ""
            should_purchase = True
            if candidate_loan <= 0:
                should_purchase = False
                purchase_reason = "No serviceability capacity for additional borrowing."
            elif cash_balance < acquisition_cost:
                should_purchase = False
                purchase_reason = "Insufficient cash for deposit and acquisition costs."
            elif post_purchase_cash < required_buffer:
                should_purchase = False
                purchase_reason = "Post-purchase cash buffer below required threshold."

            if should_purchase:
                cash_balance = post_purchase_cash
                investment_loans.append(
                    LoanPosition(
                        principal_at_start=candidate_loan,
                        annual_rate=params["current_interest_rate"],
                        term_years=params["new_loan_term_years"],
                    )
                )
                annual_rent = target_price * params["new_purchase_gross_rental_yield"]
                owned_investment_properties.append(
                    {
                        "purchase_year": year,
                        "purchase_price": target_price,
                        "annual_rent": annual_rent,
                    }
                )
                purchases.append(
                    {
                        "year": year,
                        "purchase_price": target_price,
                        "loan_amount": candidate_loan,
                        "deposit": deposit,
                        "stamp_duty": stamp_duty,
                        "lmi_cost": lmi_cost,
                        "upfront_costs": params["upfront_costs_per_purchase"],
                        "cash_after_purchase": cash_balance,
                    }
                )

            total_debt_balance = (
                sum(l.current_balance(self.mortgage_calc) for l in home_loans)
                + sum(l.current_balance(self.mortgage_calc) for l in investment_loans)
            )
            dti_existing = total_debt_balance / salary_income if salary_income > 0 else 0.0

            yearly_projection.append(
                {
                    "year": year,
                    "assessment_rate": assessment_rate,
                    "salary_income": salary_income,
                    "total_rent_income": total_rent,
                    "assessed_income": assessed_income,
                    "monthly_surplus": monthly_surplus,
                    "additional_borrowing_capacity": additional_capacity,
                    "cash_balance_end_year": cash_balance,
                    "target_purchase_price": target_price,
                    "required_cash_for_purchase": acquisition_cost,
                    "buffer_required": required_buffer,
                    "purchase_made": should_purchase,
                    "purchase_reason": purchase_reason if not should_purchase else "Purchased",
                    "investment_property_count": len(owned_investment_properties),
                    "total_debt_balance": total_debt_balance,
                    "dti_existing": dti_existing,
                }
            )

            for loan in home_loans:
                loan.advance_year()
            for loan in investment_loans:
                loan.advance_year()
            for prop in owned_investment_properties:
                prop["annual_rent"] *= 1 + params["rental_income_growth_rate"]

        return {
            "yearly_projection": yearly_projection,
            "purchases": purchases,
            "final_cash_balance": cash_balance,
            "final_property_count": len(owned_investment_properties),
            "assessment_rate": assessment_rate,
            "effective_lvr": effective_lvr,
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
