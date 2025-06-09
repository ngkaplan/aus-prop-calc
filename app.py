import streamlit as st
import pandas as pd
from calculations import calculate_buy_to_live_scenario, calculate_buy_to_rent_scenario

def main():
    st.title("🏠 Australian Property Investment Calculator")
    st.write("Compare: Buy to Live vs Buy to Rent vs Rent & Invest")
    
    # Sidebar for scenario selection
    st.sidebar.header("Choose Scenario")
    scenario = st.sidebar.selectbox(
        "Select investment scenario:",
        ["Buy to Live", "Buy to Rent"]
    )
    
    if scenario == "Buy to Live":
        st.header("🏡 Buy to Live Scenario")
        st.write("Purchase a property and live in it")
        
        # Basic property inputs
        property_price = st.number_input("Property Price ($)", value=800000, step=10000)
        deposit_percent = st.slider("Deposit (%)", min_value=5, max_value=50, value=20)
        interest_rate = st.slider("Interest Rate (%)", min_value=2.0, max_value=8.0, value=6.0, step=0.1)
        loan_term = st.selectbox("Loan Term (years)", [25, 30], index=1)
        
        if st.button("Calculate Buy to Live"):
            try:
                results = calculate_buy_to_live_scenario(
                    property_price=property_price,
                    deposit_percent=deposit_percent/100,
                    interest_rate=interest_rate/100,
                    loan_term=loan_term
                )
                
                st.success("Calculation Complete!")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Deposit Required", f"${results['deposit']:,.0f}")
                    st.metric("Monthly Payment", f"${results['monthly_payment']:,.0f}")
                
                with col2:
                    st.metric("Total Interest", f"${results['total_interest']:,.0f}")
                    st.metric("Total Payments", f"${results['total_payments']:,.0f}")
                
            except Exception as e:
                st.error(f"Calculation error: {e}")
    
    elif scenario == "Buy to Rent":
        st.header("🏢 Buy to Rent Scenario")
        st.write("Buy an investment property while renting your residence")
        
        # Investment property inputs
        st.subheader("Investment Property")
        investment_price = st.number_input("Investment Property Price ($)", value=600000, step=10000)
        deposit_percent = st.slider("Deposit (%)", min_value=5, max_value=50, value=20)
        interest_rate = st.slider("Interest Rate (%)", min_value=2.0, max_value=8.0, value=6.0, step=0.1)
        loan_term = st.selectbox("Loan Term (years)", [25, 30], index=1)
        
        # Rental inputs
        st.subheader("Rental Income & Your Housing")
        weekly_rental_income = st.number_input("Expected Weekly Rental Income ($)", value=575, step=25)
        your_weekly_rent = st.number_input("Your Weekly Rent ($)", value=460, step=25)
        
        if st.button("Calculate Buy to Rent"):
            try:
                results = calculate_buy_to_rent_scenario(
                    investment_property_price=investment_price,
                    deposit_percent=deposit_percent/100,
                    interest_rate=interest_rate/100,
                    loan_term=loan_term,
                    weekly_rental_income=weekly_rental_income,
                    your_weekly_rent=your_weekly_rent
                )
                
                st.success("Calculation Complete!")
                
                # Display key metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Investment Deposit", f"${results['deposit']:,.0f}")
                    st.metric("Monthly Mortgage", f"${results['monthly_mortgage_payment']:,.0f}")
                
                with col2:
                    st.metric("Weekly Rental Income", f"${results['weekly_rental_income']:,.0f}")
                    st.metric("Monthly Property Expenses", f"${results['monthly_property_expenses']:,.0f}")
                
                with col3:
                    st.metric("Your Weekly Rent", f"${results['your_weekly_rent']:,.0f}")
                    net_cash_flow = results['monthly_rental_net']
                    st.metric("Monthly Rental Net", f"${net_cash_flow:,.0f}", 
                             delta="Positive = Income" if net_cash_flow > 0 else "Negative = Cost")
                
                # Summary
                st.subheader("Summary")
                total_housing_cost = results['monthly_total_housing_cost']
                st.write(f"**Total Monthly Housing Cost:** ${total_housing_cost:,.0f}")
                
                if net_cash_flow > 0:
                    st.success(f"✅ Positive cash flow! Investment generates ${net_cash_flow:,.0f}/month")
                else:
                    st.warning(f"⚠️ Negative cash flow. You'll pay ${abs(net_cash_flow):,.0f}/month extra")
                
            except Exception as e:
                st.error(f"Calculation error: {e}")

if __name__ == "__main__":
    main() 