import streamlit as st
import pandas as pd
from calculations import calculate_buy_to_live_scenario

def main():
    st.title("🏠 Australian Property Investment Calculator")
    st.write("Compare: Buy to Live vs Buy to Rent vs Rent & Invest")
    
    # Start with just the basic inputs for one scenario
    st.header("Property Details")
    property_price = st.number_input("Property Price ($)", value=800000, step=10000)
    deposit_percent = st.slider("Deposit (%)", min_value=5, max_value=50, value=20)
    interest_rate = st.slider("Interest Rate (%)", min_value=2.0, max_value=8.0, value=6.0, step=0.1)
    loan_term = st.selectbox("Loan Term (years)", [25, 30], index=1)
    
    if st.button("Calculate Buy to Live Scenario"):
        try:
            results = calculate_buy_to_live_scenario(
                property_price=property_price,
                deposit_percent=deposit_percent/100,
                interest_rate=interest_rate/100,
                loan_term=loan_term
            )
            
            st.success("Calculation Complete!")
            st.write(f"**Monthly Payment:** ${results['monthly_payment']:,.2f}")
            st.write(f"**Total Interest:** ${results['total_interest']:,.2f}")
            st.write(f"**Deposit Required:** ${results['deposit']:,.2f}")
            
        except Exception as e:
            st.error(f"Calculation error: {e}")

if __name__ == "__main__":
    main() 