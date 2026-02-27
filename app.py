"""
Australian Property Investment Calculator - Restructured Application
Uses domain-driven design with modular components.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.domain.scenarios.scenario_calculator import ScenarioCalculator
from src.domain.property.affordability import AffordabilityCalculator
from src.domain.portfolio.serviceability import ServiceabilityCalculator
from src.ui.components.input_forms import InputFormManager
from src.ui.components.charts import ChartManager
from src.ui.components.summary_tables import SummaryTableManager
from src.config.defaults import DEFAULT_ANALYSIS_YEARS


def render_core_comparison_tab(
    scenario_calc: ScenarioCalculator,
    affordability_calc: AffordabilityCalculator,
    input_manager: InputFormManager,
    chart_manager: ChartManager,
    summary_manager: SummaryTableManager,
):
    """Render the existing comparison dashboard flow."""
    st.header("🔧 Investment Parameters")

    params = input_manager.render_all_inputs()

    use_affordability_switch = params.get("use_affordability_switch", False)
    btl_deposit_percent = params["deposit_percent"]
    btr_deposit_percent = params["deposit_percent"]
    ri_deposit_percent = params["deposit_percent"]
    btl_upfront_costs = params["upfront_costs"]
    btr_upfront_costs = params["upfront_costs"]

    if use_affordability_switch:
        cash_available = params["cash_available_today"]
        max_borrowing = params["max_bank_borrowing"]
        allowed_lvr = params["allowed_lvr"]
        include_lmi = params["include_lmi_above_80_lvr"]
        is_first_home_buyer = params["is_first_home_buyer"]

        # BTL LMI policy:
        # - First home buyer: no LMI up to 95% LVR.
        # - Non-FHB: LMI applies above 80% LVR.
        btl_effective_lvr = allowed_lvr
        btl_include_lmi = allowed_lvr > 0.80
        if is_first_home_buyer:
            if allowed_lvr > 0.95:
                btl_effective_lvr = 0.95
                st.warning(
                    "First-home-buyer Buy to Live affordability is capped at 95% LVR "
                    "under the no-LMI guarantee assumption."
                )
            btl_include_lmi = False

        btl_affordability = affordability_calc.solve_max_property_price(
            cash_available=cash_available,
            max_borrowing=max_borrowing,
            allowed_lvr=btl_effective_lvr,
            upfront_costs=params["upfront_costs"],
            is_first_home_buyer=is_first_home_buyer,
            include_lmi=btl_include_lmi,
        )

        btr_effective_lvr = allowed_lvr
        btr_lmi_enabled = include_lmi and allowed_lvr > 0.80
        if allowed_lvr > 0.80 and not include_lmi:
            btr_effective_lvr = 0.80
            st.warning(
                "Investment LVR above 80% requires LMI toggle. "
                "Capping Buy to Rent affordability sizing at 80% LVR."
            )

        btr_affordability = affordability_calc.solve_max_property_price(
            cash_available=cash_available,
            max_borrowing=max_borrowing,
            allowed_lvr=btr_effective_lvr,
            upfront_costs=params["upfront_costs"],
            is_first_home_buyer=False,
            include_lmi=btr_lmi_enabled,
        )

        if not btl_affordability["feasible"] or not btr_affordability["feasible"]:
            st.error("Affordability inputs are infeasible for at least one scenario.")
            if not btl_affordability["feasible"]:
                st.error(f"Buy to Live: {btl_affordability['reason']}")
            if not btr_affordability["feasible"]:
                st.error(f"Buy to Rent: {btr_affordability['reason']}")
            st.stop()

        params["btl_property_price"] = int(btl_affordability["property_price"])
        params["btr_property_price"] = int(btr_affordability["property_price"])
        params["ri_equivalent_property_price"] = params["btl_property_price"]
        params["btl_affordability"] = btl_affordability
        params["btr_affordability"] = btr_affordability
        btl_deposit_percent = 1 - (
            btl_affordability["loan_amount"] / btl_affordability["property_price"]
        )
        btr_deposit_percent = 1 - (
            btr_affordability["loan_amount"] / btr_affordability["property_price"]
        )
        ri_deposit_percent = btl_deposit_percent
        btr_upfront_costs = params["upfront_costs"] + btr_affordability["lmi_cost"]

        st.info(
            f"Affordability solved prices: Buy to Live {params['btl_property_price']:,} | "
            f"Buy to Rent {params['btr_property_price']:,}"
        )

    st.header("📊 Scenario Calculations")
    with st.spinner("Calculating scenarios..."):
        btl_analysis = scenario_calc.calculate_buy_to_live_scenario(
            property_price=params["btl_property_price"],
            deposit_percent=btl_deposit_percent,
            interest_rate=params["interest_rate"],
            loan_term=params["loan_term"],
            annual_property_growth_rate=params["property_growth_rate"],
            annual_property_expenses_percent=params["property_expenses_percent"],
            upfront_costs=btl_upfront_costs,
            is_first_home_buyer=params["is_first_home_buyer"],
            analysis_years=DEFAULT_ANALYSIS_YEARS,
        )

        btr_analysis = scenario_calc.calculate_buy_to_rent_scenario(
            investment_property_price=params["btr_property_price"],
            deposit_percent=btr_deposit_percent,
            interest_rate=params["interest_rate"],
            loan_term=params["loan_term"],
            weekly_rental_income=params["btr_weekly_rental"],
            your_weekly_rent=params["your_weekly_rent"],
            annual_property_growth_rate=params["property_growth_rate"],
            annual_rental_inflation_rate=params["rental_inflation_rate"],
            annual_property_expenses_percent=params["property_expenses_percent"],
            upfront_costs=btr_upfront_costs,
            is_first_home_buyer=params["is_first_home_buyer"],
            analysis_years=DEFAULT_ANALYSIS_YEARS,
            annual_gross_income=params["annual_gross_income"],
            salary_growth_rate=params["salary_growth_rate"],
        )

        btl_housing_costs = [
            year_data["annual_housing_cost"] for year_data in btl_analysis["yearly_analysis"]
        ]
        ri_analysis = scenario_calc.calculate_rent_and_invest_scenario(
            equivalent_property_price=params["ri_equivalent_property_price"],
            deposit_percent=ri_deposit_percent,
            your_weekly_rent=params["your_weekly_rent"],
            annual_stock_return_rate=params["stock_return_rate"],
            annual_rental_inflation_rate=params["rental_inflation_rate"],
            upfront_costs=params["upfront_costs"],
            is_first_home_buyer=params["is_first_home_buyer"],
            analysis_years=DEFAULT_ANALYSIS_YEARS,
            btl_housing_costs=btl_housing_costs,
        )

        btl_analysis, btr_analysis, ri_analysis = scenario_calc.apply_capital_gains_tax(
            btl_analysis=btl_analysis,
            btr_analysis=btr_analysis,
            ri_analysis=ri_analysis,
            annual_gross_income=params["annual_gross_income"],
            salary_growth_rate=params["salary_growth_rate"],
        )

    st.success("✅ Calculations complete!")

    summary_manager.render_summary_metrics(
        btl_analysis=btl_analysis,
        btr_analysis=btr_analysis,
        ri_analysis=ri_analysis,
        annual_gross_income=params["annual_gross_income"],
    )

    chart_manager.render_all_charts(
        btl_analysis=btl_analysis,
        btr_analysis=btr_analysis,
        ri_analysis=ri_analysis,
    )

    summary_manager.render_milestone_comparison(btl_analysis, btr_analysis, ri_analysis)
    summary_manager.render_cash_flow_table(btl_analysis, btr_analysis, ri_analysis)
    summary_manager.render_input_summary(params)


def render_portfolio_growth_tab(input_manager: InputFormManager):
    """Render Stage 2 serviceability projection tab."""
    st.header("🏗️ Portfolio Growth (Serviceability)")
    st.markdown(
        "Configure lending and acquisition assumptions for the multi-purchase strategy. "
        "This stage projects serviceability-driven borrowing capacity over time."
    )

    portfolio_params = input_manager.render_portfolio_growth_inputs()
    serviceability_calc = ServiceabilityCalculator()

    projection = serviceability_calc.project_capacity(
        annual_gross_income=portfolio_params["annual_gross_income"],
        salary_growth_rate=portfolio_params["salary_growth_rate"],
        existing_weekly_rental_income=portfolio_params["existing_weekly_rental_income"],
        rental_income_growth_rate=portfolio_params["rental_income_growth_rate"],
        monthly_living_expenses=portfolio_params["monthly_living_expenses"],
        monthly_expense_growth_rate=portfolio_params["monthly_expense_growth_rate"],
        bank_expense_floor_monthly=portfolio_params["bank_expense_floor_monthly"],
        other_monthly_debt_commitments=portfolio_params["other_monthly_debt_commitments"],
        current_interest_rate=portfolio_params["current_interest_rate"],
        assessment_buffer_rate=portfolio_params["assessment_buffer_rate"],
        assessment_rate_floor=portfolio_params["assessment_rate_floor"],
        rental_income_haircut=portfolio_params["rental_income_haircut"],
        existing_home_loan_balance=portfolio_params["existing_home_loan_balance"],
        existing_home_loan_term_remaining=portfolio_params["existing_home_loan_term_remaining"],
        existing_investment_loan_balance=portfolio_params["existing_investment_loan_balance"],
        existing_investment_loan_term_remaining=portfolio_params["existing_investment_loan_term_remaining"],
        new_loan_term_years=portfolio_params["new_loan_term_years"],
        analysis_years=DEFAULT_ANALYSIS_YEARS,
    )
    projection_df = pd.DataFrame(projection["yearly_projection"])

    st.subheader("🧭 Stage 2 Serviceability Projection")
    st.success(
        f"Assessment rate used: {projection['assessment_rate']*100:.2f}% "
        f"(max of actual + buffer and floor)"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Year 1 Additional Borrowing Capacity",
            f"${projection_df.iloc[0]['additional_borrowing_capacity']:,.0f}",
        )
    with col2:
        st.metric(
            "Year 1 Monthly Serviceability Surplus",
            f"${projection_df.iloc[0]['monthly_surplus']:,.0f}",
        )
    with col3:
        st.metric(
            "Year 1 DTI (Existing Debt)",
            f"{projection_df.iloc[0]['dti_existing']:.2f}x",
        )

    st.subheader("📈 Borrowing Capacity Over Time")
    capacity_fig = go.Figure()
    capacity_fig.add_trace(
        go.Scatter(
            x=projection_df["year"],
            y=projection_df["additional_borrowing_capacity"],
            name="Additional Borrowing Capacity",
            line=dict(color="#1f77b4", width=3),
        )
    )
    capacity_fig.update_layout(
        height=400,
        hovermode="x unified",
        yaxis_title="Capacity ($)",
        xaxis_title="Year",
    )
    st.plotly_chart(capacity_fig, use_container_width=True)

    st.subheader("💸 Serviceability Surplus vs Commitments")
    surplus_fig = go.Figure()
    surplus_fig.add_trace(
        go.Scatter(
            x=projection_df["year"],
            y=projection_df["monthly_surplus"],
            name="Monthly Surplus",
            line=dict(color="#2ca02c", width=3),
        )
    )
    surplus_fig.add_trace(
        go.Scatter(
            x=projection_df["year"],
            y=projection_df["total_monthly_commitments"],
            name="Monthly Commitments",
            line=dict(color="#d62728", width=2, dash="dash"),
        )
    )
    surplus_fig.update_layout(
        height=400,
        hovermode="x unified",
        yaxis_title="Monthly Amount ($)",
        xaxis_title="Year",
    )
    st.plotly_chart(surplus_fig, use_container_width=True)

    st.subheader("🏦 Debt-to-Income (DTI) Projection")
    dti_fig = go.Figure()
    dti_fig.add_trace(
        go.Scatter(
            x=projection_df["year"],
            y=projection_df["dti_existing"],
            name="DTI (Existing Debt)",
            line=dict(color="#9467bd", width=3),
        )
    )
    dti_fig.add_trace(
        go.Scatter(
            x=projection_df["year"],
            y=projection_df["dti_with_capacity"],
            name="DTI (Including Capacity)",
            line=dict(color="#ff7f0e", width=2, dash="dash"),
        )
    )
    dti_fig.update_layout(
        height=400,
        hovermode="x unified",
        yaxis_title="DTI (x income)",
        xaxis_title="Year",
    )
    st.plotly_chart(dti_fig, use_container_width=True)

    st.subheader("📋 Year-by-Year Serviceability Table")
    table_df = projection_df[
        [
            "year",
            "assessed_income",
            "total_monthly_commitments",
            "monthly_surplus",
            "additional_borrowing_capacity",
            "existing_total_debt",
            "dti_existing",
            "dti_with_capacity",
        ]
    ].copy()
    table_df["assessed_income"] = table_df["assessed_income"].map(lambda v: f"${v:,.0f}")
    table_df["total_monthly_commitments"] = table_df["total_monthly_commitments"].map(
        lambda v: f"${v:,.0f}"
    )
    table_df["monthly_surplus"] = table_df["monthly_surplus"].map(lambda v: f"${v:,.0f}")
    table_df["additional_borrowing_capacity"] = table_df["additional_borrowing_capacity"].map(
        lambda v: f"${v:,.0f}"
    )
    table_df["existing_total_debt"] = table_df["existing_total_debt"].map(lambda v: f"${v:,.0f}")
    table_df["dti_existing"] = table_df["dti_existing"].map(lambda v: f"{v:.2f}x")
    table_df["dti_with_capacity"] = table_df["dti_with_capacity"].map(lambda v: f"{v:.2f}x")
    st.dataframe(table_df, height=420, use_container_width=True)


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Australian Property Investment Calculator",
        page_icon="🏠",
        layout="wide",
    )

    scenario_calc = ScenarioCalculator()
    affordability_calc = AffordabilityCalculator()
    input_manager = InputFormManager()
    chart_manager = ChartManager()
    summary_manager = SummaryTableManager()

    st.title("🏠 Australian Property Investment Comparison")
    st.markdown(
        "**Compare all three investment strategies side-by-side with comprehensive analysis**"
    )

    core_tab, portfolio_tab = st.tabs(
        ["Core Comparison", "Portfolio Growth (Serviceability)"]
    )

    with core_tab:
        render_core_comparison_tab(
            scenario_calc=scenario_calc,
            affordability_calc=affordability_calc,
            input_manager=input_manager,
            chart_manager=chart_manager,
            summary_manager=summary_manager,
        )

    with portfolio_tab:
        render_portfolio_growth_tab(input_manager=input_manager)

    st.markdown("---")
    st.markdown(
        "*Disclaimer: This calculator is for educational purposes only. "
        "Please consult with a qualified financial advisor for personalized investment advice.*"
    )


if __name__ == "__main__":
    main()
