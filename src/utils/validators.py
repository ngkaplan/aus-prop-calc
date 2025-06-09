"""
Input validation utilities for the application.
"""

def validate_positive_number(value: float, name: str) -> float:
    """Validate that a number is positive"""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value

def validate_percentage(value: float, name: str) -> float:
    """Validate that a percentage is between 0 and 1"""
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1, got {value}")
    return value

def validate_property_price(price: float) -> float:
    """Validate property price is reasonable"""
    if price < 100000:
        raise ValueError(f"Property price seems too low: ${price:,.0f}")
    if price > 50000000:
        raise ValueError(f"Property price seems too high: ${price:,.0f}")
    return price

def validate_income(income: float) -> float:
    """Validate annual income is reasonable"""
    if income < 0:
        raise ValueError(f"Income cannot be negative: ${income:,.0f}")
    if income > 10000000:
        raise ValueError(f"Income seems unreasonably high: ${income:,.0f}")
    return income 