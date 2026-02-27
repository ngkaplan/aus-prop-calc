"""
Affordability solver for back-solving maximum purchasable property values.
"""

from typing import Dict, Any
from .stamp_duty import StampDutyCalculator
from .lmi import LmiCalculator


class AffordabilityCalculator:
    """Back-solve max property price from cash, borrowing, and LVR constraints."""

    def __init__(self):
        self.stamp_duty_calc = StampDutyCalculator()
        self.lmi_calc = LmiCalculator()

    def solve_max_property_price(
        self,
        cash_available: float,
        max_borrowing: float,
        allowed_lvr: float,
        upfront_costs: float,
        is_first_home_buyer: bool = False,
        include_lmi: bool = False,
    ) -> Dict[str, Any]:
        """
        Compute the maximum property value under borrowing + cash constraints.
        """
        if cash_available < 0 or max_borrowing < 0 or upfront_costs < 0:
            return self._infeasible_result("Inputs must be non-negative.")
        if allowed_lvr <= 0 or allowed_lvr > 1.0:
            return self._infeasible_result("Allowed LVR must be between 0% and 100%.")

        high = max(cash_available + max_borrowing, 1.0)
        low = 0.0
        best = None

        for _ in range(80):
            mid = (low + high) / 2.0
            snapshot = self._evaluate_candidate(
                property_price=mid,
                cash_available=cash_available,
                max_borrowing=max_borrowing,
                allowed_lvr=allowed_lvr,
                upfront_costs=upfront_costs,
                is_first_home_buyer=is_first_home_buyer,
                include_lmi=include_lmi,
            )
            if snapshot["feasible"]:
                best = snapshot
                low = mid
            else:
                high = mid

        if not best:
            return self._infeasible_result(
                "Insufficient cash/borrowing capacity after deposit and transaction costs."
            )

        return {
            "feasible": True,
            "property_price": best["property_price"],
            "loan_amount": best["loan_amount"],
            "cash_used": best["cash_required"],
            "cash_remaining": cash_available - best["cash_required"],
            "stamp_duty": best["stamp_duty"],
            "upfront_costs": upfront_costs,
            "lmi_cost": best["lmi_cost"],
            "achieved_lvr": best["loan_amount"] / best["property_price"] if best["property_price"] else 0.0,
            "reason": "",
        }

    def _evaluate_candidate(
        self,
        property_price: float,
        cash_available: float,
        max_borrowing: float,
        allowed_lvr: float,
        upfront_costs: float,
        is_first_home_buyer: bool,
        include_lmi: bool,
    ) -> Dict[str, Any]:
        stamp_duty = self.stamp_duty_calc.calculate_stamp_duty(property_price, is_first_home_buyer)
        max_loan_by_lvr = property_price * allowed_lvr
        loan_amount = min(max_borrowing, max_loan_by_lvr, property_price)

        lmi_cost = self.lmi_calc.estimate_lmi(property_price, loan_amount) if include_lmi else 0.0
        deposit = property_price - loan_amount
        cash_required = deposit + stamp_duty + upfront_costs + lmi_cost
        feasible = cash_required <= cash_available + 1e-6

        return {
            "feasible": feasible,
            "property_price": property_price,
            "loan_amount": loan_amount,
            "cash_required": cash_required,
            "stamp_duty": stamp_duty,
            "lmi_cost": lmi_cost,
        }

    def _infeasible_result(self, reason: str) -> Dict[str, Any]:
        return {
            "feasible": False,
            "property_price": 0.0,
            "loan_amount": 0.0,
            "cash_used": 0.0,
            "cash_remaining": 0.0,
            "stamp_duty": 0.0,
            "upfront_costs": 0.0,
            "lmi_cost": 0.0,
            "achieved_lvr": 0.0,
            "reason": reason,
        }
