"""
Australian Property Investment Calculator - Restructured Application
Uses domain-driven design with modular components.
"""

import streamlit as st

# Import the new modular components
from src.domain.scenarios.scenario_calculator import ScenarioCalculator
from src.ui.components.input_forms import InputFormManager
from src.ui.components.charts import ChartManager
from src.ui.components.summary_tables import SummaryTableManager
from src.config.defaults import DEFAULT_ANALYSIS_YEARS


def main():
    """Main application entry point."""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="Australian Property Investment Calculator",
        page_icon="🏠",
        layout="wide"
    )
    
    # Initialize managers
    scenario_calc = ScenarioCalculator()
    input_manager = InputFormManager()
    chart_manager = ChartManager()
    summary_manager = SummaryTableManager()
    
    # App header
    st.title("🏠 Australian Property Investment Comparison")
    st.markdown("**Compare all three investment strategies side-by-side with comprehensive analysis**")
    
    # Input sections
    st.header("🔧 Investment Parameters")
    
    # Collect all input parameters
    params = input_manager.render_all_inputs()
    
    # Calculate all scenarios
    st.header("📊 Scenario Calculations")
    
    with st.spinner("Calculating scenarios..."):
        # Buy to Live scenario
        btl_analysis = scenario_calc.calculate_buy_to_live_scenario(
            property_price=params['btl_property_price'],
            deposit_percent=params['deposit_percent'],
            interest_rate=params['interest_rate'],
            loan_term=params['loan_term'],
            annual_property_growth_rate=params['property_growth_rate'],
            annual_property_expenses_percent=params['property_expenses_percent'],
            upfront_costs=params['upfront_costs'],
            is_first_home_buyer=params['is_first_home_buyer'],
            analysis_years=DEFAULT_ANALYSIS_YEARS
        )
        
        # Buy to Rent scenario
        btr_analysis = scenario_calc.calculate_buy_to_rent_scenario(
            investment_property_price=params['btr_property_price'],
            deposit_percent=params['deposit_percent'],
            interest_rate=params['interest_rate'],
            loan_term=params['loan_term'],
            weekly_rental_income=params['btr_weekly_rental'],
            your_weekly_rent=params['your_weekly_rent'],
            annual_property_growth_rate=params['property_growth_rate'],
            annual_rental_inflation_rate=params['rental_inflation_rate'],
            annual_property_expenses_percent=params['property_expenses_percent'],
            upfront_costs=params['upfront_costs'],
            is_first_home_buyer=params['is_first_home_buyer'],
            analysis_years=DEFAULT_ANALYSIS_YEARS,
            annual_gross_income=params['annual_gross_income'],
            salary_growth_rate=params['salary_growth_rate']
        )
        
        # Rent & Invest scenario (with BTL housing costs for comparison)
        btl_housing_costs = [year_data['annual_housing_cost'] for year_data in btl_analysis['yearly_analysis']]
        ri_analysis = scenario_calc.calculate_rent_and_invest_scenario(
            equivalent_property_price=params['ri_equivalent_property_price'],
            deposit_percent=params['deposit_percent'],
            your_weekly_rent=params['your_weekly_rent'],
            annual_stock_return_rate=params['stock_return_rate'],
            annual_rental_inflation_rate=params['rental_inflation_rate'],
            upfront_costs=params['upfront_costs'],
            is_first_home_buyer=params['is_first_home_buyer'],
            analysis_years=DEFAULT_ANALYSIS_YEARS,
            btl_housing_costs=btl_housing_costs
        )
        
        # Apply capital gains tax
        btl_analysis, btr_analysis, ri_analysis = scenario_calc.apply_capital_gains_tax(
            btl_analysis=btl_analysis,
            btr_analysis=btr_analysis,
            ri_analysis=ri_analysis,
            annual_gross_income=params['annual_gross_income'],
            salary_growth_rate=params['salary_growth_rate']
        )
    
    # Display results
    st.success("✅ Calculations complete!")
    
    # Summary metrics only (top cards)
    summary_manager.render_summary_metrics(
        btl_analysis=btl_analysis,
        btr_analysis=btr_analysis,
        ri_analysis=ri_analysis,
        annual_gross_income=params['annual_gross_income']
    )
    
    # Charts
    chart_manager.render_all_charts(
        btl_analysis=btl_analysis,
        btr_analysis=btr_analysis,
        ri_analysis=ri_analysis
    )
    
    # Tables (milestone comparison, cash flow table, simplified input summary)
    summary_manager.render_milestone_comparison(btl_analysis, btr_analysis, ri_analysis)
    summary_manager.render_cash_flow_table(btl_analysis, btr_analysis, ri_analysis)
    summary_manager.render_input_summary(params)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "*Disclaimer: This calculator is for educational purposes only. "
        "Please consult with a qualified financial advisor for personalized investment advice.*"
    )


if __name__ == "__main__":
    main() 