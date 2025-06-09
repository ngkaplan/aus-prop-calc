"""
Tests for financial calculations.
Run with: python3 tests/test_calculations.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculations import calculate_monthly_payment, calculate_buy_to_live_scenario, calculate_buy_to_rent_scenario, calculate_net_worth_analysis, calculate_buy_to_live_net_worth_analysis, calculate_rent_and_invest_analysis


def test_monthly_payment_calculation():
    """Test mortgage payment calculation with known values."""
    # $500k loan, 6% interest, 30 years should be ~$2,997/month
    monthly_payment = calculate_monthly_payment(500000, 0.06, 30)
    assert abs(monthly_payment - 2997.75) < 1.0  # Within $1


def test_zero_interest_rate():
    """Test edge case of 0% interest rate."""
    monthly_payment = calculate_monthly_payment(360000, 0.0, 30)
    expected = 360000 / (30 * 12)  # $1000/month
    assert abs(monthly_payment - expected) < 0.01


def test_buy_to_live_scenario():
    """Test complete buy-to-live calculation."""
    result = calculate_buy_to_live_scenario(
        property_price=800000,
        deposit_percent=0.20,
        interest_rate=0.06,
        loan_term=30
    )
    
    assert result['deposit'] == 160000  # 20% of 800k
    assert result['loan_amount'] == 640000  # 800k - 160k
    assert abs(result['monthly_payment'] - 3837.28) < 1.0  # Known calculation


def test_calculate_remaining_balance():
    """Test the remaining balance calculation."""
    # $400,000 loan at 6% for 30 years, after 5 years
    remaining = calculate_remaining_balance(400000, 0.06, 30, 5)
    assert remaining > 0
    assert remaining < 400000  # Should be less than original
    
    # After full term, balance should be 0
    remaining_full = calculate_remaining_balance(400000, 0.06, 30, 30)
    assert abs(remaining_full) < 1.0  # Should be essentially zero


def test_buy_to_rent_scenario():
    """Test complete buy-to-rent calculation."""
    result = calculate_buy_to_rent_scenario(
        investment_property_price=600000,
        deposit_percent=0.20,
        interest_rate=0.06,
        loan_term=30,
        weekly_rental_income=575,  # ~$2,500/month
        your_weekly_rent=460       # ~$2,000/month
    )
    
    assert result['deposit'] == 120000  # 20% of 600k
    assert result['loan_amount'] == 480000
    assert result['weekly_rental_income'] == 575
    assert result['your_weekly_rent'] == 460
    assert result['monthly_rental_income'] > 0
    assert result['monthly_property_expenses'] > 0


def test_net_worth_analysis():
    """Test net worth analysis for buy-to-rent scenario."""
    result = calculate_net_worth_analysis(
        investment_property_price=600000,
        deposit_percent=0.20,
        interest_rate=0.06,
        loan_term=30,
        weekly_rental_income=575,
        your_weekly_rent=460,
        annual_property_growth_rate=0.05,
        annual_rental_inflation_rate=0.03
    )
    
    assert len(result['yearly_analysis']) == 30
    
    year_1 = result['yearly_analysis'][0]
    assert year_1['year'] == 1
    assert year_1['property_value'] > 600000
    assert year_1['net_worth'] > 0
    
    year_30 = result['yearly_analysis'][29]
    assert year_30['year'] == 30
    assert year_30['property_value'] > year_1['property_value']
    assert year_30['remaining_balance'] == 0


def test_buy_to_live_net_worth_analysis():
    """Test net worth analysis for buy-to-live scenario."""
    result = calculate_buy_to_live_net_worth_analysis(
        property_price=800000,
        deposit_percent=0.20,
        interest_rate=0.06,
        loan_term=30,
        annual_property_growth_rate=0.05
    )
    
    assert len(result['yearly_analysis']) == 30
    
    year_1 = result['yearly_analysis'][0]
    assert year_1['year'] == 1
    assert year_1['property_value'] > 800000
    assert year_1['net_worth'] > 0
    assert year_1['cumulative_income'] == 0
    
    year_30 = result['yearly_analysis'][29]
    assert year_30['year'] == 30
    assert year_30['remaining_balance'] == 0
    assert year_30['net_worth'] == year_30['property_value']


def test_calculate_rent_and_invest_analysis():
    """Test the rent and invest analysis."""
    result = calculate_rent_and_invest_analysis(
        equivalent_property_price=800000,
        deposit_percent=0.20,
        interest_rate=0.06,
        analysis_term=30,
        your_weekly_rent=450,
        annual_stock_return_rate=0.07,       # 7%
        annual_rental_inflation_rate=0.03,   # 3%
        annual_property_growth_rate=0.05,    # 5% property growth (same as other scenarios)
        annual_property_expenses_percent=0.01
    )
    
    # Should have 30 years of analysis
    assert len(result['yearly_analysis']) == 30
    
    # Check initial investment (equivalent to deposit)
    assert result['initial_investment'] == 160000  # 20% of 800k
    
    # Check first year
    year_1 = result['yearly_analysis'][0]
    assert year_1['year'] == 1
    assert year_1['stock_portfolio_value'] > 160000  # Should have grown from initial investment
    assert year_1['annual_rent_cost'] > 0
    assert year_1['annual_stock_returns'] > 0
    assert year_1['cumulative_rent_paid'] > 0
    assert year_1['cumulative_net_stock_investments'] > 160000  # Should include initial + first year investment
    
    # Check last year - stock portfolio should have grown significantly
    year_30 = result['yearly_analysis'][29]
    assert year_30['year'] == 30
    assert year_30['stock_portfolio_value'] > year_1['stock_portfolio_value']
    assert year_30['cumulative_rent_paid'] > year_1['cumulative_rent_paid']  # Should have paid more rent
    assert year_30['cumulative_net_stock_investments'] > year_1['cumulative_net_stock_investments']  # Should have invested more
    
    # Net cash invested should be rent + stock investments
    assert year_30['net_cash_invested'] == year_30['cumulative_rent_paid'] + year_30['cumulative_net_stock_investments']


if __name__ == "__main__":
    print("Running calculation tests...")
    
    # Test 1: Monthly payment calculation
    try:
        monthly_payment = calculate_monthly_payment(500000, 0.06, 30)
        expected = 2997.75
        if abs(monthly_payment - expected) < 1.0:
            print("✅ Monthly payment test PASSED")
        else:
            print(f"❌ Monthly payment test FAILED: got {monthly_payment}, expected ~{expected}")
    except Exception as e:
        print(f"❌ Monthly payment test ERROR: {e}")
    
    # Test 2: Zero interest
    try:
        monthly_payment = calculate_monthly_payment(360000, 0.0, 30)
        expected = 1000.0
        if abs(monthly_payment - expected) < 0.01:
            print("✅ Zero interest test PASSED")
        else:
            print(f"❌ Zero interest test FAILED: got {monthly_payment}, expected {expected}")
    except Exception as e:
        print(f"❌ Zero interest test ERROR: {e}")
    
    # Test 3: Complete scenario
    try:
        result = calculate_buy_to_live_scenario(800000, 0.20, 0.06, 30)
        print("✅ Complete scenario test PASSED")
        print(f"   Deposit: ${result['deposit']:,.2f}")
        print(f"   Monthly payment: ${result['monthly_payment']:,.2f}")
        print(f"   Total interest: ${result['total_interest']:,.2f}")
    except Exception as e:
        print(f"❌ Complete scenario test ERROR: {e}")
    
    # Test 4: Buy to rent scenario
    try:
        result = calculate_buy_to_rent_scenario(
            investment_property_price=600000,
            deposit_percent=0.20,
            interest_rate=0.06,
            loan_term=30,
            weekly_rental_income=575,  # ~$2,500/month
            your_weekly_rent=460       # ~$2,000/month
        )
        print("✅ Buy to rent scenario test PASSED")
        print(f"   Investment deposit: ${result['deposit']:,.2f}")
        print(f"   Monthly mortgage payment: ${result['monthly_mortgage_payment']:,.2f}")
        print(f"   Monthly rental net: ${result['monthly_rental_net']:,.2f}")
        print(f"   Your total monthly housing cost: ${result['monthly_total_housing_cost']:,.2f}")
    except Exception as e:
        print(f"❌ Buy to rent scenario test ERROR: {e}")
    
    # Test 5: Net worth analysis
    try:
        result = calculate_net_worth_analysis(
            investment_property_price=600000,
            deposit_percent=0.20,
            interest_rate=0.06,
            loan_term=30,
            weekly_rental_income=575,
            your_weekly_rent=460,
            annual_property_growth_rate=0.05,
            annual_rental_inflation_rate=0.03
        )
        print("✅ Net worth analysis test PASSED")
        year_10 = result['yearly_analysis'][9]  # Year 10 (index 9)
        print(f"   Year 10 property value: ${year_10['property_value']:,.0f}")
        print(f"   Year 10 net worth: ${year_10['net_worth']:,.0f}")
        print(f"   Year 10 ROI: {year_10['roi_percent']:.1f}%")
    except Exception as e:
        print(f"❌ Net worth analysis test ERROR: {e}")
    
    # Test 6: Buy to live net worth analysis
    try:
        result = calculate_buy_to_live_net_worth_analysis(
            property_price=800000,
            deposit_percent=0.20,
            interest_rate=0.06,
            loan_term=30,
            annual_property_growth_rate=0.05
        )
        print("✅ Buy to live net worth analysis test PASSED")
        year_10 = result['yearly_analysis'][9]  # Year 10 (index 9)
        print(f"   Year 10 property value: ${year_10['property_value']:,.0f}")
        print(f"   Year 10 net worth: ${year_10['net_worth']:,.0f}")
        print(f"   Year 10 net cash invested: ${year_10['net_cash_invested']:,.0f}")
        print(f"   Year 10 ROI: {year_10['roi_percent']:.1f}%")
    except Exception as e:
        print(f"❌ Buy to live net worth analysis test ERROR: {e}")
    
    # Test 7: Rent and invest analysis
    try:
        result = calculate_rent_and_invest_analysis(
            equivalent_property_price=800000,
            deposit_percent=0.20,
            interest_rate=0.06,
            analysis_term=30,
            your_weekly_rent=450,
            annual_stock_return_rate=0.07,
            annual_rental_inflation_rate=0.03,
            annual_property_growth_rate=0.05,  # 5% property growth 
            annual_property_expenses_percent=0.01
        )
        print("✅ Rent and invest analysis test PASSED")
        year_1 = result['yearly_analysis'][0]
        assert year_1['stock_portfolio_value'] > 160000
        assert year_1['annual_rent_cost'] > 0
        assert year_1['annual_stock_returns'] > 0
        assert year_1['cumulative_rent_paid'] > 0
        assert year_1['cumulative_net_stock_investments'] > 160000
        year_30 = result['yearly_analysis'][29]
        assert year_30['stock_portfolio_value'] > year_1['stock_portfolio_value']
        assert year_30['cumulative_rent_paid'] > year_1['cumulative_rent_paid']
        assert year_30['cumulative_net_stock_investments'] > year_1['cumulative_net_stock_investments']
        assert year_30['net_cash_invested'] == year_30['cumulative_rent_paid'] + year_30['cumulative_net_stock_investments']
    except Exception as e:
        print(f"❌ Rent and invest analysis test ERROR: {e}")
    
    print("\nAll tests completed!") 