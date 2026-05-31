"""
Streamlit input form components for the property investment calculator.
"""

import streamlit as st
from typing import Dict, Any
from ...config.defaults import *
from ...domain.property.stamp_duty import StampDutyCalculator
from ...utils.formatters import format_currency


class InputFormManager:
    """Manages all input forms for the application."""
    
    def __init__(self):
        self.stamp_duty_calc = StampDutyCalculator()
    
    def render_general_assumptions(self) -> Dict[str, Any]:
        """Render the general assumptions input section."""
        st.subheader("📊 General Assumptions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Financial Parameters**")
            analysis_years = st.slider(
                "Analysis Period (years)",
                min_value=10,
                max_value=40,
                value=DEFAULT_ANALYSIS_YEARS,
                help="Projection horizon for all three scenarios"
            )

            deposit_percent = st.slider(
                "Deposit (%)", 
                min_value=5, 
                max_value=50, 
                value=int(DEFAULT_DEPOSIT_PERCENT * 100)
            ) / 100
            
            interest_rate = st.slider(
                "Interest Rate (%)", 
                min_value=1.0, 
                max_value=10.0, 
                value=DEFAULT_INTEREST_RATE * 100, 
                step=0.1
            ) / 100
            
            loan_term = st.slider(
                "Loan Term (years)", 
                min_value=15, 
                max_value=30, 
                value=DEFAULT_LOAN_TERM
            )
        
        with col2:
            st.markdown("**Growth & Inflation**")
            property_growth_rate = st.slider(
                "Annual Property Growth (%)", 
                min_value=0.0, 
                max_value=10.0, 
                value=DEFAULT_PROPERTY_GROWTH_RATE * 100, 
                step=0.1
            ) / 100
            
            rental_inflation_rate = st.slider(
                "Annual Rental Inflation (%)", 
                min_value=0.0, 
                max_value=8.0, 
                value=DEFAULT_RENTAL_INFLATION_RATE * 100, 
                step=0.1
            ) / 100
            
            property_expenses_percent = st.slider(
                "Annual Property Expenses (% of value)", 
                min_value=0.5, 
                max_value=3.0, 
                value=DEFAULT_PROPERTY_EXPENSES_PERCENT * 100, 
                step=0.1
            ) / 100
        
        with col3:
            st.markdown("**Housing & Investment**")
            your_weekly_rent = st.number_input(
                "Your Weekly Rent ($)", 
                value=DEFAULT_YOUR_WEEKLY_RENT, 
                step=25, 
                help="Your rent cost (used in Buy to Rent and Rent & Invest scenarios)"
            )
            
            stock_return_rate = st.slider(
                "Annual Stock Market Return (%)", 
                min_value=1.0, 
                max_value=15.0, 
                value=DEFAULT_STOCK_RETURN_RATE * 100, 
                step=0.1, 
                help="Expected return for Rent & Invest scenario"
            ) / 100
            
            upfront_costs = st.number_input(
                "Upfront Costs ($)", 
                value=DEFAULT_UPFRONT_COSTS, 
                step=500, 
                help="Legal fees, inspections, conveyancing"
            )
        
        return {
            'analysis_years': analysis_years,
            'deposit_percent': deposit_percent,
            'interest_rate': interest_rate,
            'loan_term': loan_term,
            'property_growth_rate': property_growth_rate,
            'rental_inflation_rate': rental_inflation_rate,
            'property_expenses_percent': property_expenses_percent,
            'your_weekly_rent': your_weekly_rent,
            'stock_return_rate': stock_return_rate,
            'upfront_costs': upfront_costs
        }
    
    def render_tax_considerations(self) -> Dict[str, Any]:
        """Render the tax considerations input section."""
        st.subheader("💰 Tax Considerations")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Income & Tax**")
            annual_gross_income = st.number_input(
                "Annual Gross Income ($)", 
                value=DEFAULT_ANNUAL_GROSS_INCOME, 
                step=5000, 
                help="Your current gross annual income for tax calculations"
            )
            
            salary_growth_rate = st.slider(
                "Annual Salary Growth (%)", 
                min_value=0.0, 
                max_value=8.0, 
                value=DEFAULT_SALARY_GROWTH_RATE * 100, 
                step=0.1, 
                help="Expected annual salary increase"
            ) / 100
        
        with col2:
            st.markdown("**Capital Gains Tax & Negative Gearing**")
            st.info("🏡 Buy to Live: **CGT Exempt** (main residence)")
            st.warning(
                "🏠 Buy to Rent (non-new-build): **No CGT discount** — minimum 30% effective tax "
                "(2026-27 Budget reform, purchases after 12 May 2026)"
            )
            st.warning(
                "🏠 Buy to Rent (non-new-build): **Negative gearing losses quarantined** — "
                "cannot offset general income (2026-27 Budget reform)"
            )
            st.success(
                "🏠 Buy to Rent (new build): **Full negative gearing** + choice of 50% CGT discount "
                "or new inflation-indexed arrangement"
            )
            st.warning("📈 Rent & Invest: **CGT on stocks** (50% discount if held >12 months)")
        
        return {
            'annual_gross_income': annual_gross_income,
            'salary_growth_rate': salary_growth_rate
        }
    
    def render_scenario_parameters(self) -> Dict[str, Any]:
        """Render the scenario-specific parameters section."""
        st.subheader("🏠 Scenario-Specific Parameters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🏡 Buy to Live**")
            btl_property_price = st.number_input(
                "Home Property Price ($)", 
                value=DEFAULT_BTL_PROPERTY_PRICE, 
                step=10000, 
                help="Price of the home you would buy to live in"
            )
            
            is_first_home_buyer = st.checkbox(
                "First Home Buyer", 
                value=False, 
                help="Check if eligible for first home buyer stamp duty concessions"
            )
            
            # Show stamp duty preview
            if btl_property_price > 0:
                self._show_stamp_duty_preview(btl_property_price, is_first_home_buyer)
        
        with col2:
            st.markdown("**🏠 Buy to Rent**")
            btr_property_price = st.number_input(
                "Investment Property Price ($)",
                value=DEFAULT_BTR_PROPERTY_PRICE,
                step=10000,
                help="Price of investment property"
            )

            btr_weekly_rental = st.number_input(
                "Weekly Rental Income ($)",
                value=DEFAULT_BTR_WEEKLY_RENTAL,
                step=25,
                help="Expected weekly rent from investment property"
            )

            is_new_build = st.checkbox(
                "New Build",
                value=False,
                help=(
                    "2026-27 Budget reform: new builds retain full negative gearing and may choose "
                    "the old 50% CGT discount. Non-new-builds bought after 12 May 2026 have losses "
                    "quarantined and face a minimum 30% CGT rate."
                )
            )

            # Show stamp duty for investment property
            if btr_property_price > 0:
                investment_stamp_duty = self.stamp_duty_calc.calculate_stamp_duty(btr_property_price, False)
                st.info(f"ℹ️ Investment Property Stamp Duty: {format_currency(investment_stamp_duty)}")
        
        with col3:
            st.markdown("**📈 Rent & Invest**")
            ri_equivalent_property_price = st.number_input(
                "Equivalent Property Price ($)", 
                value=DEFAULT_RI_EQUIVALENT_PROPERTY_PRICE, 
                step=10000, 
                help="Price of equivalent property for comparison (typically same as Buy to Live)"
            )
        
        return {
            'btl_property_price': btl_property_price,
            'is_first_home_buyer': is_first_home_buyer,
            'btr_property_price': btr_property_price,
            'btr_weekly_rental': btr_weekly_rental,
            'is_new_build': is_new_build,
            'ri_equivalent_property_price': ri_equivalent_property_price
        }
    
    def _show_stamp_duty_preview(self, property_price: float, is_first_home_buyer: bool):
        """Show stamp duty preview with first home buyer savings."""
        standard_stamp_duty = self.stamp_duty_calc.calculate_stamp_duty(property_price, False)
        fhb_stamp_duty = self.stamp_duty_calc.calculate_stamp_duty(property_price, True)
        
        if is_first_home_buyer:
            savings = standard_stamp_duty - fhb_stamp_duty
            if savings > 0:
                st.success(f"🎉 FHB Saving: {format_currency(savings)} (Stamp Duty: {format_currency(fhb_stamp_duty)})")
            else:
                st.info(f"ℹ️ Stamp Duty: {format_currency(fhb_stamp_duty)}")
        else:
            st.info(f"ℹ️ Stamp Duty: {format_currency(standard_stamp_duty)}")
    
    def render_all_inputs(self) -> Dict[str, Any]:
        """Render all input sections and return combined parameters."""
        general_params = self.render_general_assumptions()
        tax_params = self.render_tax_considerations()
        scenario_params = self.render_scenario_parameters()
        
        # Combine all parameters
        return {**general_params, **tax_params, **scenario_params} 
