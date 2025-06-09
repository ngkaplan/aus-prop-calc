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


def calculate_buy_to_rent_scenario(
    investment_property_price: float, 
    deposit_percent: float,
    interest_rate: float, 
    loan_term: int,
    weekly_rental_income: float,
    your_weekly_rent: float,
    annual_property_expenses_percent: float = 0.01  # 1% of property value for maintenance, etc.
) -> dict:
    """
    Calculate the financial outcome for buying an investment property while renting.
    
    Args:
        investment_property_price: Price of the investment property
        deposit_percent: Deposit as decimal (0.2 for 20%)
        interest_rate: Annual interest rate as decimal (0.06 for 6%)
        loan_term: Loan term in years
        weekly_rental_income: Expected weekly rental income (Australian standard)
        your_weekly_rent: Your weekly rent for where you live
        annual_property_expenses_percent: Annual expenses as % of property value
    
    Returns:
        Dictionary with calculation results
    """
    # Convert weekly amounts to monthly (52 weeks / 12 months = 4.33)
    monthly_rental_income = weekly_rental_income * 52 / 12
    your_monthly_rent = your_weekly_rent * 52 / 12
    
    # Investment property calculations
    deposit = investment_property_price * deposit_percent
    loan_amount = investment_property_price - deposit
    monthly_mortgage_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    
    # Annual expenses (maintenance, rates, insurance, etc.)
    annual_property_expenses = investment_property_price * annual_property_expenses_percent
    monthly_property_expenses = annual_property_expenses / 12
    
    # Monthly cash flow calculation
    monthly_rental_net = monthly_rental_income - monthly_mortgage_payment - monthly_property_expenses
    monthly_total_housing_cost = your_monthly_rent - monthly_rental_net  # Net cost after rental income
    
    # Total calculations over loan term
    total_mortgage_payments = monthly_mortgage_payment * loan_term * 12
    total_interest = total_mortgage_payments - loan_amount
    total_rental_income = monthly_rental_income * loan_term * 12
    total_property_expenses = monthly_property_expenses * loan_term * 12
    total_your_rent = your_monthly_rent * loan_term * 12
    
    return {
        'deposit': deposit,
        'loan_amount': loan_amount,
        'investment_property_price': investment_property_price,
        'monthly_mortgage_payment': monthly_mortgage_payment,
        'weekly_rental_income': weekly_rental_income,
        'monthly_rental_income': monthly_rental_income,
        'monthly_property_expenses': monthly_property_expenses,
        'monthly_rental_net': monthly_rental_net,
        'your_weekly_rent': your_weekly_rent,
        'your_monthly_rent': your_monthly_rent,
        'monthly_total_housing_cost': monthly_total_housing_cost,
        'total_interest': total_interest,
        'total_rental_income': total_rental_income,
        'total_property_expenses': total_property_expenses,
        'total_your_rent': total_your_rent
    } 