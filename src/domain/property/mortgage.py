"""
Mortgage calculation utilities for property investment analysis.
"""

import math
from typing import Dict, Any


class MortgageCalculator:
    """Calculator for mortgage payments, balances, and interest calculations."""
    
    def calculate_monthly_payment(self, principal: float, annual_rate: float, years: int) -> float:
        """
        Calculate monthly mortgage payment using standard formula.
        
        Args:
            principal: Loan amount
            annual_rate: Annual interest rate as decimal (e.g., 0.06 for 6%)
            years: Loan term in years
        
        Returns:
            Monthly payment amount
        """
        if principal <= 0 or years <= 0:
            return 0
            
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        
        if annual_rate == 0:
            return principal / num_payments
        
        monthly_payment = principal * (
            monthly_rate * (1 + monthly_rate) ** num_payments
        ) / ((1 + monthly_rate) ** num_payments - 1)
        
        return monthly_payment
    
    def calculate_remaining_balance(self, principal: float, annual_rate: float, 
                                  years: int, years_paid: int) -> float:
        """
        Calculate remaining loan balance after a certain number of years.
        
        Args:
            principal: Original loan amount
            annual_rate: Annual interest rate as decimal
            years: Total loan term in years
            years_paid: Number of years already paid
        
        Returns:
            Remaining loan balance
        """
        if years_paid >= years or principal <= 0:
            return 0.0
        
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        payments_made = years_paid * 12
        
        if annual_rate == 0:
            return principal - (principal / num_payments * payments_made)
        
        monthly_payment = self.calculate_monthly_payment(principal, annual_rate, years)
        
        # Remaining balance formula
        remaining_balance = principal * (
            (1 + monthly_rate) ** num_payments - (1 + monthly_rate) ** payments_made
        ) / ((1 + monthly_rate) ** num_payments - 1)
        
        return max(0, remaining_balance)
    
    def calculate_annual_mortgage_interest(self, principal: float, annual_rate: float, 
                                         years: int, year: int) -> float:
        """
        Calculate the interest portion of mortgage payments for a specific year.
        This is important for negative gearing calculations as only interest is tax deductible.
        
        Args:
            principal: Original loan amount
            annual_rate: Annual interest rate as decimal
            years: Total loan term in years
            year: Year to calculate interest for (1-based)
        
        Returns:
            Annual interest paid in that year
        """
        if year > years or annual_rate == 0 or principal <= 0:
            return 0
        
        monthly_rate = annual_rate / 12
        monthly_payment = self.calculate_monthly_payment(principal, annual_rate, years)
        
        # Calculate interest for each month of the year
        annual_interest = 0
        
        for month in range((year - 1) * 12, year * 12):
            if month >= years * 12:
                break
                
            # Calculate remaining balance at start of this month
            remaining_balance = principal
            for i in range(month):
                interest_payment = remaining_balance * monthly_rate
                principal_payment = monthly_payment - interest_payment
                remaining_balance -= principal_payment
                if remaining_balance <= 0:
                    break
            
            if remaining_balance > 0:
                monthly_interest = remaining_balance * monthly_rate
                annual_interest += monthly_interest
        
        return annual_interest
    
    def get_payment_breakdown(self, principal: float, annual_rate: float, years: int) -> Dict[str, Any]:
        """
        Get a comprehensive breakdown of mortgage payments.
        
        Returns:
            Dictionary with payment details including total interest and costs
        """
        monthly_payment = self.calculate_monthly_payment(principal, annual_rate, years)
        total_payments = monthly_payment * years * 12
        total_interest = total_payments - principal
        
        return {
            "principal": principal,
            "annual_rate": annual_rate,
            "loan_term_years": years,
            "monthly_payment": monthly_payment,
            "total_payments": total_payments,
            "total_interest": total_interest,
            "interest_to_principal_ratio": total_interest / principal if principal > 0 else 0
        }
    
    def calculate_loan_amortization_schedule(self, principal: float, annual_rate: float, 
                                           years: int, max_years: int = None) -> list:
        """
        Calculate year-by-year loan amortization schedule.
        
        Args:
            principal: Original loan amount
            annual_rate: Annual interest rate as decimal
            years: Total loan term in years
            max_years: Maximum years to calculate (for analysis purposes)
        
        Returns:
            List of dictionaries with yearly breakdown
        """
        if max_years is None:
            max_years = years
            
        schedule = []
        remaining_balance = principal
        monthly_payment = self.calculate_monthly_payment(principal, annual_rate, years)
        
        for year in range(1, min(max_years + 1, years + 1)):
            annual_interest = self.calculate_annual_mortgage_interest(principal, annual_rate, years, year)
            annual_principal = (monthly_payment * 12) - annual_interest
            
            # Update remaining balance
            remaining_balance = self.calculate_remaining_balance(principal, annual_rate, years, year)
            
            schedule.append({
                "year": year,
                "annual_payment": monthly_payment * 12,
                "annual_interest": annual_interest,
                "annual_principal": annual_principal,
                "remaining_balance": remaining_balance,
                "cumulative_interest": sum(s["annual_interest"] for s in schedule) + annual_interest,
                "cumulative_principal": principal - remaining_balance
            })
        
        return schedule 