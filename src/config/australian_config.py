"""
Australian-specific configuration including tax brackets, stamp duty rates, and other constants.
"""

# 2023-24 Australian Tax Brackets
TAX_BRACKETS = [
    {"min": 0, "max": 18200, "rate": 0.0, "base": 0},
    {"min": 18201, "max": 45000, "rate": 0.19, "base": 0},
    {"min": 45001, "max": 120000, "rate": 0.325, "base": 5092},
    {"min": 120001, "max": 180000, "rate": 0.37, "base": 29467},
    {"min": 180001, "max": float('inf'), "rate": 0.45, "base": 51667}
]

# Medicare Levy
MEDICARE_LEVY_RATE = 0.02
MEDICARE_LEVY_THRESHOLD = 24276

# Capital Gains Tax
CGT_DISCOUNT_RATE = 0.5  # 50% discount for assets held > 12 months
CGT_MIN_HOLDING_PERIOD_MONTHS = 12

# Stamp Duty Brackets (NSW-style)
STAMP_DUTY_BRACKETS = [
    {"min": 0, "max": 17000, "rate": 0.0125, "base": 0, "min_amount": 20},
    {"min": 17001, "max": 36000, "rate": 0.015, "base": 212},
    {"min": 36001, "max": 97000, "rate": 0.0175, "base": 497},
    {"min": 97001, "max": 364000, "rate": 0.035, "base": 1564},
    {"min": 364001, "max": 1212000, "rate": 0.045, "base": 10909},
    {"min": 1212001, "max": 3636000, "rate": 0.055, "base": 49069},
    {"min": 3636001, "max": float('inf'), "rate": 0.07, "base": 182390}
]

# First Home Buyer Concessions
FHB_STAMP_DUTY_EXEMPT_THRESHOLD = 800000  # No stamp duty under this amount
FHB_STAMP_DUTY_FULL_THRESHOLD = 1000000   # Full stamp duty over this amount

# Property Investment Constants
WEEKS_PER_YEAR = 52
MONTHS_PER_YEAR = 12 