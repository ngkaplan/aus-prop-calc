"""
Financial calculations for Australian property investment scenarios.
Start simple - just mortgage calculations first.
"""

def calculate_stamp_duty(property_value: float, is_first_home_buyer: bool = False) -> float:
    """
    Calculate Australian stamp duty based on property value and first home buyer status.
    
    Args:
        property_value: Property purchase price
        is_first_home_buyer: Whether buyer qualifies for first home buyer concessions
    
    Returns:
        Stamp duty amount
    """
    if is_first_home_buyer:
        # First Home Buyer concessional rates
        if property_value <= 800000:
            return 0  # No stamp duty for properties under $800k
        elif property_value >= 1000000:
            # Standard rate for properties $1M and over (fall through to standard calculation)
            pass
        else:
            # Between $800k and $1M: (property value - 800k) / 200k * Standard Stamp Duty Rate
            standard_rate = calculate_stamp_duty(property_value, False)  # Get standard rate
            concession_factor = (property_value - 800000) / 200000
            return standard_rate * concession_factor
    
    # Standard stamp duty rates (NSW-style brackets)
    if property_value <= 17000:
        return max(20, property_value * 0.0125)  # Minimum $20
    elif property_value <= 36000:
        return 212 + ((property_value - 17000) * 0.015)
    elif property_value <= 97000:
        return 497 + ((property_value - 36000) * 0.0175)
    elif property_value <= 364000:
        return 1564 + ((property_value - 97000) * 0.035)
    elif property_value <= 1212000:
        return 10909 + ((property_value - 364000) * 0.045)
    elif property_value <= 3636000:
        return 49069 + ((property_value - 1212000) * 0.055)
    else:
        return 182390 + ((property_value - 3636000) * 0.07)


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


