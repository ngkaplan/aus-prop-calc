"""
Australian Property Investment Calculator - Restructured Application
Uses domain-driven design with modular components.
"""

import streamlit as st

from src.domain.scenarios.scenario_calculator import ScenarioCalculator
from src.domain.property.affordability import AffordabilityCalculator
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
    """Render Stage 1 scaffold for serviceability-based portfolio growth."""
    st.header("🏗️ Portfolio Growth (Serviceability)")
    st.markdown(
        "Configure lending and acquisition assumptions for the multi-purchase strategy. "
        "Simulation logic lands in Stage 2+."
    )

    portfolio_params = input_manager.render_portfolio_growth_inputs()

    st.subheader("🧭 Stage 1 Preview")
    st.info(
        "This tab is scaffolding only in Stage 1. "
        "Next stage will compute borrowing capacity and purchase timing."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Configured Rules**")
        st.write(f"• Assessment Buffer: {portfolio_params['assessment_buffer_rate']*100:.2f}%")
        st.write(f"• Assessment Floor: {portfolio_params['assessment_rate_floor']*100:.2f}%")
        st.write(f"• Rental Income Haircut: {portfolio_params['rental_income_haircut']*100:.0f}%")
        st.write(f"• Expense Floor: ${portfolio_params['bank_expense_floor_monthly']:,.0f}/month")
        st.write(f"• Cash Buffer: {portfolio_params['cash_buffer_months']} months")
        st.write(f"• Review Frequency: {portfolio_params['review_frequency']}")

    with col2:
        st.markdown("**Configured Acquisition Profile**")
        st.write(
            f"• Base Investment Price: ${portfolio_params['base_investment_purchase_price']:,.0f}"
        )
        st.write(
            f"• Gross Rental Yield: "
            f"{portfolio_params['new_purchase_gross_rental_yield']*100:.2f}%"
        )
        st.write(
            f"• Purchase Price Growth: "
            f"{portfolio_params['new_purchase_price_growth_rate']*100:.2f}% p.a."
        )


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
