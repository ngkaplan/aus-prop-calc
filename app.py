import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from calculations import (
    calculate_buy_to_live_scenario, 
    calculate_buy_to_rent_scenario,
    calculate_net_worth_analysis,
    calculate_buy_to_live_net_worth_analysis,
    calculate_rent_and_invest_analysis,
    calculate_stamp_duty
)

def format_currency(amount):
    """Format currency for Australian dollars"""
    return f"${amount:,.0f}"

def format_hover_currency(amount):
    """Format currency for hover display (to nearest 1k)"""
    if amount >= 1000000:
        return f"${amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"${amount/1000:.0f}k"
    else:
        return f"${amount:.0f}"

def format_hover_percent(percent):
    """Format percentage for hover display (to nearest whole %)"""
    return f"{percent:.0f}%"

st.set_page_config(
    page_title="Australian Property Investment Calculator",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Australian Property Investment Comparison")
st.markdown("**Compare all three investment strategies side-by-side with comprehensive analysis**")

# Input sections for all scenarios
st.header("🔧 Investment Parameters")

# Shared assumptions
st.subheader("📊 General Assumptions")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Financial Parameters**")
    deposit_percent = st.slider("Deposit (%)", min_value=5, max_value=50, value=10) / 100
    interest_rate = st.slider("Interest Rate (%)", min_value=1.0, max_value=10.0, value=6.0, step=0.1) / 100
    loan_term = st.slider("Loan Term (years)", min_value=15, max_value=30, value=30)

with col2:
    st.markdown("**Growth & Inflation**")
    property_growth_rate = st.slider("Annual Property Growth (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1) / 100
    rental_inflation_rate = st.slider("Annual Rental Inflation (%)", min_value=0.0, max_value=8.0, value=2.5, step=0.1) / 100
    property_expenses_percent = st.slider("Annual Property Expenses (% of value)", min_value=0.5, max_value=3.0, value=1.0, step=0.1) / 100

with col3:
    st.markdown("**Housing & Investment**")
    your_weekly_rent = st.number_input("Your Weekly Rent ($)", value=450, step=25, help="Your rent cost (used in Buy to Rent and Rent & Invest scenarios)")
    stock_return_rate = st.slider("Annual Stock Market Return (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.1, help="Expected return for Rent & Invest scenario") / 100
    upfront_costs = st.number_input("Upfront Costs ($)", value=3000, step=500, help="Legal fees, inspections, conveyancing")

# Scenario-specific inputs
st.subheader("🏠 Scenario-Specific Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🏡 Buy to Live**")
    btl_property_price = st.number_input("Home Property Price ($)", value=800000, step=10000, help="Price of the home you would buy to live in")
    is_first_home_buyer = st.checkbox("First Home Buyer", value=False, help="Check if eligible for first home buyer stamp duty concessions")
    
    # Show stamp duty preview
    if btl_property_price > 0:
        standard_stamp_duty = calculate_stamp_duty(btl_property_price, False)
        fhb_stamp_duty = calculate_stamp_duty(btl_property_price, True)
        
        if is_first_home_buyer:
            savings = standard_stamp_duty - fhb_stamp_duty
            if savings > 0:
                st.success(f"🎉 FHB Saving: {format_currency(savings)} (Stamp Duty: {format_currency(fhb_stamp_duty)})")
            else:
                st.info(f"ℹ️ Stamp Duty: {format_currency(fhb_stamp_duty)}")
        else:
            st.info(f"ℹ️ Stamp Duty: {format_currency(standard_stamp_duty)}")

with col2:
    st.markdown("**🏠 Buy to Rent**")
    btr_property_price = st.number_input("Investment Property Price ($)", value=600000, step=10000, help="Price of investment property")
    btr_weekly_rental = st.number_input("Weekly Rental Income ($)", value=500, step=25, help="Expected weekly rent from investment property")
    
    # Show stamp duty for investment property
    if btr_property_price > 0:
        investment_stamp_duty = calculate_stamp_duty(btr_property_price, False)
        st.info(f"ℹ️ Investment Property Stamp Duty: {format_currency(investment_stamp_duty)}")

with col3:
    st.markdown("**📈 Rent & Invest**")
    ri_equivalent_property_price = st.number_input("Equivalent Property Price ($)", value=800000, step=10000, help="Price of equivalent property for comparison (typically same as Buy to Live)")

# Calculate all scenarios using shared and specific parameters
st.header("📊 Scenario Calculations")

# Buy to Live
btl_analysis = calculate_buy_to_live_net_worth_analysis(
    btl_property_price, deposit_percent, interest_rate, loan_term, 
    property_growth_rate, property_expenses_percent, upfront_costs, is_first_home_buyer
)

# Buy to Rent
btr_analysis = calculate_net_worth_analysis(
    btr_property_price, deposit_percent, interest_rate, loan_term,
    btr_weekly_rental, your_weekly_rent, property_growth_rate, 
    rental_inflation_rate, property_expenses_percent, upfront_costs
)

# Rent & Invest
ri_analysis = calculate_rent_and_invest_analysis(
    ri_equivalent_property_price, deposit_percent, interest_rate, loan_term,
    your_weekly_rent, stock_return_rate, rental_inflation_rate, property_growth_rate,
    property_expenses_percent, upfront_costs, is_first_home_buyer
)

# Summary metrics
st.subheader("📈 30-Year Summary Comparison")
col1, col2, col3 = st.columns(3)

btl_final = btl_analysis['yearly_analysis'][-1]
btr_final = btr_analysis['yearly_analysis'][-1]
ri_final = ri_analysis['yearly_analysis'][-1]

with col1:
    st.metric("🏡 Buy to Live", format_currency(btl_final['net_worth']), f"ROI: {btl_final['roi_percent']:.1f}%")
    st.metric("Initial Investment", format_currency(btl_analysis['total_upfront_costs']))
    st.metric("Total Cash Invested", format_currency(btl_final['net_cash_invested']))
    st.caption(f"Includes: Deposit {format_currency(btl_analysis['initial_deposit'])}, Stamp Duty {format_currency(btl_analysis['stamp_duty'])}, Legal {format_currency(btl_analysis['upfront_costs'])}")

with col2:
    st.metric("🏠 Buy to Rent", format_currency(btr_final['net_worth']), f"ROI: {btr_final['roi_percent']:.1f}%")
    st.metric("Initial Investment", format_currency(btr_analysis['total_upfront_costs']))
    st.metric("Total Cash Invested", format_currency(btr_final['net_cash_invested']))
    st.caption(f"Includes: Deposit {format_currency(btr_analysis['initial_deposit'])}, Stamp Duty {format_currency(btr_analysis['stamp_duty'])}, Legal {format_currency(btr_analysis['upfront_costs'])}")

with col3:
    st.metric("📈 Rent & Invest", format_currency(ri_final['stock_portfolio_value']), f"ROI: {ri_final['roi_percent']:.1f}%")
    st.metric("Initial Investment", format_currency(ri_analysis['initial_investment']))
    st.metric("Total Cash Invested", format_currency(ri_final['net_cash_invested']))
    st.caption(f"Includes: Deposit Equiv {format_currency(ri_analysis['deposit_equivalent'])}, Stamp Duty Equiv {format_currency(ri_analysis['stamp_duty_equivalent'])}, Legal {format_currency(ri_analysis['upfront_costs_equivalent'])}")

# Combined Charts
st.header("📊 Comparative Analysis")

# Prepare data for combined charts
btl_df = pd.DataFrame(btl_analysis['yearly_analysis'])
btr_df = pd.DataFrame(btr_analysis['yearly_analysis'])
ri_df = pd.DataFrame(ri_analysis['yearly_analysis'])

# Net Worth vs Investment Chart
st.subheader("💰 Net Worth vs Cumulative Cash Investment")

fig_combined = make_subplots(specs=[[{"secondary_y": False}]])

# Buy to Live
fig_combined.add_trace(
    go.Scatter(
        x=btl_df['year'], 
        y=btl_df['net_worth'], 
        name='🏡 Buy to Live (Net Worth)', 
        line=dict(color='green', width=3),
        hovertemplate="Year %{x}<br>Buy to Live Net Worth: %{customdata[0]}<extra></extra>",
        customdata=[[format_hover_currency(val)] for val in btl_df['net_worth']]
    )
)

fig_combined.add_trace(
    go.Scatter(
        x=btl_df['year'], 
        y=btl_df['net_cash_invested'], 
        name='🏡 Buy to Live (Investment)', 
        line=dict(color='green', width=2, dash='dash'),
        hovertemplate="Year %{x}<br>Buy to Live Investment: %{customdata[0]}<extra></extra>",
        customdata=[[format_hover_currency(val)] for val in btl_df['net_cash_invested']]
    )
)

# Buy to Rent
fig_combined.add_trace(
    go.Scatter(
        x=btr_df['year'], 
        y=btr_df['net_worth'], 
        name='🏠 Buy to Rent (Net Worth)', 
        line=dict(color='blue', width=3),
        hovertemplate="Year %{x}<br>Buy to Rent Net Worth: %{customdata[0]}<extra></extra>",
        customdata=[[format_hover_currency(val)] for val in btr_df['net_worth']]
    )
)

fig_combined.add_trace(
    go.Scatter(
        x=btr_df['year'], 
        y=btr_df['net_cash_invested'], 
        name='🏠 Buy to Rent (Investment)', 
        line=dict(color='blue', width=2, dash='dash'),
        hovertemplate="Year %{x}<br>Buy to Rent Investment: %{customdata[0]}<extra></extra>",
        customdata=[[format_hover_currency(val)] for val in btr_df['net_cash_invested']]
    )
)

# Rent & Invest
fig_combined.add_trace(
    go.Scatter(
        x=ri_df['year'], 
        y=ri_df['stock_portfolio_value'], 
        name='📈 Rent & Invest (Net Worth)', 
        line=dict(color='purple', width=3),
        hovertemplate="Year %{x}<br>Rent & Invest Portfolio: %{customdata[0]}<extra></extra>",
        customdata=[[format_hover_currency(val)] for val in ri_df['stock_portfolio_value']]
    )
)

fig_combined.add_trace(
    go.Scatter(
        x=ri_df['year'], 
        y=ri_df['net_cash_invested'], 
        name='📈 Rent & Invest (Investment)', 
        line=dict(color='purple', width=2, dash='dash'),
        hovertemplate="Year %{x}<br>Rent & Invest Investment: %{customdata[0]}<extra></extra>",
        customdata=[[format_hover_currency(val)] for val in ri_df['net_cash_invested']]
    )
)

fig_combined.update_xaxes(title_text="Year")
fig_combined.update_yaxes(title_text="Amount ($)")

fig_combined.update_layout(
    title="Net Worth (solid lines) vs Cumulative Cash Investment (dashed lines)",
    hovermode='x unified',
    height=600,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_combined, use_container_width=True)

# ROI Comparison Chart
st.subheader("📈 Return on Investment (ROI) Comparison")

fig_roi = go.Figure()

fig_roi.add_trace(
    go.Scatter(
        x=btl_df['year'], 
        y=btl_df['roi_percent'], 
        name='🏡 Buy to Live',
        line=dict(color='green', width=3),
        hovertemplate="Year %{x}<br>Buy to Live ROI: %{customdata[0]}<extra></extra>",
        customdata=[[format_hover_percent(val)] for val in btl_df['roi_percent']]
    )
)

fig_roi.add_trace(
    go.Scatter(
        x=btr_df['year'], 
        y=btr_df['roi_percent'], 
        name='🏠 Buy to Rent',
        line=dict(color='blue', width=3),
        hovertemplate="Year %{x}<br>Buy to Rent ROI: %{customdata[0]}<extra></extra>",
        customdata=[[format_hover_percent(val)] for val in btr_df['roi_percent']]
    )
)

fig_roi.add_trace(
    go.Scatter(
        x=ri_df['year'], 
        y=ri_df['roi_percent'], 
        name='📈 Rent & Invest',
        line=dict(color='purple', width=3),
        hovertemplate="Year %{x}<br>Rent & Invest ROI: %{customdata[0]}<extra></extra>",
        customdata=[[format_hover_percent(val)] for val in ri_df['roi_percent']]
    )
)

fig_roi.update_xaxes(title_text="Year")
fig_roi.update_yaxes(title_text="ROI Percentage (%)")

fig_roi.update_layout(
    title="Return on Investment Comparison Over Time",
    hovermode='x unified',
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_roi, use_container_width=True)

# Milestone Comparison Table
st.subheader("📊 Key Milestone Comparison")

milestones = [5, 10, 15, 20, 30]
comparison_data = []

for year in milestones:
    if year <= len(btl_df) and year <= len(btr_df) and year <= len(ri_df):
        btl_data = btl_df.iloc[year-1]
        btr_data = btr_df.iloc[year-1]
        ri_data = ri_df.iloc[year-1]
        
        comparison_data.append({
            'Year': year,
            '🏡 Buy to Live Net Worth': format_currency(btl_data['net_worth']),
            '🏡 Buy to Live ROI': f"{btl_data['roi_percent']:.1f}%",
            '🏠 Buy to Rent Net Worth': format_currency(btr_data['net_worth']),
            '🏠 Buy to Rent ROI': f"{btr_data['roi_percent']:.1f}%",
            '📈 Rent & Invest Portfolio': format_currency(ri_data['stock_portfolio_value']),
            '📈 Rent & Invest ROI': f"{ri_data['roi_percent']:.1f}%"
        })

st.table(pd.DataFrame(comparison_data))

# Input Summary
st.subheader("📋 Current Input Summary")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Shared Parameters:**")
    st.write(f"• Deposit: {deposit_percent*100:.0f}%")
    st.write(f"• Interest Rate: {interest_rate*100:.1f}%")
    st.write(f"• Loan Term: {loan_term} years")
    st.write(f"• Property Growth: {property_growth_rate*100:.1f}% p.a.")
    st.write(f"• Rental Inflation: {rental_inflation_rate*100:.1f}% p.a.")
    st.write(f"• Property Expenses: {property_expenses_percent*100:.1f}% p.a.")

with col2:
    st.markdown("**Scenario-Specific:**")
    st.write(f"• Your Weekly Rent: ${your_weekly_rent:,.0f}")
    st.write(f"• Stock Market Return: {stock_return_rate*100:.1f}% p.a.")
    st.write(f"• Buy to Live Property: ${btl_property_price:,.0f}")
    st.write(f"• Investment Property: ${btr_property_price:,.0f}")
    st.write(f"• Investment Property Rent: ${btr_weekly_rental:,.0f}/week")

# Annual Net Cash Flows & Net Worth Table
st.subheader("💰 Annual Net Cash Flows & Net Worth by Year")

# Create year-by-year cash flow and net worth table
max_years = min(len(btl_df), len(btr_df), len(ri_df))
cash_flow_data = []

# Year 0 (Initial upfront costs including stamp duty)
cash_flow_data.append({
    'Year': 0,
    '🏡 Cash Flow': format_currency(-btl_analysis['total_upfront_costs']),
    '🏡 Net Worth': format_currency(0),  # No net worth yet
    '🏠 Cash Flow': format_currency(-btr_analysis['total_upfront_costs']),
    '🏠 Net Worth': format_currency(0),  # No net worth yet
    '📈 Cash Flow': format_currency(-ri_analysis['initial_investment']),
    '📈 Net Worth': format_currency(0)   # No net worth yet
})

# Years 1 to max_years
for year in range(1, max_years + 1):
    btl_row = btl_df.iloc[year-1]
    btr_row = btr_df.iloc[year-1]
    ri_row = ri_df.iloc[year-1]
    
    # Calculate net cash flow for each scenario (negative = outflow, positive = inflow)
    btl_net_flow = -btl_row['annual_housing_cost']  # Housing costs (outflow)
    
    btr_net_flow = btr_row['annual_rental_income'] - btr_row['annual_mortgage_payments'] - btr_row['annual_property_expenses'] - btr_row['annual_your_rent']  # Rental income minus all costs
    
    ri_net_flow = -ri_row['annual_rent_cost'] - ri_row['annual_net_investment']  # Rent and stock investments (outflows)
    
    cash_flow_data.append({
        'Year': year,
        '🏡 Cash Flow': format_currency(btl_net_flow),
        '🏡 Net Worth': format_currency(btl_row['net_worth']),
        '🏠 Cash Flow': format_currency(btr_net_flow),
        '🏠 Net Worth': format_currency(btr_row['net_worth']), 
        '📈 Cash Flow': format_currency(ri_net_flow),
        '📈 Net Worth': format_currency(ri_row['stock_portfolio_value'])
    })

# Display the table
cash_flow_df = pd.DataFrame(cash_flow_data)
st.dataframe(cash_flow_df, height=400, use_container_width=True)

st.caption("*Cash Flow: Negative = outflows (expenses), Positive = net inflows. Net Worth: Total wealth accumulated. Year 0 shows initial upfront costs and zero net worth.*")

# Footer
st.markdown("---")
st.markdown("*Disclaimer: This calculator is for educational purposes only. Please consult with a qualified financial advisor for personalized investment advice.*") 