def calculate_annual_mortgage_interest(principal: float, annual_rate: float, years: int, year: int) -> float:
    """
    Calculate the interest portion of mortgage payments for a specific year.
    
    Args:
        principal: Original loan amount
        annual_rate: Annual interest rate as decimal
        years: Total loan term in years
        year: Year to calculate interest for (1-based)
    
    Returns:
        Annual interest paid in that year
    """
    if year > years or annual_rate == 0:
        return 0
    
    monthly_rate = annual_rate / 12
    monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
    
    # Calculate interest for each month of the year
    annual_interest = 0
    
    for month in range((year - 1) * 12, year * 12):
        if month >= years * 12:
            break
            
        # Calculate remaining balance at start of this month
        remaining_balance = principal
        for i in range(month):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            if remaining_balance <= 0:
                break
        
        if remaining_balance > 0:
            monthly_interest = remaining_balance * monthly_rate
            annual_interest += monthly_interest
    
    return annual_interest


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
    annual_property_expenses_percent: float = 0.01,
    upfront_costs: float = 3000,
    annual_gross_income: float = 100000,
    salary_growth_rate: float = 0.03
) -> dict:
    """
    Calculate year-by-year net worth and ROI analysis for buy-to-rent scenario.
    Includes Australian negative gearing tax benefits.
    
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
        upfront_costs: Legal fees, inspections, etc.
        annual_gross_income: Starting annual gross income for tax calculations
        salary_growth_rate: Annual salary growth rate
    
    Returns:
        Dictionary with year-by-year analysis including negative gearing benefits
    """
    # Initial calculations
    deposit = investment_property_price * deposit_percent
    stamp_duty = calculate_stamp_duty(investment_property_price, False)  # Investment property, no FHB
    total_upfront_costs = deposit + stamp_duty + upfront_costs
    loan_amount = investment_property_price - deposit
    monthly_mortgage_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    
    # Convert weekly to monthly
    initial_monthly_rental = weekly_rental_income * 52 / 12
    your_monthly_rent = your_weekly_rent * 52 / 12
    
    # Year-by-year tracking
    yearly_analysis = []
    cumulative_costs = total_upfront_costs  # Start with deposit + stamp duty + upfront costs
    cumulative_income = 0  # Track rental income received
    cumulative_negative_gearing_benefits = 0  # Track negative gearing tax savings
    
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
        
        # Calculate mortgage interest (deductible) vs principal (not deductible)
        annual_mortgage_interest = calculate_annual_mortgage_interest(loan_amount, interest_rate, loan_term, year)
        
        # Negative gearing calculation
        current_income = annual_gross_income * (1 + salary_growth_rate) ** year
        marginal_tax_rate = calculate_marginal_tax_rate(current_income)
        
        # Deductible expenses: mortgage interest + property expenses
        annual_deductible_expenses = annual_mortgage_interest + annual_property_expenses
        
        # Property loss for tax purposes (if expenses > rental income)
        property_loss = max(0, annual_deductible_expenses - annual_rental_income)
        
        # Tax savings from negative gearing
        annual_negative_gearing_benefit = property_loss * marginal_tax_rate
        cumulative_negative_gearing_benefits += annual_negative_gearing_benefit
        
        # Cumulative costs (add all expenses including your rent)
        cumulative_costs += annual_property_expenses
        cumulative_costs += annual_mortgage_payments  
        cumulative_costs += annual_your_rent
        
        # Cumulative income (rental income + negative gearing tax benefits)
        cumulative_income += annual_rental_income + annual_negative_gearing_benefit
        
        # Net cash invested = Total Costs - Total Income
        net_cash_invested = cumulative_costs - cumulative_income
        
        # Monthly cash flow for display
        monthly_net_cash_flow = rental_income - monthly_mortgage_payment - monthly_property_expenses
        annual_net_cash_flow = monthly_net_cash_flow * 12
        
        # Remaining loan balance
        remaining_balance = calculate_remaining_balance(loan_amount, interest_rate, loan_term, year)
        
        # Net worth = Property Value - Remaining Loan Balance + Cumulative Negative Gearing Benefits
        net_worth = property_value - remaining_balance + cumulative_negative_gearing_benefits
        
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
            'annual_rental_income': annual_rental_income,
            'annual_mortgage_payments': annual_mortgage_payments,
            'annual_mortgage_interest': annual_mortgage_interest,
            'annual_property_expenses': annual_property_expenses,
            'annual_your_rent': annual_your_rent,
            'annual_deductible_expenses': annual_deductible_expenses,
            'property_loss': property_loss,
            'annual_negative_gearing_benefit': annual_negative_gearing_benefit,
            'cumulative_negative_gearing_benefits': cumulative_negative_gearing_benefits,
            'marginal_tax_rate': marginal_tax_rate,
            'roi_percent': roi_percent,
            'rental_income_monthly': rental_income
        })
    
    return {
        'yearly_analysis': yearly_analysis,
        'initial_deposit': deposit,
        'stamp_duty': stamp_duty,
        'upfront_costs': upfront_costs,
        'total_upfront_costs': total_upfront_costs,
        'loan_amount': loan_amount,
        'monthly_mortgage_payment': monthly_mortgage_payment
    }


