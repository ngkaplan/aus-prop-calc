"""
Tests for financial calculations.
Run with: python3 tests/test_calculations.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculations import calculate_monthly_payment, calculate_buy_to_live_scenario


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
    
    print("\nAll tests completed!") 