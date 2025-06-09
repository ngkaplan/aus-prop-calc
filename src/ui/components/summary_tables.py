"""
Summary tables and comparison components for displaying scenario results.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from ...utils.formatters import format_currency
from ...domain.tax.australian_tax import AustralianTaxCalculator


class SummaryTableManager:
    """Manages summary displays and comparison tables for the application."""
    
    def __init__(self):
        self.tax_calc = AustralianTaxCalculator()
    
    def render_summary_metrics(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any],
        annual_gross_income: float
    ):
        """Render the 30-year summary comparison metrics."""
        st.subheader("📈 30-Year Summary Comparison")
        
        # Show current marginal tax rate
        current_marginal_rate = self.tax_calc.calculate_marginal_tax_rate(annual_gross_income)
        st.info(f"💡 **Current Marginal Tax Rate:** {current_marginal_rate*100:.1f}% (includes Medicare levy)")
        
        col1, col2, col3 = st.columns(3)
        
        btl_final = btl_analysis['yearly_analysis'][-1]
        btr_final = btr_analysis['yearly_analysis'][-1]
        ri_final = ri_analysis['yearly_analysis'][-1]
        
        with col1:
            self._render_btl_summary(btl_analysis, btl_final)
        
        with col2:
            self._render_btr_summary(btr_analysis, btr_final)
        
        with col3:
            self._render_ri_summary(ri_analysis, ri_final)
    
    def _render_btl_summary(self, btl_analysis: Dict[str, Any], btl_final: Dict[str, Any]):
        """Render Buy to Live summary card."""
        st.metric(
            "🏡 Buy to Live", 
            format_currency(btl_final['net_worth']), 
            f"ROI: {btl_final['roi_percent']:.1f}%"
        )
        st.metric("Initial Investment", format_currency(btl_analysis['total_upfront_costs']))
        st.metric("Total Cash Invested", format_currency(btl_final['net_cash_invested']))
        st.success("✅ **CGT Exempt** (main residence)")
        st.caption(
            f"Includes: Deposit {format_currency(btl_analysis['initial_deposit'])}, "
            f"Stamp Duty {format_currency(btl_analysis['stamp_duty'])}, "
            f"Legal {format_currency(btl_analysis['upfront_costs'])}"
        )
    
    def _render_btr_summary(self, btr_analysis: Dict[str, Any], btr_final: Dict[str, Any]):
        """Render Buy to Rent summary card."""
        net_worth_before_tax = btr_final['net_worth']
        net_worth_after_tax = btr_final['net_worth_after_tax']
        cgt_liability = btr_final['cgt_liability']
        negative_gearing_benefits = btr_final['cumulative_negative_gearing_benefits']
        
        roi_after_tax = ((net_worth_after_tax - btr_final['net_cash_invested']) / 
                        btr_final['net_cash_invested'] * 100) if btr_final['net_cash_invested'] > 0 else 0
        
        st.metric(
            "🏠 Buy to Rent (After Tax)", 
            format_currency(net_worth_after_tax), 
            f"ROI: {roi_after_tax:.1f}%"
        )
        st.metric("Before Tax + Neg. Gearing", format_currency(net_worth_before_tax))
        st.metric("CGT Liability", format_currency(cgt_liability))
        st.success(f"💰 **Negative Gearing Benefits:** +{format_currency(negative_gearing_benefits)}")
        st.warning(f"⚠️ **CGT Impact:** -{format_currency(cgt_liability)}")
        st.caption(
            f"Includes: Deposit {format_currency(btr_analysis['initial_deposit'])}, "
            f"Stamp Duty {format_currency(btr_analysis['stamp_duty'])}, "
            f"Legal {format_currency(btr_analysis['upfront_costs'])}"
        )
    
    def _render_ri_summary(self, ri_analysis: Dict[str, Any], ri_final: Dict[str, Any]):
        """Render Rent & Invest summary card."""
        portfolio_before_tax = ri_final['stock_portfolio_value']
        portfolio_after_tax = ri_final['net_worth_after_tax']
        cgt_liability = ri_final['cgt_liability']
        
        roi_after_tax = ((portfolio_after_tax - ri_final['net_cash_invested']) / 
                        ri_final['net_cash_invested'] * 100) if ri_final['net_cash_invested'] > 0 else 0
        
        st.metric(
            "📈 Rent & Invest (After Tax)", 
            format_currency(portfolio_after_tax), 
            f"ROI: {roi_after_tax:.1f}%"
        )
        st.metric("Before Tax", format_currency(portfolio_before_tax))
        st.metric("CGT Liability", format_currency(cgt_liability))
        st.warning(f"⚠️ **CGT Impact:** -{format_currency(cgt_liability)}")
        st.caption(
            f"Includes: Deposit Equiv {format_currency(ri_analysis['deposit_equivalent'])}, "
            f"Stamp Duty Equiv {format_currency(ri_analysis['stamp_duty_equivalent'])}, "
            f"Legal {format_currency(ri_analysis['upfront_costs_equivalent'])}"
        )
    
    def render_milestone_comparison(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any]
    ):
        """Render the milestone comparison table."""
        st.subheader("📊 Key Milestone Comparison")
        
        btl_df = pd.DataFrame(btl_analysis['yearly_analysis'])
        btr_df = pd.DataFrame(btr_analysis['yearly_analysis'])
        ri_df = pd.DataFrame(ri_analysis['yearly_analysis'])
        
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
    
    def render_cash_flow_table(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any]
    ):
        """Render the annual cash flows and net worth table."""
        try:
            st.subheader("💰 Annual Net Cash Flows & Net Worth by Year")
            
            btl_df = pd.DataFrame(btl_analysis['yearly_analysis'])
            btr_df = pd.DataFrame(btr_analysis['yearly_analysis'])
            ri_df = pd.DataFrame(ri_analysis['yearly_analysis'])
            
            max_years = min(len(btl_df), len(btr_df), len(ri_df))
            st.write(f"Displaying {max_years} years of data")
            
            cash_flow_data = []
            
            # Year 0 (Initial upfront costs)
            cash_flow_data.append({
                'Year': 0,
                '🏡 Cash Flow': format_currency(-btl_analysis['total_upfront_costs']),
                '🏡 Net Worth': format_currency(0),
                '🏠 Cash Flow': format_currency(-btr_analysis['total_upfront_costs']),
                '🏠 Net Worth': format_currency(0),
                '📈 Cash Flow': format_currency(-ri_analysis['initial_investment']),
                '📈 Net Worth': format_currency(0)
            })
            
            # Years 1 to max_years
            for year in range(1, max_years + 1):
                btl_row = btl_df.iloc[year-1]
                btr_row = btr_df.iloc[year-1]
                ri_row = ri_df.iloc[year-1]
                
                # Calculate net cash flow for each scenario
                btl_net_flow = -btl_row['annual_housing_cost']
                
                btr_net_flow = (btr_row['annual_rental_income'] - 
                              btr_row['annual_mortgage_payments'] - 
                              btr_row['annual_property_expenses'] - 
                              btr_row['annual_your_rent'] + 
                              btr_row['annual_negative_gearing_benefit'])
                
                # For RI, calculate the equivalent housing cost that should be invested
                # This represents rent + the amount that should be invested to match housing costs
                btl_equivalent_cost = btl_row['annual_housing_cost']  # What BTL person spends on housing
                ri_actual_rent = ri_row['annual_rent_cost']  # What RI person spends on rent
                ri_should_invest = btl_equivalent_cost - ri_actual_rent  # Difference should be invested
                ri_net_flow = -ri_actual_rent - ri_should_invest  # Total cash outflow
                
                cash_flow_data.append({
                    'Year': year,
                    '🏡 Cash Flow': format_currency(btl_net_flow),
                    '🏡 Net Worth': format_currency(btl_row['net_worth']),
                    '🏠 Cash Flow': format_currency(btr_net_flow),
                    '🏠 Net Worth': format_currency(btr_row['net_worth_after_tax']),
                    '📈 Cash Flow': format_currency(ri_net_flow),
                    '📈 Net Worth': format_currency(ri_row['net_worth_after_tax'])
                })
            
            cash_flow_df = pd.DataFrame(cash_flow_data)
            st.dataframe(cash_flow_df, height=400, use_container_width=True)
            
            st.caption(
                "*Cash Flow: Negative = outflows (expenses), Positive = net inflows. "
                "Net Worth: Total wealth accumulated (after capital gains tax for Buy to Rent and Rent & Invest). "
                "Year 0 shows initial upfront costs and zero net worth.*"
            )
        except Exception as e:
            st.error(f"Error rendering cash flow table: {str(e)}")
            st.write("Debugging information:")
            st.write(f"BTL keys: {list(btl_analysis.keys())}")
            st.write(f"BTR keys: {list(btr_analysis.keys())}")
            st.write(f"RI keys: {list(ri_analysis.keys())}")
            if 'yearly_analysis' in btl_analysis:
                st.write(f"BTL yearly keys: {list(btl_analysis['yearly_analysis'][0].keys())}")
            if 'yearly_analysis' in btr_analysis:
                st.write(f"BTR yearly keys: {list(btr_analysis['yearly_analysis'][0].keys())}")
            if 'yearly_analysis' in ri_analysis:
                st.write(f"RI yearly keys: {list(ri_analysis['yearly_analysis'][0].keys())}")
            raise e
    
    def render_input_summary(self, params: Dict[str, Any]):
        """Render simplified assumptions summary."""
        st.subheader("📋 Key Assumptions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Fixed Assumptions:**")
            st.write(f"• Property Expenses: {params['property_expenses_percent']*100:.1f}% p.a.")
            st.write(f"• Upfront Costs: {format_currency(params['upfront_costs'])}")
            st.write(f"• Analysis Period: 30 years")
        
        with col2:
            st.markdown("**Growth Rates:**")
            st.write(f"• Property Growth: {params['property_growth_rate']*100:.1f}% p.a.")
            st.write(f"• Rental Inflation: {params['rental_inflation_rate']*100:.1f}% p.a.")
            st.write(f"• Salary Growth: {params['salary_growth_rate']*100:.1f}% p.a.")
    
    def render_all_summaries(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any],
        params: Dict[str, Any]
    ):
        """Render all summary components."""
        self.render_summary_metrics(btl_analysis, btr_analysis, ri_analysis, params['annual_gross_income'])
        self.render_milestone_comparison(btl_analysis, btr_analysis, ri_analysis)
        self.render_input_summary(params)
        self.render_cash_flow_table(btl_analysis, btr_analysis, ri_analysis) 