def calculate_buy_to_live_net_worth_analysis(
    property_price: float,
    deposit_percent: float,
    interest_rate: float,
    loan_term: int,
    annual_property_growth_rate: float,
    annual_property_expenses_percent: float = 0.01,
    upfront_costs: float = 3000,
    is_first_home_buyer: bool = False
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
        upfront_costs: Legal fees, inspections, etc.
        is_first_home_buyer: Whether eligible for first home buyer stamp duty concessions
    
    Returns:
        Dictionary with year-by-year analysis
    """
    # Initial calculations
    deposit = property_price * deposit_percent
    stamp_duty = calculate_stamp_duty(property_price, is_first_home_buyer)
    total_upfront_costs = deposit + stamp_duty + upfront_costs
    loan_amount = property_price - deposit
    monthly_mortgage_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    
    # Year-by-year tracking
    yearly_analysis = []
    cumulative_costs = total_upfront_costs  # Start with deposit + stamp duty + upfront costs
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
        'stamp_duty': stamp_duty,
        'upfront_costs': upfront_costs,
        'total_upfront_costs': total_upfront_costs,
        'loan_amount': loan_amount,
        'monthly_mortgage_payment': monthly_mortgage_payment
    }


def calculate_rent_and_invest_analysis(
    equivalent_property_price: float,
    deposit_percent: float,
    interest_rate: float,
    analysis_term: int,
    your_weekly_rent: float,
    annual_stock_return_rate: float,
    annual_rental_inflation_rate: float,
    annual_property_growth_rate: float,
    annual_property_expenses_percent: float = 0.01,
    upfront_costs: float = 3000,
    is_first_home_buyer: bool = False
) -> dict:
    """
    Calculate year-by-year net worth and ROI analysis for rent-and-invest scenario.
    
    CORRECTED APPROACH: Only invest the NET amount after paying rent.
    This creates a fair comparison where total cash outlay equals property scenarios.
    
    Logic: If property costs $X per year, and you pay $Y rent, 
    then you only have $(X-Y) available to invest in stocks.
    
    UPDATED: Property expenses now grow each year based on growing property value,
    exactly matching the Buy to Live scenario for perfect comparison.
    
    INCLUDES: Stamp duty and upfront costs that would have been spent on property
    are instead invested in the stock market from day one.
    """
    # Calculate what would have been spent on property (including all upfront costs)
    deposit_equivalent = equivalent_property_price * deposit_percent
    stamp_duty_equivalent = calculate_stamp_duty(equivalent_property_price, is_first_home_buyer)
    total_upfront_equivalent = deposit_equivalent + stamp_duty_equivalent + upfront_costs
    loan_amount_equivalent = equivalent_property_price - deposit_equivalent
    monthly_mortgage_equivalent = calculate_monthly_payment(loan_amount_equivalent, interest_rate, analysis_term)
    
    # Convert weekly rent to monthly
    your_monthly_rent = your_weekly_rent * 52 / 12
    
    # Year-by-year tracking
    yearly_analysis = []
    cumulative_rent_paid = 0  # Track total rent payments
    cumulative_net_stock_investments = total_upfront_equivalent  # Start with total upfront costs invested
    stock_portfolio_value = total_upfront_equivalent  # Start with all upfront costs invested in stocks
    
    for year in range(1, analysis_term + 1):
        # Your annual rent (with inflation)
        annual_your_rent = your_monthly_rent * (1 + annual_rental_inflation_rate) ** year * 12
        
        # What property costs would have been this year - GROWING property expenses
        # This now matches exactly with Buy to Live scenario
        current_property_value = equivalent_property_price * (1 + annual_property_growth_rate) ** year
        annual_property_expenses_equivalent = (current_property_value * annual_property_expenses_percent)
        annual_mortgage_equivalent = monthly_mortgage_equivalent * 12
        annual_property_costs_total = annual_mortgage_equivalent + annual_property_expenses_equivalent
        
        # NET amount available to invest (property costs minus rent paid)
        annual_net_investment = annual_property_costs_total - annual_your_rent
        
        # Only invest if there's a positive net amount
        if annual_net_investment > 0:
            stock_portfolio_value += annual_net_investment
            cumulative_net_stock_investments += annual_net_investment
        # If rent > property costs, no additional investment (but don't reduce portfolio)
        
        # Apply stock market returns to entire portfolio
        stock_returns_this_year = stock_portfolio_value * annual_stock_return_rate
        stock_portfolio_value += stock_returns_this_year
        
        # Track cumulative rent paid
        cumulative_rent_paid += annual_your_rent
        
        # Net cash invested = Stock investments + Rent paid
        # This should now equal property scenario total costs
        net_cash_invested = cumulative_net_stock_investments + cumulative_rent_paid
        
        # Net worth = Stock portfolio value
        net_worth = stock_portfolio_value
        
        # Return on investment
        roi_percent = ((net_worth - net_cash_invested) / net_cash_invested) * 100 if net_cash_invested > 0 else 0
        
        yearly_analysis.append({
            'year': year,
            'stock_portfolio_value': stock_portfolio_value,
            'net_worth': net_worth,
            'cumulative_rent_paid': cumulative_rent_paid,
            'cumulative_net_stock_investments': cumulative_net_stock_investments,
            'net_cash_invested': net_cash_invested,
            'annual_rent_cost': annual_your_rent,
            'annual_stock_returns': stock_returns_this_year,
            'annual_net_investment': annual_net_investment,
            'annual_property_costs_total': annual_property_costs_total,
            'roi_percent': roi_percent
        })
    
    return {
        'yearly_analysis': yearly_analysis,
        'initial_investment': total_upfront_equivalent,
        'deposit_equivalent': deposit_equivalent,
        'stamp_duty_equivalent': stamp_duty_equivalent,
        'upfront_costs_equivalent': upfront_costs,
        'monthly_net_investment_equivalent': max(0, (annual_property_costs_total - annual_your_rent) / 12)
    }


def calculate_australian_income_tax(taxable_income: float, year: int = 2024) -> float:
    """
    Calculate Australian income tax based on current tax brackets.
    
    Args:
        taxable_income: Annual taxable income in AUD
        year: Tax year (for future tax bracket updates)
    
    Returns:
        Annual income tax amount
    """
    # 2023-24 Australian tax brackets (including Medicare levy)
    if taxable_income <= 18200:
        tax = 0
    elif taxable_income <= 45000:
        tax = (taxable_income - 18200) * 0.19
    elif taxable_income <= 120000:
        tax = 5092 + (taxable_income - 45000) * 0.325
    elif taxable_income <= 180000:
        tax = 29467 + (taxable_income - 120000) * 0.37
    else:
        tax = 51667 + (taxable_income - 180000) * 0.45
    
    # Add Medicare levy (2% for incomes over $24,276)
    medicare_threshold = 24276
    if taxable_income > medicare_threshold:
        medicare_levy = taxable_income * 0.02
        tax += medicare_levy
    
    return max(0, tax)


def calculate_marginal_tax_rate(taxable_income: float, year: int = 2024) -> float:
    """
    Calculate the marginal tax rate (including Medicare levy) for a given income.
    
    Args:
        taxable_income: Annual taxable income in AUD
        year: Tax year
    
    Returns:
        Marginal tax rate as decimal (e.g., 0.325 for 32.5%)
    """
    # Medicare levy applies to all brackets above threshold
    medicare_rate = 0.02 if taxable_income > 24276 else 0
    
    if taxable_income <= 18200:
        return 0 + medicare_rate
    elif taxable_income <= 45000:
        return 0.19 + medicare_rate
    elif taxable_income <= 120000:
        return 0.325 + medicare_rate
    elif taxable_income <= 180000:
        return 0.37 + medicare_rate
    else:
        return 0.45 + medicare_rate


def calculate_capital_gains_tax(
    capital_gain: float, 
    marginal_tax_rate: float, 
    held_over_12_months: bool = True
) -> float:
    """
    Calculate Australian capital gains tax.
    
    Args:
        capital_gain: Amount of capital gain
        marginal_tax_rate: Investor's marginal tax rate (as decimal)
        held_over_12_months: Whether asset was held for more than 12 months
    
    Returns:
        Capital gains tax amount
    """
    if capital_gain <= 0:
        return 0
    
    # 50% CGT discount for assets held over 12 months
    if held_over_12_months:
        taxable_gain = capital_gain * 0.5
    else:
        taxable_gain = capital_gain
    
    return taxable_gain * marginal_tax_rate


def apply_capital_gains_tax_to_scenarios(
    btl_analysis: dict,
    btr_analysis: dict, 
    ri_analysis: dict,
    annual_gross_income: float,
    salary_growth_rate: float
) -> tuple:
    """
    Apply capital gains tax to buy-to-rent and rent-and-invest scenarios.
    Buy-to-live is exempt due to main residence exemption.
    
    Args:
        btl_analysis: Buy to live analysis results
        btr_analysis: Buy to rent analysis results  
        ri_analysis: Rent and invest analysis results
        annual_gross_income: Starting annual gross income
        salary_growth_rate: Annual salary growth rate
    
    Returns:
        Tuple of (btl_analysis, btr_analysis_after_tax, ri_analysis_after_tax)
    """
    # Buy to live - no changes (main residence exemption)
    btl_analysis_final = btl_analysis.copy()
    
    # Buy to rent - apply CGT on property sale
    btr_analysis_after_tax = btr_analysis.copy()
    btr_yearly = btr_analysis_after_tax['yearly_analysis'].copy()
    
    for i, year_data in enumerate(btr_yearly):
        year = year_data['year']
        
        # Calculate income and marginal tax rate for this year
        current_income = annual_gross_income * (1 + salary_growth_rate) ** year
        marginal_rate = calculate_marginal_tax_rate(current_income)
        
        # Calculate property capital gain
        property_value = year_data['property_value']
        # Get the original property price (deposit / deposit_percent)
        deposit_percent = btr_analysis['initial_deposit'] / (btr_analysis['initial_deposit'] + btr_analysis['loan_amount'])
        initial_property_price = btr_analysis['initial_deposit'] / deposit_percent
        capital_gain = property_value - initial_property_price
        
        # Calculate CGT (held > 12 months, so 50% discount applies)
        cgt_liability = calculate_capital_gains_tax(capital_gain, marginal_rate, True)
        
        # Adjust net worth for CGT liability if sold
        net_worth_after_tax = year_data['net_worth'] - cgt_liability
        
        # Update the year data
        btr_yearly[i] = year_data.copy()
        btr_yearly[i]['net_worth_after_tax'] = net_worth_after_tax
        btr_yearly[i]['cgt_liability'] = cgt_liability
        btr_yearly[i]['capital_gain'] = capital_gain
        btr_yearly[i]['marginal_tax_rate'] = marginal_rate
    
    btr_analysis_after_tax['yearly_analysis'] = btr_yearly
    
    # Rent and invest - apply CGT on stock portfolio sale
    ri_analysis_after_tax = ri_analysis.copy()
    ri_yearly = ri_analysis_after_tax['yearly_analysis'].copy()
    
    for i, year_data in enumerate(ri_yearly):
        year = year_data['year']
        
        # Calculate income and marginal tax rate for this year
        current_income = annual_gross_income * (1 + salary_growth_rate) ** year
        marginal_rate = calculate_marginal_tax_rate(current_income)
        
        # Calculate stock portfolio capital gain
        portfolio_value = year_data['stock_portfolio_value']
        total_invested = year_data['cumulative_net_stock_investments']
        capital_gain = portfolio_value - total_invested
        
        # Calculate CGT (held > 12 months, so 50% discount applies)
        cgt_liability = calculate_capital_gains_tax(capital_gain, marginal_rate, True)
        
        # Adjust net worth for CGT liability if sold
        net_worth_after_tax = portfolio_value - cgt_liability
        
        # Update the year data
        ri_yearly[i] = year_data.copy()
        ri_yearly[i]['net_worth_after_tax'] = net_worth_after_tax
        ri_yearly[i]['cgt_liability'] = cgt_liability
        ri_yearly[i]['capital_gain'] = capital_gain
        ri_yearly[i]['marginal_tax_rate'] = marginal_rate
    
    ri_analysis_after_tax['yearly_analysis'] = ri_yearly
    
    return btl_analysis_final, btr_analysis_after_tax, ri_analysis_after_tax 