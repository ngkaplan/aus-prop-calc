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


def calculate_remaining_balance(principal: float, annual_rate: float, years: int, years_paid: int) -> float:
    """Calculate remaining loan balance after a certain number of years."""
    if years_paid >= years:
        return 0.0
    
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payments_made = years_paid * 12
    
    if annual_rate == 0:
        return principal - (principal / num_payments * payments_made)
    
    monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
    
    # Remaining balance formula
    remaining_balance = principal * (
        (1 + monthly_rate) ** num_payments - (1 + monthly_rate) ** payments_made
    ) / ((1 + monthly_rate) ** num_payments - 1)
    
    return max(0, remaining_balance)


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


def calculate_net_worth_analysis(
    investment_property_price: float,
    deposit_percent: float,
    interest_rate: float,
    loan_term: int,
    weekly_rental_income: float,
    your_weekly_rent: float,
    annual_property_growth_rate: float,
    annual_rental_inflation_rate: float,
    annual_property_expenses_percent: float = 0.01
) -> dict:
    """
    Calculate year-by-year net worth and ROI analysis for buy-to-rent scenario.
    
    Args:
        investment_property_price: Price of the investment property
        deposit_percent: Deposit as decimal (0.2 for 20%)
        interest_rate: Annual interest rate as decimal (0.06 for 6%)
        loan_term: Loan term in years
        weekly_rental_income: Expected weekly rental income
        your_weekly_rent: Your weekly rent
        annual_property_growth_rate: Expected annual property value growth (e.g., 0.05 for 5%)
        annual_rental_inflation_rate: Expected annual rental inflation (e.g., 0.03 for 3%)
        annual_property_expenses_percent: Annual expenses as % of property value
    
    Returns:
        Dictionary with year-by-year analysis
    """
    # Initial calculations
    deposit = investment_property_price * deposit_percent
    loan_amount = investment_property_price - deposit
    monthly_mortgage_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    
    # Convert weekly to monthly
    initial_monthly_rental = weekly_rental_income * 52 / 12
    your_monthly_rent = your_weekly_rent * 52 / 12
    
    # Year-by-year tracking
    yearly_analysis = []
    cumulative_costs = deposit  # Start with deposit
    cumulative_income = 0  # Track rental income received
    
    for year in range(1, loan_term + 1):
        # Property value with growth
        property_value = investment_property_price * (1 + annual_property_growth_rate) ** year
        
        # Rental income with inflation
        rental_income = initial_monthly_rental * (1 + annual_rental_inflation_rate) ** year
        
        # Property expenses (as % of current property value)
        monthly_property_expenses = (property_value * annual_property_expenses_percent) / 12
        
        # Annual calculations
        annual_property_expenses = monthly_property_expenses * 12
        annual_mortgage_payments = monthly_mortgage_payment * 12
        annual_rental_income = rental_income * 12
        annual_your_rent = your_monthly_rent * (1 + annual_rental_inflation_rate) ** year * 12
        
        # Cumulative costs (add all expenses including your rent)
        cumulative_costs += annual_property_expenses
        cumulative_costs += annual_mortgage_payments  
        cumulative_costs += annual_your_rent
        
        # Cumulative income (rental income received)
        cumulative_income += annual_rental_income
        
        # Net cash invested = Total Costs - Total Income
        net_cash_invested = cumulative_costs - cumulative_income
        
        # Monthly cash flow for display
        monthly_net_cash_flow = rental_income - monthly_mortgage_payment - monthly_property_expenses
        annual_net_cash_flow = monthly_net_cash_flow * 12
        
        # Remaining loan balance
        remaining_balance = calculate_remaining_balance(loan_amount, interest_rate, loan_term, year)
        
        # Net worth = Property Value - Remaining Loan Balance
        net_worth = property_value - remaining_balance
        
        # Return on investment
        roi_percent = ((net_worth - net_cash_invested) / net_cash_invested) * 100 if net_cash_invested > 0 else 0
        
        yearly_analysis.append({
            'year': year,
            'property_value': property_value,
            'remaining_balance': remaining_balance,
            'net_worth': net_worth,
            'cumulative_costs': cumulative_costs,
            'cumulative_income': cumulative_income,
            'net_cash_invested': net_cash_invested,
            'annual_net_cash_flow': annual_net_cash_flow,
            'annual_total_housing_cost': annual_property_expenses + annual_mortgage_payments + annual_your_rent,
            'roi_percent': roi_percent,
            'rental_income_monthly': rental_income
        })
    
    return {
        'yearly_analysis': yearly_analysis,
        'initial_deposit': deposit,
        'loan_amount': loan_amount,
        'monthly_mortgage_payment': monthly_mortgage_payment
    }


def calculate_buy_to_live_net_worth_analysis(
    property_price: float,
    deposit_percent: float,
    interest_rate: float,
    loan_term: int,
    annual_property_growth_rate: float,
    annual_property_expenses_percent: float = 0.01
) -> dict:
    """
    Calculate year-by-year net worth and ROI analysis for buy-to-live scenario.
    
    Args:
        property_price: Total property price
        deposit_percent: Deposit as decimal (0.2 for 20%)
        interest_rate: Annual interest rate as decimal (0.06 for 6%)
        loan_term: Loan term in years
        annual_property_growth_rate: Expected annual property value growth
        annual_property_expenses_percent: Annual expenses as % of property value
    
    Returns:
        Dictionary with year-by-year analysis
    """
    # Initial calculations
    deposit = property_price * deposit_percent
    loan_amount = property_price - deposit
    monthly_mortgage_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    
    # Year-by-year tracking
    yearly_analysis = []
    cumulative_costs = deposit  # Start with deposit
    cumulative_income = 0  # No income for buy-to-live
    
    for year in range(1, loan_term + 1):
        # Property value with growth
        property_value = property_price * (1 + annual_property_growth_rate) ** year
        
        # Property expenses (as % of current property value)
        monthly_property_expenses = (property_value * annual_property_expenses_percent) / 12
        
        # Annual calculations
        annual_mortgage_payments = monthly_mortgage_payment * 12
        annual_property_expenses = monthly_property_expenses * 12
        
        # Cumulative costs (always add expenses and mortgage payments)
        cumulative_costs += annual_mortgage_payments
        cumulative_costs += annual_property_expenses
        
        # Net cash invested = Costs - Income (for buy-to-live, income is 0)
        net_cash_invested = cumulative_costs - cumulative_income
        
        # Remaining loan balance
        remaining_balance = calculate_remaining_balance(loan_amount, interest_rate, loan_term, year)
        
        # Net worth = Property Value - Remaining Loan Balance
        net_worth = property_value - remaining_balance
        
        # Return on investment
        roi_percent = ((net_worth - net_cash_invested) / net_cash_invested) * 100 if net_cash_invested > 0 else 0
        
        # Annual housing cost (mortgage + expenses)
        annual_housing_cost = annual_mortgage_payments + annual_property_expenses
        
        yearly_analysis.append({
            'year': year,
            'property_value': property_value,
            'remaining_balance': remaining_balance,
            'net_worth': net_worth,
            'cumulative_costs': cumulative_costs,
            'cumulative_income': cumulative_income,
            'net_cash_invested': net_cash_invested,
            'annual_housing_cost': annual_housing_cost,
            'roi_percent': roi_percent
        })
    
    return {
        'yearly_analysis': yearly_analysis,
        'initial_deposit': deposit,
        'loan_amount': loan_amount,
        'monthly_mortgage_payment': monthly_mortgage_payment
    } 