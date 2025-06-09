"""
Chart components for visualizing investment scenario comparisons.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any
from ...utils.formatters import format_hover_currency, format_hover_percent


class ChartManager:
    """Manages all chart creation and display for the application."""
    
    def create_net_worth_comparison_chart(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any]
    ) -> go.Figure:
        """Create the main net worth vs investment comparison chart."""
        
        # Convert to DataFrames
        btl_df = pd.DataFrame(btl_analysis['yearly_analysis'])
        btr_df = pd.DataFrame(btr_analysis['yearly_analysis'])
        ri_df = pd.DataFrame(ri_analysis['yearly_analysis'])
        
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        # Buy to Live
        fig.add_trace(
            go.Scatter(
                x=btl_df['year'], 
                y=btl_df['net_worth'], 
                name='🏡 Buy to Live (Net Worth)', 
                line=dict(color='green', width=3),
                hovertemplate="Year %{x}<br>Buy to Live Net Worth: %{customdata[0]}<extra></extra>",
                customdata=[[format_hover_currency(val)] for val in btl_df['net_worth']]
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=btl_df['year'], 
                y=btl_df['net_cash_invested'], 
                name='🏡 Buy to Live (Investment)', 
                line=dict(color='green', width=2, dash='dash'),
                hovertemplate="Year %{x}<br>Buy to Live Investment: %{customdata[0]}<extra></extra>",
                customdata=[[format_hover_currency(val)] for val in btl_df['net_cash_invested']]
            )
        )
        
        # Buy to Rent (After Tax)
        fig.add_trace(
            go.Scatter(
                x=btr_df['year'], 
                y=btr_df['net_worth_after_tax'], 
                name='🏠 Buy to Rent (After Tax)', 
                line=dict(color='blue', width=3),
                hovertemplate="Year %{x}<br>Buy to Rent After Tax: %{customdata[0]}<extra></extra>",
                customdata=[[format_hover_currency(val)] for val in btr_df['net_worth_after_tax']]
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=btr_df['year'], 
                y=btr_df['net_cash_invested'], 
                name='🏠 Buy to Rent (Investment)', 
                line=dict(color='blue', width=2, dash='dash'),
                hovertemplate="Year %{x}<br>Buy to Rent Investment: %{customdata[0]}<extra></extra>",
                customdata=[[format_hover_currency(val)] for val in btr_df['net_cash_invested']]
            )
        )
        
        # Rent & Invest (After Tax)
        fig.add_trace(
            go.Scatter(
                x=ri_df['year'], 
                y=ri_df['net_worth_after_tax'], 
                name='📈 Rent & Invest (After Tax)', 
                line=dict(color='purple', width=3),
                hovertemplate="Year %{x}<br>Rent & Invest After Tax: %{customdata[0]}<extra></extra>",
                customdata=[[format_hover_currency(val)] for val in ri_df['net_worth_after_tax']]
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=ri_df['year'], 
                y=ri_df['net_cash_invested'], 
                name='📈 Rent & Invest (Investment)', 
                line=dict(color='purple', width=2, dash='dash'),
                hovertemplate="Year %{x}<br>Rent & Invest Investment: %{customdata[0]}<extra></extra>",
                customdata=[[format_hover_currency(val)] for val in ri_df['net_cash_invested']]
            )
        )
        
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Amount ($)")
        
        fig.update_layout(
            title="Net Worth After Tax (solid lines) vs Cumulative Cash Investment (dashed lines)",
            hovermode='x unified',
            height=600,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def create_roi_comparison_chart(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any]
    ) -> go.Figure:
        """Create the ROI comparison chart."""
        
        # Convert to DataFrames
        btl_df = pd.DataFrame(btl_analysis['yearly_analysis'])
        btr_df = pd.DataFrame(btr_analysis['yearly_analysis'])
        ri_df = pd.DataFrame(ri_analysis['yearly_analysis'])
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=btl_df['year'], 
                y=btl_df['roi_percent'], 
                name='🏡 Buy to Live',
                line=dict(color='green', width=3),
                hovertemplate="Year %{x}<br>Buy to Live ROI: %{customdata[0]}<extra></extra>",
                customdata=[[format_hover_percent(val)] for val in btl_df['roi_percent']]
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=btr_df['year'], 
                y=btr_df['roi_percent'], 
                name='🏠 Buy to Rent',
                line=dict(color='blue', width=3),
                hovertemplate="Year %{x}<br>Buy to Rent ROI: %{customdata[0]}<extra></extra>",
                customdata=[[format_hover_percent(val)] for val in btr_df['roi_percent']]
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=ri_df['year'], 
                y=ri_df['roi_percent'], 
                name='📈 Rent & Invest',
                line=dict(color='purple', width=3),
                hovertemplate="Year %{x}<br>Rent & Invest ROI: %{customdata[0]}<extra></extra>",
                customdata=[[format_hover_percent(val)] for val in ri_df['roi_percent']]
            )
        )
        
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="ROI Percentage (%)")
        
        fig.update_layout(
            title="Return on Investment Comparison Over Time",
            hovermode='x unified',
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def render_net_worth_chart(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any]
    ):
        """Render the net worth comparison chart."""
        st.subheader("💰 Net Worth vs Cumulative Cash Investment")
        fig = self.create_net_worth_comparison_chart(btl_analysis, btr_analysis, ri_analysis)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_roi_chart(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any]
    ):
        """Render the ROI comparison chart."""
        st.subheader("📈 Return on Investment (ROI) Comparison")
        fig = self.create_roi_comparison_chart(btl_analysis, btr_analysis, ri_analysis)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_all_charts(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any]
    ):
        """Render all comparison charts."""
        st.header("📊 Comparative Analysis")
        self.render_net_worth_chart(btl_analysis, btr_analysis, ri_analysis)
        self.render_roi_chart(btl_analysis, btr_analysis, ri_analysis) 