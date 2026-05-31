from src.domain.property.mortgage import MortgageCalculator
from src.domain.property.stamp_duty import StampDutyCalculator
from src.domain.tax.australian_tax import AustralianTaxCalculator


def test_mortgage_zero_interest_payment_and_balance():
    calc = MortgageCalculator()
    payment = calc.calculate_monthly_payment(120_000, 0.0, 20)
    assert payment == 500

    remaining = calc.calculate_remaining_balance(120_000, 0.0, 20, 10)
    assert remaining == 60_000


def test_stamp_duty_first_home_buyer_thresholds():
    calc = StampDutyCalculator()
    assert calc.calculate_stamp_duty(799_999, True) == 0

    at_full = calc.calculate_stamp_duty(1_000_000, True)
    standard = calc.calculate_stamp_duty(1_000_000, False)
    assert at_full == standard


def test_negative_gearing_benefit_only_when_loss():
    calc = AustralianTaxCalculator()
    assert calc.calculate_negative_gearing_benefit(30_000, 20_000, 0.39) == 3900
    assert calc.calculate_negative_gearing_benefit(20_000, 30_000, 0.39) == 0
