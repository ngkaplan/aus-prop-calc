"""
Australian Property Investment Calculator - Restructured Demo
This demonstrates the domain-driven architecture while using existing calculations for compatibility.
"""

import streamlit as st

# Import existing calculation functions for compatibility
from calculations import (
    calculate_buy_to_live_net_worth_analysis,
    calculate_net_worth_analysis,
    calculate_rent_and_invest_analysis,
    apply_capital_gains_tax_to_scenarios,
    calculate_marginal_tax_rate
)

# Import the new modular components
from src.ui.components.input_forms import InputFormManager
from src.ui.components.charts import ChartManager
from src.ui.components.summary_tables import SummaryTableManager
from src.config.defaults import DEFAULT_ANALYSIS_YEARS


def main():
    """Main application entry point demonstrating the new architecture."""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="Australian Property Investment Calculator - Restructured",
        page_icon="🏠",
        layout="wide"
    )
    
    # Initialize UI managers (demonstrating modular components)
    input_manager = InputFormManager()
    chart_manager = ChartManager()
    summary_manager = SummaryTableManager()
    
    # App header
    st.title("🏠 Australian Property Investment Comparison")
    st.markdown("**Restructured with Domain-Driven Design** 🎯")
    st.info("✨ This demonstrates the new modular architecture with separated domains and UI components")
    
    # Input sections using new modular input manager
    st.header("🔧 Investment Parameters")
    
    # Collect all input parameters using the new InputFormManager
    params = input_manager.render_all_inputs()
    
    # Calculate all scenarios using existing functions for compatibility
    st.header("📊 Scenario Calculations")
    
    with st.spinner("Calculating scenarios using modular architecture..."):
        # Use existing calculation functions to maintain compatibility
        btl_analysis = calculate_buy_to_live_net_worth_analysis(
            params['btl_property_price'], 
            params['deposit_percent'], 
            params['interest_rate'], 
            params['loan_term'], 
            params['property_growth_rate'], 
            params['property_expenses_percent'], 
            params['upfront_costs'], 
            params['is_first_home_buyer']
        )
        
        btr_analysis = calculate_net_worth_analysis(
            params['btr_property_price'], 
            params['deposit_percent'], 
            params['interest_rate'], 
            params['loan_term'],
            params['btr_weekly_rental'], 
            params['your_weekly_rent'], 
            params['property_growth_rate'], 
            params['rental_inflation_rate'], 
            params['property_expenses_percent'], 
            params['upfront_costs'],
            params['annual_gross_income'], 
            params['salary_growth_rate']
        )
        
        ri_analysis = calculate_rent_and_invest_analysis(
            params['ri_equivalent_property_price'], 
            params['deposit_percent'], 
            params['interest_rate'], 
            DEFAULT_ANALYSIS_YEARS,
            params['your_weekly_rent'], 
            params['stock_return_rate'], 
            params['rental_inflation_rate'], 
            params['property_growth_rate'],
            params['property_expenses_percent'], 
            params['upfront_costs'], 
            params['is_first_home_buyer']
        )
        
        # Apply capital gains tax
        btl_analysis, btr_analysis, ri_analysis = apply_capital_gains_tax_to_scenarios(
            btl_analysis, btr_analysis, ri_analysis, 
            params['annual_gross_income'], params['salary_growth_rate']
        )
    
    # Display results using new modular UI components
    st.success("✅ Calculations complete using restructured architecture!")
    
    # Architecture demonstration
    with st.expander("🏗️ **New Architecture Overview**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Domain Layer:**")
            st.code("""
src/domain/
├── tax/
│   └── australian_tax.py      # Tax calculations
├── property/
│   ├── stamp_duty.py         # Stamp duty logic
│   └── mortgage.py           # Mortgage calculations
├── investment/
│   └── stock_calculator.py   # Stock investment logic
└── scenarios/
    └── scenario_calculator.py # Main orchestrator
            """)
        
        with col2:
            st.markdown("**UI Layer:**")
            st.code("""
src/ui/
└── components/
    ├── input_forms.py        # Input form management
    ├── charts.py            # Chart visualization
    └── summary_tables.py    # Summary displays

src/utils/
├── formatters.py            # Currency/percent formatting
└── validators.py            # Input validation

src/config/
├── defaults.py              # Default values
└── australian_config.py     # AU-specific constants
            """)
    
    # Summary metrics and tables using new SummaryTableManager
    summary_manager.render_all_summaries(
        btl_analysis=btl_analysis,
        btr_analysis=btr_analysis,
        ri_analysis=ri_analysis,
        params=params
    )
    
    # Charts using new ChartManager
    chart_manager.render_all_charts(
        btl_analysis=btl_analysis,
        btr_analysis=btr_analysis,
        ri_analysis=ri_analysis
    )
    
    # Architecture benefits
    st.header("🎯 Benefits of New Architecture")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏗️ Modularity**")
        st.write("• Separated concerns by domain")
        st.write("• Reusable components")
        st.write("• Easier testing")
        st.write("• Clear dependencies")
    
    with col2:
        st.markdown("**🔧 Maintainability**")
        st.write("• Single responsibility principle")
        st.write("• Domain expertise isolation")
        st.write("• Simplified debugging")
        st.write("• Enhanced readability")
    
    with col3:
        st.markdown("**📈 Scalability**")
        st.write("• Easy to add new scenarios")
        st.write("• Simple UI component updates")
        st.write("• Configuration management")
        st.write("• Plugin architecture ready")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "*This restructured version demonstrates domain-driven design principles. "
        "All calculations remain identical to ensure accuracy while improving code organization.*"
    )


if __name__ == "__main__":
    main() 