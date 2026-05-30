"""
Australian tax calculations including income tax, Medicare levy, and capital gains tax.
"""

from typing import Dict, Any
from ...config.australian_config import (
    TAX_BRACKETS, MEDICARE_LEVY_RATE, MEDICARE_LEVY_THRESHOLD,
    CGT_DISCOUNT_RATE, CGT_MIN_HOLDING_PERIOD_MONTHS, CGT_REFORM_MIN_TAX_RATE
)


class AustralianTaxCalculator:
    """
    Calculator for Australian tax obligations including income tax, Medicare levy,
    capital gains tax, and negative gearing benefits.
    """
    
    def calculate_income_tax(self, taxable_income: float, year: int = 2024) -> float:
        """
        Calculate Australian income tax based on current tax brackets.
        
        Args:
            taxable_income: Annual taxable income in AUD
            year: Tax year (for future tax bracket updates)
        
        Returns:
            Annual income tax amount
        """
        if taxable_income <= 0:
            return 0
            
        # Calculate tax using brackets
        tax = 0
        for bracket in TAX_BRACKETS:
            if taxable_income <= bracket["min"]:
                break
                
            taxable_in_bracket = min(taxable_income, bracket["max"]) - bracket["min"] + 1
            if taxable_in_bracket > 0:
                tax = bracket["base"] + (taxable_in_bracket * bracket["rate"])
        
        # Add Medicare levy
        medicare_levy = self.calculate_medicare_levy(taxable_income)
        
        return max(0, tax + medicare_levy)
    
    def calculate_medicare_levy(self, taxable_income: float) -> float:
        """Calculate Medicare levy (2% for incomes over threshold)"""
        if taxable_income > MEDICARE_LEVY_THRESHOLD:
            return taxable_income * MEDICARE_LEVY_RATE
        return 0
    
    def calculate_marginal_tax_rate(self, taxable_income: float, year: int = 2024) -> float:
        """
        Calculate the marginal tax rate (including Medicare levy) for a given income.
        
        Args:
            taxable_income: Annual taxable income in AUD
            year: Tax year
        
        Returns:
            Marginal tax rate as decimal (e.g., 0.345 for 34.5%)
        """
        # Medicare levy applies to all brackets above threshold
        medicare_rate = MEDICARE_LEVY_RATE if taxable_income > MEDICARE_LEVY_THRESHOLD else 0
        
        # Find applicable tax bracket
        for bracket in TAX_BRACKETS:
            if bracket["min"] <= taxable_income <= bracket["max"]:
                return bracket["rate"] + medicare_rate
                
        # Default to highest bracket
        return TAX_BRACKETS[-1]["rate"] + medicare_rate
    
    def calculate_capital_gains_tax(
        self,
        capital_gain: float,
        marginal_tax_rate: float,
        held_over_12_months: bool = True,
        is_new_build: bool = False,
        apply_2026_reform: bool = True
    ) -> float:
        """
        Calculate Australian capital gains tax.

        Args:
            capital_gain: Amount of capital gain
            marginal_tax_rate: Investor's marginal tax rate (as decimal)
            held_over_12_months: Whether asset was held for more than 12 months
            is_new_build: Whether the property is a new build
            apply_2026_reform: Apply 2026-27 Budget reform rules (purchases after 12 May 2026)

        Returns:
            Capital gains tax amount
        """
        if capital_gain <= 0:
            return 0

        if apply_2026_reform:
            if is_new_build:
                # New builds: investor chooses whichever arrangement results in less tax
                old_rule_cgt = capital_gain * CGT_DISCOUNT_RATE * marginal_tax_rate
                new_rule_cgt = capital_gain * max(marginal_tax_rate, CGT_REFORM_MIN_TAX_RATE)
                return min(old_rule_cgt, new_rule_cgt)
            else:
                # Non-new-build purchased after 12 May 2026: no 50% discount, minimum 30% tax
                effective_rate = max(marginal_tax_rate, CGT_REFORM_MIN_TAX_RATE)
                return capital_gain * effective_rate

        # Legacy rules: 50% discount for assets held over 12 months
        if held_over_12_months:
            taxable_gain = capital_gain * CGT_DISCOUNT_RATE
        else:
            taxable_gain = capital_gain

        return taxable_gain * marginal_tax_rate
    
    def calculate_negative_gearing_benefit(
        self,
        deductible_expenses: float,
        rental_income: float,
        marginal_tax_rate: float,
        is_new_build: bool = False,
        apply_2026_reform: bool = True
    ) -> float:
        """
        Calculate negative gearing tax benefit.

        Args:
            deductible_expenses: Total tax-deductible expenses (interest + property costs)
            rental_income: Annual rental income received
            marginal_tax_rate: Investor's marginal tax rate
            is_new_build: Whether the property is a new build
            apply_2026_reform: Apply 2026-27 Budget reform rules (purchases after 12 May 2026)

        Returns:
            Tax savings from negative gearing (0 if property is positively geared or losses quarantined)
        """
        # 2026-27 reform: losses on non-new-build investment properties bought after 12 May 2026
        # are quarantined — they can only offset other residential property income, not general income
        if apply_2026_reform and not is_new_build:
            return 0.0

        property_loss = max(0, deductible_expenses - rental_income)
        return property_loss * marginal_tax_rate
    
    def get_tax_summary(self, taxable_income: float) -> Dict[str, Any]:
        """
        Get a comprehensive tax summary for a given income.
        
        Returns:
            Dictionary with tax breakdown including rates and amounts
        """
        income_tax = self.calculate_income_tax(taxable_income)
        medicare_levy = self.calculate_medicare_levy(taxable_income)
        marginal_rate = self.calculate_marginal_tax_rate(taxable_income)
        
        return {
            "taxable_income": taxable_income,
            "income_tax": income_tax,
            "medicare_levy": medicare_levy,
            "total_tax": income_tax,  # Income tax already includes Medicare levy
            "marginal_rate": marginal_rate,
            "average_rate": income_tax / taxable_income if taxable_income > 0 else 0,
            "after_tax_income": taxable_income - income_tax
        } 