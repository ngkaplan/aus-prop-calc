"""
Stock market investment calculations for the rent and invest scenario.
"""

from typing import Dict, Any, List


class StockInvestmentCalculator:
    """Calculator for stock market investment returns and growth projections."""
    
    def calculate_compound_growth(self, initial_amount: float, annual_return_rate: float, 
                                 years: int, regular_contribution: float = 0) -> float:
        """
        Calculate compound growth with optional regular contributions.
        
        Args:
            initial_amount: Initial investment amount
            annual_return_rate: Annual return rate as decimal (e.g., 0.07 for 7%)
            years: Number of years to compound
            regular_contribution: Annual regular contribution (optional)
        
        Returns:
            Final investment value after compound growth
        """
        if years <= 0:
            return initial_amount
            
        value = initial_amount
        
        for year in range(years):
            # Apply annual return
            value *= (1 + annual_return_rate)
            # Add regular contribution at end of year
            value += regular_contribution
        
        return value
    
    def calculate_yearly_investment_growth(self, initial_amount: float, annual_return_rate: float,
                                         years: int, regular_contribution: float = 0) -> List[Dict[str, Any]]:
        """
        Calculate year-by-year investment growth.
        
        Args:
            initial_amount: Initial investment amount
            annual_return_rate: Annual return rate as decimal
            years: Number of years to project
            regular_contribution: Annual regular contribution
        
        Returns:
            List of yearly investment values and growth
        """
        yearly_data = []
        value = initial_amount
        cumulative_contributions = initial_amount
        
        for year in range(1, years + 1):
            # Calculate growth for this year
            annual_growth = value * annual_return_rate
            value += annual_growth
            
            # Add regular contribution
            value += regular_contribution
            cumulative_contributions += regular_contribution
            
            cumulative_gains = value - cumulative_contributions
            
            yearly_data.append({
                "year": year,
                "investment_value": value,
                "annual_growth": annual_growth,
                "annual_contribution": regular_contribution,
                "cumulative_contributions": cumulative_contributions,
                "cumulative_gains": cumulative_gains,
                "return_percentage": (cumulative_gains / cumulative_contributions) if cumulative_contributions > 0 else 0
            })
        
        return yearly_data
    
    def calculate_total_return(self, initial_amount: float, final_amount: float) -> Dict[str, float]:
        """
        Calculate total return metrics.
        
        Args:
            initial_amount: Initial investment
            final_amount: Final investment value
        
        Returns:
            Dictionary with return metrics
        """
        total_gain = final_amount - initial_amount
        percentage_return = (total_gain / initial_amount) if initial_amount > 0 else 0
        
        return {
            "initial_amount": initial_amount,
            "final_amount": final_amount,
            "total_gain": total_gain,
            "percentage_return": percentage_return,
            "multiple": final_amount / initial_amount if initial_amount > 0 else 0
        }
    
    def calculate_equivalent_deposit_investment(self, property_deposit: float, 
                                              annual_return_rate: float, years: int) -> Dict[str, Any]:
        """
        Calculate what happens if you invest the property deposit equivalent in stocks.
        
        Args:
            property_deposit: Amount that would have been used as property deposit
            annual_return_rate: Expected annual stock return rate
            years: Investment period in years
        
        Returns:
            Investment projection details
        """
        final_value = self.calculate_compound_growth(property_deposit, annual_return_rate, years)
        yearly_growth = self.calculate_yearly_investment_growth(property_deposit, annual_return_rate, years)
        returns = self.calculate_total_return(property_deposit, final_value)
        
        return {
            "initial_investment": property_deposit,
            "annual_return_rate": annual_return_rate,
            "years": years,
            "final_value": final_value,
            "yearly_growth": yearly_growth,
            "return_metrics": returns,
            "average_annual_return": returns["percentage_return"] / years if years > 0 else 0
        }
    
    def calculate_dollar_cost_averaging(self, monthly_amount: float, annual_return_rate: float,
                                      years: int) -> Dict[str, Any]:
        """
        Calculate dollar cost averaging strategy returns.
        
        Args:
            monthly_amount: Monthly investment amount
            annual_return_rate: Expected annual return rate
            years: Investment period in years
        
        Returns:
            DCA investment projection
        """
        # Convert to annual contribution for calculation
        annual_contribution = monthly_amount * 12
        
        # Start with no initial amount for pure DCA
        final_value = self.calculate_compound_growth(0, annual_return_rate, years, annual_contribution)
        total_contributed = annual_contribution * years
        
        return {
            "monthly_amount": monthly_amount,
            "annual_contribution": annual_contribution,
            "total_contributed": total_contributed,
            "final_value": final_value,
            "total_gain": final_value - total_contributed,
            "return_percentage": ((final_value - total_contributed) / total_contributed) if total_contributed > 0 else 0,
            "years": years
        } 