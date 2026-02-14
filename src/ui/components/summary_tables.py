"""
Summary tables and comparison components for displaying scenario results.
"""

from io import BytesIO
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import streamlit as st
from typing import Dict, Any
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
        annual_gross_income: float,
        analysis_years: int,
    ):
        """Render the final-year summary comparison metrics."""
        st.subheader(f"📈 {analysis_years}-Year Summary Comparison")

        # Show current marginal tax rate
        current_marginal_rate = self.tax_calc.calculate_marginal_tax_rate(annual_gross_income)
        st.info(f"💡 **Current Marginal Tax Rate:** {current_marginal_rate*100:.1f}% (includes Medicare levy)")

        col1, col2, col3 = st.columns(3)

        btl_final = btl_analysis["yearly_analysis"][-1]
        btr_final = btr_analysis["yearly_analysis"][-1]
        ri_final = ri_analysis["yearly_analysis"][-1]

        with col1:
            self._render_btl_summary(btl_analysis, btl_final)

        with col2:
            self._render_btr_summary(btr_analysis, btr_final)

        with col3:
            self._render_ri_summary(ri_analysis, ri_final)

    def _render_btl_summary(self, btl_analysis: Dict[str, Any], btl_final: Dict[str, Any]):
        """Render Buy to Live summary card."""
        st.metric("🏡 Buy to Live", format_currency(btl_final["net_worth"]), f"ROI: {btl_final['roi_percent']:.1f}%")
        st.metric("Initial Investment", format_currency(btl_analysis["total_upfront_costs"]))
        st.metric("Total Cash Invested", format_currency(btl_final["net_cash_invested"]))
        st.success("✅ **CGT Exempt** (main residence)")
        st.caption(
            f"Includes: Deposit {format_currency(btl_analysis['initial_deposit'])}, "
            f"Stamp Duty {format_currency(btl_analysis['stamp_duty'])}, "
            f"Legal {format_currency(btl_analysis['upfront_costs'])}"
        )

    def _render_btr_summary(self, btr_analysis: Dict[str, Any], btr_final: Dict[str, Any]):
        """Render Buy to Rent summary card."""
        net_worth_before_tax = btr_final["net_worth"]
        net_worth_after_tax = btr_final["net_worth_after_tax"]
        cgt_liability = btr_final["cgt_liability"]
        negative_gearing_benefits = btr_final["cumulative_negative_gearing_benefits"]

        roi_after_tax = (
            (net_worth_after_tax - btr_final["net_cash_invested"]) / btr_final["net_cash_invested"] * 100
            if btr_final["net_cash_invested"] > 0
            else 0
        )

        st.metric("🏠 Buy to Rent (After Tax)", format_currency(net_worth_after_tax), f"ROI: {roi_after_tax:.1f}%")
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
        portfolio_before_tax = ri_final["stock_portfolio_value"]
        portfolio_after_tax = ri_final["net_worth_after_tax"]
        cgt_liability = ri_final["cgt_liability"]

        roi_after_tax = (
            (portfolio_after_tax - ri_final["net_cash_invested"]) / ri_final["net_cash_invested"] * 100
            if ri_final["net_cash_invested"] > 0
            else 0
        )

        st.metric("📈 Rent & Invest (After Tax)", format_currency(portfolio_after_tax), f"ROI: {roi_after_tax:.1f}%")
        st.metric("Before Tax", format_currency(portfolio_before_tax))
        st.metric("CGT Liability", format_currency(cgt_liability))
        st.warning(f"⚠️ **CGT Impact:** -{format_currency(cgt_liability)}")
        st.caption(
            f"Includes: Deposit Equiv {format_currency(ri_analysis['deposit_equivalent'])}, "
            f"Stamp Duty Equiv {format_currency(ri_analysis['stamp_duty_equivalent'])}, "
            f"Legal {format_currency(ri_analysis['upfront_costs_equivalent'])}"
        )

    def build_milestone_dataframe(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any],
    ) -> pd.DataFrame:
        """Build milestone comparison data."""
        btl_df = pd.DataFrame(btl_analysis["yearly_analysis"])
        btr_df = pd.DataFrame(btr_analysis["yearly_analysis"])
        ri_df = pd.DataFrame(ri_analysis["yearly_analysis"])

        max_years = min(len(btl_df), len(btr_df), len(ri_df))
        milestones = [year for year in [5, 10, 15, 20, 30] if year <= max_years]

        if max_years not in milestones:
            milestones.append(max_years)

        comparison_data = []
        for year in sorted(set(milestones)):
            btl_data = btl_df.iloc[year - 1]
            btr_data = btr_df.iloc[year - 1]
            ri_data = ri_df.iloc[year - 1]

            comparison_data.append(
                {
                    "Year": year,
                    "Buy to Live Net Worth": btl_data["net_worth"],
                    "Buy to Live ROI (%)": btl_data["roi_percent"],
                    "Buy to Rent Net Worth (After Tax)": btr_data["net_worth_after_tax"],
                    "Buy to Rent ROI (%)": btr_data["roi_percent"],
                    "Rent & Invest Net Worth (After Tax)": ri_data["net_worth_after_tax"],
                    "Rent & Invest ROI (%)": ri_data["roi_percent"],
                }
            )

        return pd.DataFrame(comparison_data)

    def render_milestone_comparison(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any],
    ):
        """Render the milestone comparison table."""
        st.subheader("📊 Key Milestone Comparison")
        milestone_df = self.build_milestone_dataframe(btl_analysis, btr_analysis, ri_analysis)
        formatted_df = milestone_df.copy()

        for col in [
            "Buy to Live Net Worth",
            "Buy to Rent Net Worth (After Tax)",
            "Rent & Invest Net Worth (After Tax)",
        ]:
            formatted_df[col] = formatted_df[col].apply(format_currency)

        for col in ["Buy to Live ROI (%)", "Buy to Rent ROI (%)", "Rent & Invest ROI (%)"]:
            formatted_df[col] = formatted_df[col].map(lambda v: f"{v:.1f}%")

        st.table(formatted_df)

    def build_cash_flow_dataframe(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any],
    ) -> pd.DataFrame:
        """Build annual cash flow and net worth data for export and display."""
        btl_df = pd.DataFrame(btl_analysis["yearly_analysis"])
        btr_df = pd.DataFrame(btr_analysis["yearly_analysis"])
        ri_df = pd.DataFrame(ri_analysis["yearly_analysis"])

        max_years = min(len(btl_df), len(btr_df), len(ri_df))
        cash_flow_data = [
            {
                "Year": 0,
                "Buy to Live Cash Flow": -btl_analysis["total_upfront_costs"],
                "Buy to Live Net Worth": 0,
                "Buy to Rent Cash Flow": -btr_analysis["total_upfront_costs"],
                "Buy to Rent Net Worth": 0,
                "Rent & Invest Cash Flow": -ri_analysis["initial_investment"],
                "Rent & Invest Net Worth": 0,
            }
        ]

        for year in range(1, max_years + 1):
            btl_row = btl_df.iloc[year - 1]
            btr_row = btr_df.iloc[year - 1]
            ri_row = ri_df.iloc[year - 1]

            btl_net_flow = -btl_row["annual_housing_cost"]
            btr_net_flow = (
                btr_row["annual_rental_income"]
                - btr_row["annual_mortgage_payments"]
                - btr_row["annual_property_expenses"]
                - btr_row["annual_your_rent"]
                + btr_row["annual_negative_gearing_benefit"]
            )

            btl_equivalent_cost = btl_row["annual_housing_cost"]
            ri_actual_rent = ri_row["annual_rent_cost"]
            ri_should_invest = btl_equivalent_cost - ri_actual_rent
            ri_net_flow = -ri_actual_rent - ri_should_invest

            cash_flow_data.append(
                {
                    "Year": year,
                    "Buy to Live Cash Flow": btl_net_flow,
                    "Buy to Live Net Worth": btl_row["net_worth"],
                    "Buy to Rent Cash Flow": btr_net_flow,
                    "Buy to Rent Net Worth": btr_row["net_worth_after_tax"],
                    "Rent & Invest Cash Flow": ri_net_flow,
                    "Rent & Invest Net Worth": ri_row["net_worth_after_tax"],
                }
            )

        return pd.DataFrame(cash_flow_data)

    def render_cash_flow_table(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any],
    ):
        """Render the annual cash flows and net worth table."""
        st.subheader("💰 Annual Net Cash Flows & Net Worth by Year")
        cash_flow_df = self.build_cash_flow_dataframe(btl_analysis, btr_analysis, ri_analysis)

        st.write(f"Displaying {len(cash_flow_df) - 1} years of data")

        display_df = cash_flow_df.copy()
        money_columns = [col for col in display_df.columns if col != "Year"]
        for col in money_columns:
            display_df[col] = display_df[col].apply(format_currency)

        st.dataframe(display_df, height=400, use_container_width=True)

        st.caption(
            "*Cash Flow: Negative = outflows (expenses), Positive = net inflows. "
            "Net Worth: Total wealth accumulated (after capital gains tax for Buy to Rent and Rent & Invest). "
            "Year 0 shows initial upfront costs and zero net worth.*"
        )

    def build_final_summary_dataframe(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any],
    ) -> pd.DataFrame:
        """Build final scenario summary table for export."""
        btl_final = btl_analysis["yearly_analysis"][-1]
        btr_final = btr_analysis["yearly_analysis"][-1]
        ri_final = ri_analysis["yearly_analysis"][-1]

        return pd.DataFrame(
            [
                {
                    "Scenario": "Buy to Live",
                    "Final Net Worth (After Tax)": btl_final["net_worth_after_tax"],
                    "Final Cash Invested": btl_final["net_cash_invested"],
                    "Final ROI (%)": btl_final["roi_percent"],
                    "CGT Liability": btl_final["cgt_liability"],
                },
                {
                    "Scenario": "Buy to Rent",
                    "Final Net Worth (After Tax)": btr_final["net_worth_after_tax"],
                    "Final Cash Invested": btr_final["net_cash_invested"],
                    "Final ROI (%)": btr_final["roi_percent"],
                    "CGT Liability": btr_final["cgt_liability"],
                },
                {
                    "Scenario": "Rent & Invest",
                    "Final Net Worth (After Tax)": ri_final["net_worth_after_tax"],
                    "Final Cash Invested": ri_final["net_cash_invested"],
                    "Final ROI (%)": ri_final["roi_percent"],
                    "CGT Liability": ri_final["cgt_liability"],
                },
            ]
        )

    def _dataframe_to_sheet_xml(self, dataframe: pd.DataFrame) -> str:
        """Convert a dataframe to minimal XLSX worksheet XML."""
        rows = [list(dataframe.columns)]
        rows.extend(dataframe.fillna("").values.tolist())

        row_xml_parts = []
        for row_index, row_values in enumerate(rows, start=1):
            cells = []
            for col_index, value in enumerate(row_values, start=1):
                column_label = ""
                current = col_index
                while current > 0:
                    current, rem = divmod(current - 1, 26)
                    column_label = chr(65 + rem) + column_label
                cell_ref = f"{column_label}{row_index}"

                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    cells.append(f'<c r="{cell_ref}"><v>{value}</v></c>')
                else:
                    text_value = escape(str(value))
                    cells.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{text_value}</t></is></c>')

            row_xml_parts.append(f'<row r="{row_index}">{"".join(cells)}</row>')

        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<sheetData>'
            f'{"".join(row_xml_parts)}'
            '</sheetData>'
            '</worksheet>'
        )

    def _build_export_workbook(
        self,
        summary_df: pd.DataFrame,
        milestone_df: pd.DataFrame,
        cash_flow_df: pd.DataFrame,
    ) -> bytes:
        """Build XLSX workbook bytes for downloads without external writer dependencies."""
        output = BytesIO()
        with ZipFile(output, "w", compression=ZIP_DEFLATED) as zf:
            zf.writestr(
                "[Content_Types].xml",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                '<Default Extension="xml" ContentType="application/xml"/>'
                '<Override PartName="/xl/workbook.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                '<Override PartName="/xl/worksheets/sheet1.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                '<Override PartName="/xl/worksheets/sheet2.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                '<Override PartName="/xl/worksheets/sheet3.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                '</Types>',
            )
            zf.writestr(
                "_rels/.rels",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
                'Target="xl/workbook.xml"/>'
                '</Relationships>',
            )
            zf.writestr(
                "xl/workbook.xml",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                '<sheets>'
                '<sheet name="Final Summary" sheetId="1" r:id="rId1"/>'
                '<sheet name="Milestones" sheetId="2" r:id="rId2"/>'
                '<sheet name="Annual Cash Flow" sheetId="3" r:id="rId3"/>'
                '</sheets>'
                '</workbook>',
            )
            zf.writestr(
                "xl/_rels/workbook.xml.rels",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                'Target="worksheets/sheet1.xml"/>'
                '<Relationship Id="rId2" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                'Target="worksheets/sheet2.xml"/>'
                '<Relationship Id="rId3" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                'Target="worksheets/sheet3.xml"/>'
                '</Relationships>',
            )
            zf.writestr("xl/worksheets/sheet1.xml", self._dataframe_to_sheet_xml(summary_df))
            zf.writestr("xl/worksheets/sheet2.xml", self._dataframe_to_sheet_xml(milestone_df))
            zf.writestr("xl/worksheets/sheet3.xml", self._dataframe_to_sheet_xml(cash_flow_df))

        output.seek(0)
        return output.read()

    def render_export_section(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any],
    ):
        """Render CSV/XLSX download actions for scenario outputs."""
        st.subheader("📤 Export / Reporting")

        summary_df = self.build_final_summary_dataframe(btl_analysis, btr_analysis, ri_analysis)
        milestone_df = self.build_milestone_dataframe(btl_analysis, btr_analysis, ri_analysis)
        cash_flow_df = self.build_cash_flow_dataframe(btl_analysis, btr_analysis, ri_analysis)

        csv_data = cash_flow_df.to_csv(index=False)
        workbook_data = self._build_export_workbook(summary_df, milestone_df, cash_flow_df)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Download Annual Cash Flow (CSV)",
                data=csv_data,
                file_name="annual_cash_flow.csv",
                mime="text/csv",
            )

        with col2:
            st.download_button(
                label="⬇️ Download Full Report (XLSX)",
                data=workbook_data,
                file_name="scenario_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    def render_input_summary(self, params: Dict[str, Any]):
        """Render simplified assumptions summary."""
        st.subheader("📋 Key Assumptions")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Fixed Assumptions:**")
            st.write(f"• Property Expenses: {params['property_expenses_percent']*100:.1f}% p.a.")
            st.write(f"• Upfront Costs: {format_currency(params['upfront_costs'])}")
            st.write(f"• Analysis Period: {params['analysis_years']} years")

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
        params: Dict[str, Any],
    ):
        """Render all summary components."""
        self.render_summary_metrics(
            btl_analysis,
            btr_analysis,
            ri_analysis,
            params["annual_gross_income"],
            params["analysis_years"],
        )
        self.render_milestone_comparison(btl_analysis, btr_analysis, ri_analysis)
        self.render_input_summary(params)
        self.render_cash_flow_table(btl_analysis, btr_analysis, ri_analysis)
        self.render_export_section(btl_analysis, btr_analysis, ri_analysis)
