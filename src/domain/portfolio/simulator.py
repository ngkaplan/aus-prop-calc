"""
Stage 3 portfolio growth simulator with serviceability and purchase checks.
"""

from dataclasses import dataclass
from typing import Dict, Any, List

from ..property.mortgage import MortgageCalculator
from ..property.stamp_duty import StampDutyCalculator
from ..property.lmi import LmiCalculator
from ..tax.australian_tax import AustralianTaxCalculator


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
        self.tax_calc = AustralianTaxCalculator()

    def simulate(self, params: Dict[str, Any], analysis_years: int) -> Dict[str, Any]:
        assessment_rate = max(
            params["current_interest_rate"] + params["assessment_buffer_rate"],
            params["assessment_rate_floor"],
        )
        effective_lvr = params["allowed_lvr"]
        if effective_lvr > 0.80 and not params["include_lmi_above_80"]:
            effective_lvr = 0.80
        periods_per_year = 4 if params.get("review_frequency") == "Quarterly" else 1
        months_per_period = 12 / periods_per_year

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

        existing_home_property_value = max(
            0.0,
            params["existing_home_loan_balance"] + params.get("existing_home_equity", 0.0),
        )
        existing_investment_property_value = max(
            0.0,
            params.get("existing_investment_property_value", 0.0),
        )

        owned_investment_properties: List[Dict[str, Any]] = []
        yearly_projection: List[Dict[str, Any]] = []
        purchases: List[Dict[str, Any]] = []
        stop_reason_code = ""
        stop_reason = ""
        stop_year = None

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

            purchases_this_year = 0
            total_gross_rent = 0.0
            net_rent = 0.0
            management_fees = 0.0
            vacancy_loss = 0.0
            annual_insurance_cost = 0.0
            annual_maintenance_cost = 0.0
            annual_other_running_costs = 0.0
            annual_land_tax = 0.0
            monthly_surplus = 0.0
            additional_capacity = 0.0
            monthly_actual_mortgage = 0.0
            required_buffer = 0.0
            purchase_reason = "No purchase checks executed."
            purchase_reason_code = "NO_REVIEW_WINDOW"
            stop_triggered = False

            for period in range(periods_per_year):
                existing_external_rent = (params["existing_weekly_rental_income"] * 52) * (
                    (1 + params["rental_income_growth_rate"]) ** years_elapsed
                )
                portfolio_gross_rent = sum(p["annual_rent_gross"] for p in owned_investment_properties)
                total_gross_rent = existing_external_rent + portfolio_gross_rent
                total_investment_property_value = existing_investment_property_value + sum(
                    p["current_value"] for p in owned_investment_properties
                )
                collected_rent = total_gross_rent * (1 - params["average_vacancy_rate"])
                management_fees = (
                    collected_rent * params["property_management_fee_rate"]
                    if params["use_property_manager"]
                    else 0.0
                )
                annual_insurance_cost = (
                    total_investment_property_value * params["annual_insurance_percent_of_value"]
                )
                annual_maintenance_cost = (
                    total_investment_property_value * params["annual_maintenance_percent_of_value"]
                )
                annual_other_running_costs = (
                    collected_rent * params["other_running_cost_percent_of_rent"]
                )
                annual_land_tax = 0.0
                if params["apply_nsw_land_tax"]:
                    taxable_land_value = max(
                        0.0, total_investment_property_value - params["nsw_land_tax_threshold"]
                    )
                    annual_land_tax = taxable_land_value * params["nsw_land_tax_rate"]
                annual_non_finance_costs = (
                    management_fees
                    + annual_insurance_cost
                    + annual_maintenance_cost
                    + annual_other_running_costs
                    + annual_land_tax
                )
                net_rent_before_interest = collected_rent - annual_non_finance_costs
                vacancy_loss = total_gross_rent - collected_rent
                net_rent_for_assessment = max(0.0, net_rent_before_interest)
                shaded_rent = net_rent_for_assessment * params["rental_income_haircut"]
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

                period_cashflow = (
                    (salary_income / periods_per_year)
                    + (net_rent_before_interest / periods_per_year)
                    - (monthly_actual_mortgage * months_per_period)
                    - (params["other_monthly_debt_commitments"] * months_per_period)
                    - (living_expenses_monthly * months_per_period)
                )
                cash_balance += period_cashflow

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

                period_elapsed_years = years_elapsed + (period / periods_per_year)
                target_price = params["base_investment_purchase_price"] * (
                    (1 + params["new_purchase_price_growth_rate"]) ** period_elapsed_years
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
                purchase_reason_code = "PURCHASED"
                should_purchase = True
                if candidate_loan <= 0:
                    should_purchase = False
                    purchase_reason_code = "SERVICEABILITY_CAPACITY_ZERO"
                    purchase_reason = "No serviceability capacity for additional borrowing."
                elif cash_balance < acquisition_cost:
                    should_purchase = False
                    purchase_reason_code = "INSUFFICIENT_CASH_FOR_ACQUISITION"
                    purchase_reason = "Insufficient cash for deposit and acquisition costs."
                elif post_purchase_cash < required_buffer:
                    should_purchase = False
                    purchase_reason_code = "POST_PURCHASE_BUFFER_BREACH"
                    purchase_reason = "Post-purchase cash buffer below required threshold."

                if should_purchase:
                    purchases_this_year += 1
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
                            "current_value": target_price,
                            "annual_rent_gross": annual_rent,
                        }
                    )
                    purchases.append(
                        {
                            "year": year,
                            "review_period": period + 1,
                            "purchase_price": target_price,
                            "loan_amount": candidate_loan,
                            "deposit": deposit,
                            "stamp_duty": stamp_duty,
                            "lmi_cost": lmi_cost,
                            "upfront_costs": params["upfront_costs_per_purchase"],
                            "cash_after_purchase": cash_balance,
                        }
                    )

                baseline_required_buffer = params["cash_buffer_months"] * (
                    assessed_living_monthly
                    + monthly_actual_mortgage
                    + params["other_monthly_debt_commitments"]
                )
                if cash_balance < 0:
                    stop_triggered = True
                    stop_reason_code = "BANKRUPTCY_NEGATIVE_CASH"
                    stop_reason = "Cash balance dropped below zero."
                    stop_year = year
                    break
                if cash_balance < baseline_required_buffer:
                    stop_triggered = True
                    stop_reason_code = "ERODED_BUFFER"
                    stop_reason = "Cash balance dropped below required minimum buffer."
                    stop_year = year
                    break

            annual_investment_interest = sum(
                l.current_balance(self.mortgage_calc) * l.annual_rate for l in investment_loans
            )
            annual_non_finance_costs = (
                management_fees
                + annual_insurance_cost
                + annual_maintenance_cost
                + annual_other_running_costs
                + annual_land_tax
            )
            taxable_rental_profit = total_gross_rent - annual_non_finance_costs - annual_investment_interest
            gearing_tax_impact = 0.0
            if params.get("apply_gearing_tax_effects", True):
                marginal_rate = self.tax_calc.calculate_marginal_tax_rate(salary_income)
                gearing_tax_impact = -taxable_rental_profit * marginal_rate
                cash_balance += gearing_tax_impact
                if not stop_triggered:
                    if cash_balance < 0:
                        stop_triggered = True
                        stop_reason_code = "BANKRUPTCY_NEGATIVE_CASH"
                        stop_reason = "Cash balance dropped below zero after gearing tax impact."
                        stop_year = year
                    elif cash_balance < baseline_required_buffer:
                        stop_triggered = True
                        stop_reason_code = "ERODED_BUFFER"
                        stop_reason = (
                            "Cash balance dropped below required minimum buffer after gearing tax impact."
                        )
                        stop_year = year

            total_debt_balance = (
                sum(l.current_balance(self.mortgage_calc) for l in home_loans)
                + sum(l.current_balance(self.mortgage_calc) for l in investment_loans)
            )
            total_property_value = (
                existing_home_property_value
                + existing_investment_property_value
                + sum(p["current_value"] for p in owned_investment_properties)
            )
            weighted_portfolio_lvr = (
                total_debt_balance / total_property_value if total_property_value > 0 else 0.0
            )
            dti_existing = total_debt_balance / salary_income if salary_income > 0 else 0.0
            baseline_required_buffer = params["cash_buffer_months"] * (
                assessed_living_monthly + monthly_actual_mortgage + params["other_monthly_debt_commitments"]
            )

            yearly_projection.append(
                {
                    "year": year,
                    "assessment_rate": assessment_rate,
                    "salary_income": salary_income,
                    "total_rent_income_gross": total_gross_rent,
                    "total_rent_income_net_before_interest": net_rent_before_interest,
                    "vacancy_loss": total_gross_rent - collected_rent,
                    "property_management_fees": management_fees,
                    "insurance_costs": annual_insurance_cost,
                    "maintenance_costs": annual_maintenance_cost,
                    "other_running_costs": annual_other_running_costs,
                    "land_tax_costs": annual_land_tax,
                    "investment_interest_costs": annual_investment_interest,
                    "taxable_rental_profit": taxable_rental_profit,
                    "gearing_tax_impact": gearing_tax_impact,
                    "assessed_income": assessed_income,
                    "monthly_surplus": monthly_surplus,
                    "additional_borrowing_capacity": additional_capacity,
                    "cash_balance_end_year": cash_balance,
                    "target_purchase_price": target_price,
                    "required_cash_for_purchase": acquisition_cost,
                    "buffer_required": required_buffer,
                    "baseline_buffer_required": baseline_required_buffer,
                    "purchase_made": purchases_this_year > 0,
                    "purchase_reason": (
                        "Purchased"
                        if purchases_this_year > 0
                        else (purchase_reason if purchase_reason else "No purchase made.")
                    ),
                    "purchase_reason_code": (
                        "PURCHASED" if purchases_this_year > 0 else purchase_reason_code
                    ),
                    "purchases_this_year": purchases_this_year,
                    "investment_property_count": len(owned_investment_properties),
                    "total_debt_balance": total_debt_balance,
                    "total_property_value": total_property_value,
                    "weighted_portfolio_lvr": weighted_portfolio_lvr,
                    "dti_existing": dti_existing,
                    "stop_triggered": stop_triggered,
                    "stop_reason_code": stop_reason_code if stop_triggered else "",
                    "stop_reason": stop_reason if stop_triggered else "",
                }
            )

            if stop_triggered:
                break

            for loan in home_loans:
                loan.advance_year()
            for loan in investment_loans:
                loan.advance_year()
            for prop in owned_investment_properties:
                prop["annual_rent_gross"] *= 1 + params["rental_income_growth_rate"]
                prop["current_value"] *= 1 + params["new_purchase_price_growth_rate"]
            existing_home_property_value *= 1 + params["new_purchase_price_growth_rate"]
            existing_investment_property_value *= 1 + params["new_purchase_price_growth_rate"]

        return {
            "yearly_projection": yearly_projection,
            "purchases": purchases,
            "final_cash_balance": cash_balance,
            "final_property_count": len(owned_investment_properties),
            "assessment_rate": assessment_rate,
            "effective_lvr": effective_lvr,
            "review_frequency": params.get("review_frequency", "Yearly"),
            "stop_reason_code": stop_reason_code,
            "stop_reason": stop_reason,
            "stop_year": stop_year,
            "stopped_early": stop_year is not None,
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
