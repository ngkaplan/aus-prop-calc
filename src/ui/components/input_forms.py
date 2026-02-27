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
            st.warning("🏠 Buy to Rent: **CGT on property** (50% discount if held >12 months)")
            st.success("🏠 Buy to Rent: **Negative gearing benefits** (tax deductible losses)")
            st.warning("📈 Rent & Invest: **CGT on stocks** (50% discount if held >12 months)")
        
        return {
            'annual_gross_income': annual_gross_income,
            'salary_growth_rate': salary_growth_rate
        }
    
    def render_scenario_parameters(self) -> Dict[str, Any]:
        """Render the scenario-specific parameters section."""
        st.subheader("🏠 Scenario-Specific Parameters")

        affordability_mode = st.toggle(
            "What I can afford switch",
            value=DEFAULT_USE_AFFORDABILITY_SWITCH,
            help="Back-solve property values from available cash, max borrowing, and LVR limits.",
        )

        affordability_params = {}
        if affordability_mode:
            st.markdown("**Affordability Inputs**")
            aff_col1, aff_col2, aff_col3 = st.columns(3)

            with aff_col1:
                cash_available = st.number_input(
                    "Cash Available Today ($)",
                    min_value=0,
                    value=DEFAULT_CASH_AVAILABLE,
                    step=5000,
                    help="Cash available for deposits and transaction costs.",
                )
                max_borrowing = st.number_input(
                    "Maximum Bank Borrowing ($)",
                    min_value=0,
                    value=DEFAULT_MAX_BORROWING,
                    step=5000,
                    help="Maximum principal your bank will lend.",
                )

            with aff_col2:
                allowed_lvr = st.slider(
                    "Allowed LVR (%)",
                    min_value=50,
                    max_value=100,
                    value=int(DEFAULT_ALLOWED_LVR * 100),
                    help="Maximum loan-to-value ratio permitted for purchase sizing.",
                ) / 100

                include_lmi_above_80_lvr = st.checkbox(
                    "Include LMI above 80% LVR (Investment)",
                    value=DEFAULT_INCLUDE_LMI_ABOVE_80_LVR,
                    help="Required to model investment LVR above 80%.",
                )

            with aff_col3:
                st.info(
                    "In affordability mode, home/investment purchase prices are solved automatically."
                )

            affordability_params = {
                'use_affordability_switch': affordability_mode,
                'cash_available_today': cash_available,
                'max_bank_borrowing': max_borrowing,
                'allowed_lvr': allowed_lvr,
                'include_lmi_above_80_lvr': include_lmi_above_80_lvr
            }

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🏡 Buy to Live**")
            if affordability_mode:
                st.caption("Price solved from affordability inputs.")
                btl_property_price = 0
            else:
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
            if btl_property_price > 0 and not affordability_mode:
                self._show_stamp_duty_preview(btl_property_price, is_first_home_buyer)
        
        with col2:
            st.markdown("**🏠 Buy to Rent**")
            if affordability_mode:
                st.caption("Price solved from affordability inputs.")
                btr_property_price = 0
            else:
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
            
            # Show stamp duty for investment property
            if btr_property_price > 0 and not affordability_mode:
                investment_stamp_duty = self.stamp_duty_calc.calculate_stamp_duty(btr_property_price, False)
                st.info(f"ℹ️ Investment Property Stamp Duty: {format_currency(investment_stamp_duty)}")
        
        with col3:
            st.markdown("**📈 Rent & Invest**")
            if affordability_mode:
                st.caption("Equivalent price set from solved Buy to Live value.")
                ri_equivalent_property_price = 0
            else:
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
            'ri_equivalent_property_price': ri_equivalent_property_price
        } | affordability_params
    
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

    def render_portfolio_growth_inputs(self) -> Dict[str, Any]:
        """Render Stage 1 scaffold inputs for the portfolio growth simulation tab."""
        st.subheader("🏗️ Portfolio Growth Inputs")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Serviceability Rules**")
            assessment_buffer_rate = st.slider(
                "Assessment Buffer Above Actual Rate (%)",
                min_value=1.0,
                max_value=5.0,
                value=DEFAULT_SERVICEABILITY_BUFFER_RATE * 100,
                step=0.25,
                help="Banks often assess at actual rate plus a serviceability buffer.",
            ) / 100
            assessment_rate_floor = st.slider(
                "Assessment Rate Floor (%)",
                min_value=6.0,
                max_value=12.0,
                value=DEFAULT_SERVICEABILITY_RATE_FLOOR * 100,
                step=0.25,
                help="Minimum assessment rate regardless of market rates.",
            ) / 100
            rental_income_haircut = st.slider(
                "Rental Income Haircut (%)",
                min_value=50,
                max_value=100,
                value=int(DEFAULT_RENTAL_INCOME_HAIRCUT * 100),
                step=1,
                help="Percentage of gross rent counted by lender for serviceability.",
            ) / 100

        with col2:
            st.markdown("**Expense + Buffer Rules**")
            bank_expense_floor_monthly = st.number_input(
                "Bank Expense Floor ($/month)",
                min_value=0,
                value=DEFAULT_BANK_EXPENSE_FLOOR_MONTHLY,
                step=100,
                help="Applied as a minimum to serviceability expenses.",
            )
            cash_buffer_months = st.slider(
                "Minimum Cash Buffer (months)",
                min_value=1,
                max_value=24,
                value=DEFAULT_CASH_BUFFER_MONTHS,
                help="Cash to retain post-purchase as months of mortgage + living expenses.",
            )
            review_frequency = st.selectbox(
                "Purchase Review Frequency",
                options=["Yearly", "Quarterly"],
                index=0 if DEFAULT_PORTFOLIO_REVIEW_FREQUENCY == "Yearly" else 1,
                help="How often the model checks if another investment can be purchased.",
            )

        with col3:
            st.markdown("**New Purchase Assumptions**")
            base_investment_purchase_price = st.number_input(
                "Base Investment Price Today ($)",
                min_value=100000,
                value=DEFAULT_BASE_INVESTMENT_PURCHASE_PRICE,
                step=10000,
                help="Reference price for newly added properties in Stage 2+ simulations.",
            )
            new_purchase_gross_rental_yield = st.slider(
                "Gross Rental Yield at Purchase (%)",
                min_value=2.0,
                max_value=10.0,
                value=DEFAULT_NEW_PURCHASE_GROSS_RENTAL_YIELD * 100,
                step=0.1,
                help="Gross rent / purchase price for newly acquired properties.",
            ) / 100
            new_purchase_price_growth_rate = st.slider(
                "New Purchase Price Growth (%)",
                min_value=0.0,
                max_value=10.0,
                value=DEFAULT_NEW_PURCHASE_PRICE_GROWTH_RATE * 100,
                step=0.1,
                help="Growth applied to target purchase price over time.",
            ) / 100

        return {
            'assessment_buffer_rate': assessment_buffer_rate,
            'assessment_rate_floor': assessment_rate_floor,
            'rental_income_haircut': rental_income_haircut,
            'bank_expense_floor_monthly': bank_expense_floor_monthly,
            'cash_buffer_months': cash_buffer_months,
            'review_frequency': review_frequency,
            'base_investment_purchase_price': base_investment_purchase_price,
            'new_purchase_gross_rental_yield': new_purchase_gross_rental_yield,
            'new_purchase_price_growth_rate': new_purchase_price_growth_rate,
        }
    
    def render_all_inputs(self) -> Dict[str, Any]:
        """Render all input sections and return combined parameters."""
        general_params = self.render_general_assumptions()
        tax_params = self.render_tax_considerations()
        scenario_params = self.render_scenario_parameters()
        
        # Combine all parameters
        return {**general_params, **tax_params, **scenario_params} 
