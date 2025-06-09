"""
Main scenario calculator orchestrating property and investment scenarios.
"""

from typing import Dict, Any, Tuple, List
from ..property.stamp_duty import StampDutyCalculator
from ..property.mortgage import MortgageCalculator
from ..investment.stock_calculator import StockInvestmentCalculator
from ..tax.australian_tax import AustralianTaxCalculator
from ...config.australian_config import WEEKS_PER_YEAR, MONTHS_PER_YEAR


class ScenarioCalculator:
    """
    Main calculator for comparing Buy to Live, Buy to Rent, and Rent & Invest scenarios.
    """
    
    def __init__(self):
        self.stamp_duty_calc = StampDutyCalculator()
        self.mortgage_calc = MortgageCalculator()
        self.stock_calc = StockInvestmentCalculator()
        self.tax_calc = AustralianTaxCalculator()
    
    def calculate_buy_to_live_scenario(
        self,
        property_price: float,
        deposit_percent: float,
        interest_rate: float,
        loan_term: int,
        annual_property_growth_rate: float,
        annual_property_expenses_percent: float = 0.01,
        upfront_costs: float = 3000,
        is_first_home_buyer: bool = False,
        analysis_years: int = 30
    ) -> Dict[str, Any]:
        """Calculate the Buy to Live scenario with detailed year-by-year analysis."""
        
        # Basic calculations
        deposit = property_price * deposit_percent
        stamp_duty = self.stamp_duty_calc.calculate_stamp_duty(property_price, is_first_home_buyer)
        total_upfront = deposit + stamp_duty + upfront_costs
        loan_amount = property_price - deposit
        
        # Monthly payment
        monthly_payment = self.mortgage_calc.calculate_monthly_payment(loan_amount, interest_rate, loan_term)
        
        # Year-by-year analysis
        yearly_analysis = []
        cumulative_costs = total_upfront
        cumulative_income = 0
        
        for year in range(1, analysis_years + 1):
            property_value = property_price * ((1 + annual_property_growth_rate) ** year)
            remaining_balance = self.mortgage_calc.calculate_remaining_balance(loan_amount, interest_rate, loan_term, year)
            annual_property_expenses = property_value * annual_property_expenses_percent
            # Calculate realistic annual mortgage payment
            if year <= loan_term:
                annual_mortgage_payment = monthly_payment * 12
            else:
                annual_mortgage_payment = 0
            
            # Annual housing cost (mortgage + property expenses)
            annual_housing_cost = annual_mortgage_payment + annual_property_expenses
            
            # Cumulative calculations
            cumulative_costs += annual_housing_cost
            net_cash_invested = cumulative_costs - cumulative_income
            
            # Net worth and ROI
            net_worth = property_value - remaining_balance
            roi_percent = ((net_worth - net_cash_invested) / net_cash_invested) * 100 if net_cash_invested > 0 else 0
            
            yearly_analysis.append({
                'year': year,
                'property_value': property_value,
                'remaining_balance': remaining_balance,
                'net_worth': net_worth,
                'cumulative_costs': cumulative_costs,
                'cumulative_income': cumulative_income,
                'net_cash_invested': net_cash_invested,
                'annual_housing_cost': annual_housing_cost,
                'annual_property_expenses': annual_property_expenses,
                'annual_mortgage_payment': annual_mortgage_payment,
                'roi_percent': roi_percent
            })
        
        return {
            'scenario': 'Buy to Live',
            'property_price': property_price,
            'deposit': deposit,
            'stamp_duty': stamp_duty,
            'total_upfront_cost': total_upfront,
            'total_upfront_costs': total_upfront,  # For compatibility
            'initial_deposit': deposit,  # For compatibility
            'upfront_costs': upfront_costs,  # For compatibility
            'loan_amount': loan_amount,
            'monthly_payment': monthly_payment,
            'yearly_analysis': yearly_analysis,
            'final_net_worth': yearly_analysis[-1]['net_worth'] if yearly_analysis else 0
        }
    
    def calculate_buy_to_rent_scenario(
        self,
        investment_property_price: float,
        deposit_percent: float,
        interest_rate: float,
        loan_term: int,
        weekly_rental_income: float,
        your_weekly_rent: float,
        annual_property_growth_rate: float,
        annual_rental_inflation_rate: float,
        annual_property_expenses_percent: float = 0.01,
        upfront_costs: float = 3000,
        is_first_home_buyer: bool = False,
        analysis_years: int = 30,
        annual_gross_income: float = 100000,
        salary_growth_rate: float = 0.03
    ) -> Dict[str, Any]:
        """Calculate the Buy to Rent scenario with negative gearing benefits."""
        
        # Basic calculations
        deposit = investment_property_price * deposit_percent
        stamp_duty = self.stamp_duty_calc.calculate_stamp_duty(investment_property_price, is_first_home_buyer)
        total_upfront = deposit + stamp_duty + upfront_costs
        loan_amount = investment_property_price - deposit
        
        # Monthly payments and income
        monthly_mortgage_payment = self.mortgage_calc.calculate_monthly_payment(loan_amount, interest_rate, loan_term)
        monthly_rental_income = weekly_rental_income * WEEKS_PER_YEAR / MONTHS_PER_YEAR
        your_monthly_rent = your_weekly_rent * WEEKS_PER_YEAR / MONTHS_PER_YEAR
        
        # Year-by-year analysis with negative gearing
        yearly_analysis = []
        cumulative_negative_gearing = 0
        cumulative_costs = total_upfront
        cumulative_income = 0
        
        for year in range(1, analysis_years + 1):
            # Property and income growth
            property_value = investment_property_price * ((1 + annual_property_growth_rate) ** year)
            annual_rental_income = (weekly_rental_income * WEEKS_PER_YEAR) * ((1 + annual_rental_inflation_rate) ** year)
            your_annual_rent = (your_weekly_rent * WEEKS_PER_YEAR) * ((1 + annual_rental_inflation_rate) ** year)
            current_income = annual_gross_income * ((1 + salary_growth_rate) ** year)
            
            # Mortgage details
            remaining_balance = self.mortgage_calc.calculate_remaining_balance(loan_amount, interest_rate, loan_term, year)
            annual_mortgage_interest = self.mortgage_calc.calculate_annual_mortgage_interest(loan_amount, interest_rate, loan_term, year)
            # Calculate realistic annual mortgage payment
            if year <= loan_term:
                annual_mortgage_payment = monthly_mortgage_payment * 12
            else:
                annual_mortgage_payment = 0
            
            # Property expenses
            annual_property_expenses = property_value * annual_property_expenses_percent
            
            # Tax calculations
            marginal_tax_rate = self.tax_calc.calculate_marginal_tax_rate(current_income)
            
            # Negative gearing calculation
            deductible_expenses = annual_mortgage_interest + annual_property_expenses
            property_loss = max(0, deductible_expenses - annual_rental_income)
            negative_gearing_benefit = self.tax_calc.calculate_negative_gearing_benefit(
                deductible_expenses, annual_rental_income, marginal_tax_rate
            )
            cumulative_negative_gearing += negative_gearing_benefit
            
            # Cash flows and costs
            annual_costs = annual_mortgage_payment + annual_property_expenses + your_annual_rent
            annual_income = annual_rental_income + negative_gearing_benefit
            
            cumulative_costs += annual_costs
            cumulative_income += annual_income
            net_cash_invested = cumulative_costs - cumulative_income
            
            # Total housing cost (what you pay out of pocket)
            annual_total_housing_cost = annual_costs - annual_income
            annual_net_cash_flow = annual_income - annual_costs
            
            # Net worth calculation
            net_worth = property_value - remaining_balance + cumulative_negative_gearing
            roi_percent = ((net_worth - net_cash_invested) / net_cash_invested) * 100 if net_cash_invested > 0 else 0
            
            yearly_analysis.append({
                'year': year,
                'property_value': property_value,
                'remaining_balance': remaining_balance,
                'net_worth': net_worth,
                'cumulative_costs': cumulative_costs,
                'cumulative_income': cumulative_income,
                'net_cash_invested': net_cash_invested,
                'annual_net_cash_flow': annual_net_cash_flow,
                'annual_total_housing_cost': annual_total_housing_cost,
                'annual_rental_income': annual_rental_income,
                'annual_mortgage_payments': annual_mortgage_payment,
                'annual_mortgage_interest': annual_mortgage_interest,
                'annual_property_expenses': annual_property_expenses,
                'annual_your_rent': your_annual_rent,
                'annual_deductible_expenses': deductible_expenses,
                'property_loss': property_loss,
                'annual_negative_gearing_benefit': negative_gearing_benefit,
                'cumulative_negative_gearing_benefits': cumulative_negative_gearing,
                'marginal_tax_rate': marginal_tax_rate,
                'roi_percent': roi_percent,
                'rental_income_monthly': annual_rental_income / 12
            })
        
        return {
            'scenario': 'Buy to Rent',
            'investment_property_price': investment_property_price,
            'deposit': deposit,
            'stamp_duty': stamp_duty,
            'total_upfront_cost': total_upfront,
            'total_upfront_costs': total_upfront,  # For compatibility
            'initial_deposit': deposit,  # For compatibility
            'upfront_costs': upfront_costs,  # For compatibility
            'loan_amount': loan_amount,
            'monthly_mortgage_payment': monthly_mortgage_payment,
            'initial_monthly_rental_income': monthly_rental_income,
            'your_initial_monthly_rent': your_monthly_rent,
            'yearly_analysis': yearly_analysis,
            'final_net_worth': yearly_analysis[-1]['net_worth'] if yearly_analysis else 0,
            'total_negative_gearing_benefits': cumulative_negative_gearing
        }
    
    def calculate_rent_and_invest_scenario(
        self,
        equivalent_property_price: float,
        deposit_percent: float,
        your_weekly_rent: float,
        annual_stock_return_rate: float,
        annual_rental_inflation_rate: float,
        upfront_costs: float = 3000,
        is_first_home_buyer: bool = False,
        analysis_years: int = 30,
        btl_housing_costs: List[float] = None
    ) -> Dict[str, Any]:
        """Calculate the Rent and Invest scenario."""
        
        # Investment amount equals what would have been spent on property
        investment_deposit = equivalent_property_price * deposit_percent
        stamp_duty_saved = self.stamp_duty_calc.calculate_stamp_duty(equivalent_property_price, is_first_home_buyer)
        total_initial_investment = investment_deposit + stamp_duty_saved + upfront_costs
        
        # Initial rent
        your_monthly_rent = your_weekly_rent * WEEKS_PER_YEAR / MONTHS_PER_YEAR
        
        # Year-by-year analysis
        yearly_analysis = []
        stock_portfolio_value = total_initial_investment
        cumulative_rent_paid = 0
        cumulative_net_stock_investments = total_initial_investment
        
        for year in range(1, analysis_years + 1):
            # Rent growth
            annual_rent_cost = (your_weekly_rent * WEEKS_PER_YEAR) * ((1 + annual_rental_inflation_rate) ** year)
            cumulative_rent_paid += annual_rent_cost
            
            # Calculate additional investment (difference between BTL housing cost and RI rent)
            if btl_housing_costs and year <= len(btl_housing_costs):
                btl_annual_cost = btl_housing_costs[year - 1]  # year-1 because list is 0-indexed
                annual_additional_investment = max(0, btl_annual_cost - annual_rent_cost)
            else:
                # Fallback: estimate additional investment as reasonable amount
                annual_additional_investment = 0
            
            # Investment growth (compound existing portfolio)
            annual_stock_returns = stock_portfolio_value * annual_stock_return_rate
            stock_portfolio_value += annual_stock_returns
            
            # Add additional investment to portfolio
            stock_portfolio_value += annual_additional_investment
            cumulative_net_stock_investments += annual_additional_investment
            
            # Calculate what would be equivalent property costs for comparison
            annual_property_costs_total = annual_rent_cost + annual_additional_investment
            
            # Annual net investment now includes the additional amount
            annual_net_investment = annual_additional_investment
            
            # Net cash invested = rent paid + all investments (initial + ongoing)
            net_cash_invested = cumulative_net_stock_investments + cumulative_rent_paid
            
            # Net worth = stock portfolio value (no debt)
            net_worth = stock_portfolio_value
            roi_percent = ((net_worth - net_cash_invested) / net_cash_invested) * 100 if net_cash_invested > 0 else 0
            
            yearly_analysis.append({
                'year': year,
                'stock_portfolio_value': stock_portfolio_value,
                'net_worth': net_worth,
                'cumulative_rent_paid': cumulative_rent_paid,
                'cumulative_net_stock_investments': cumulative_net_stock_investments,
                'net_cash_invested': net_cash_invested,
                'annual_rent_cost': annual_rent_cost,
                'annual_stock_returns': annual_stock_returns,
                'annual_net_investment': annual_net_investment,
                'annual_property_costs_total': annual_property_costs_total,
                'roi_percent': roi_percent
            })
        
        return {
            'scenario': 'Rent and Invest',
            'equivalent_property_price': equivalent_property_price,
            'initial_investment': total_initial_investment,
            'investment_deposit_equivalent': investment_deposit,
            'deposit_equivalent': investment_deposit,  # For compatibility
            'stamp_duty_saved': stamp_duty_saved,
            'stamp_duty_equivalent': stamp_duty_saved,  # For compatibility
            'upfront_costs_equivalent': upfront_costs,  # For compatibility
            'your_initial_monthly_rent': your_monthly_rent,
            'yearly_analysis': yearly_analysis,
            'final_net_worth': yearly_analysis[-1]['net_worth'] if yearly_analysis else 0,
            'final_investment_value': stock_portfolio_value
        }
    
    def apply_capital_gains_tax(
        self,
        btl_analysis: Dict[str, Any],
        btr_analysis: Dict[str, Any],
        ri_analysis: Dict[str, Any],
        annual_gross_income: float,
        salary_growth_rate: float
    ) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        """Apply capital gains tax to scenarios (BTL is exempt as main residence)."""
        
        # BTL is exempt from CGT as main residence - just add required fields
        btl_after_tax = btl_analysis.copy()
        btl_yearly = btl_after_tax['yearly_analysis'].copy()
        
        for i, year_data in enumerate(btl_yearly):
            btl_yearly[i] = year_data.copy()
            btl_yearly[i]['cgt_liability'] = 0  # No CGT for main residence
            btl_yearly[i]['net_worth_after_tax'] = year_data['net_worth']  # Same as net worth
        
        btl_after_tax['yearly_analysis'] = btl_yearly
        
        # Calculate CGT for BTR
        btr_after_tax = btr_analysis.copy()
        btr_yearly = btr_after_tax['yearly_analysis'].copy()
        final_year = len(btr_analysis['yearly_analysis'])
        final_income = annual_gross_income * ((1 + salary_growth_rate) ** final_year)
        marginal_rate = self.tax_calc.calculate_marginal_tax_rate(final_income)
        
        # BTR capital gains
        initial_price = btr_analysis['investment_property_price']
        
        for i, year_data in enumerate(btr_yearly):
            current_property_value = year_data['property_value']
            capital_gain = current_property_value - initial_price
            cgt_liability = self.tax_calc.calculate_capital_gains_tax(capital_gain, marginal_rate, True)
            net_worth_after_tax = year_data['net_worth'] - cgt_liability
            
            btr_yearly[i] = year_data.copy()
            btr_yearly[i]['cgt_liability'] = cgt_liability
            btr_yearly[i]['net_worth_after_tax'] = net_worth_after_tax
        
        btr_after_tax['yearly_analysis'] = btr_yearly
        btr_after_tax['capital_gains_tax'] = btr_yearly[-1]['cgt_liability']
        btr_after_tax['final_net_worth_after_cgt'] = btr_yearly[-1]['net_worth_after_tax']
        
        # Calculate CGT for RI
        ri_after_tax = ri_analysis.copy()
        ri_yearly = ri_after_tax['yearly_analysis'].copy()
        initial_investment = ri_analysis['initial_investment']
        
        for i, year_data in enumerate(ri_yearly):
            current_portfolio_value = year_data['stock_portfolio_value']
            capital_gain = current_portfolio_value - initial_investment
            cgt_liability = self.tax_calc.calculate_capital_gains_tax(capital_gain, marginal_rate, True)
            net_worth_after_tax = year_data['net_worth'] - cgt_liability
            
            ri_yearly[i] = year_data.copy()
            ri_yearly[i]['cgt_liability'] = cgt_liability
            ri_yearly[i]['net_worth_after_tax'] = net_worth_after_tax
        
        ri_after_tax['yearly_analysis'] = ri_yearly
        ri_after_tax['capital_gains_tax'] = ri_yearly[-1]['cgt_liability']
        ri_after_tax['final_net_worth_after_cgt'] = ri_yearly[-1]['net_worth_after_tax']
        
        return btl_after_tax, btr_after_tax, ri_after_tax 