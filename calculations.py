"""
Financial calculations for Australian property investment scenarios.
Start simple - just mortgage calculations first.
"""

def calculate_monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    """Calculate monthly mortgage payment using standard formula."""
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    
    if annual_rate == 0:
        return principal / num_payments
    
    monthly_payment = principal * (
        monthly_rate * (1 + monthly_rate) ** num_payments
    ) / ((1 + monthly_rate) ** num_payments - 1)
    
    return monthly_payment


def calculate_buy_to_live_scenario(property_price: float, deposit_percent: float, 
                                  interest_rate: float, loan_term: int) -> dict:
    """
    Calculate the financial outcome for buying a property to live in.
    
    Args:
        property_price: Total property price
        deposit_percent: Deposit as decimal (0.2 for 20%)
        interest_rate: Annual interest rate as decimal (0.06 for 6%)
        loan_term: Loan term in years
    
    Returns:
        Dictionary with calculation results
    """
    deposit = property_price * deposit_percent
    loan_amount = property_price - deposit
    
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    total_payments = monthly_payment * loan_term * 12
    total_interest = total_payments - loan_amount
    
    return {
        'deposit': deposit,
        'loan_amount': loan_amount,
        'monthly_payment': monthly_payment,
        'total_payments': total_payments,
        'total_interest': total_interest,
        'property_price': property_price
    } 