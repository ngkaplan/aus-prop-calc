"""
Loan Mortgage Insurance (LMI) estimation utilities.
"""


class LmiCalculator:
    """Estimate LMI cost for high-LVR loans."""

    # Simplified market-style bands for estimation.
    _LVR_BANDS = [
        (0.80, 0.000),
        (0.85, 0.005),
        (0.90, 0.012),
        (0.95, 0.024),
        (1.00, 0.036),
    ]

    def estimate_lmi(self, property_price: float, loan_amount: float) -> float:
        """
        Estimate LMI payable based on LVR.

        Args:
            property_price: Purchase price of the property
            loan_amount: Loan principal amount

        Returns:
            Estimated LMI amount
        """
        if property_price <= 0 or loan_amount <= 0:
            return 0.0

        lvr = loan_amount / property_price
        if lvr <= 0.80:
            return 0.0

        rate = self._LVR_BANDS[-1][1]
        for max_lvr, band_rate in self._LVR_BANDS:
            if lvr <= max_lvr:
                rate = band_rate
                break

        return loan_amount * rate
