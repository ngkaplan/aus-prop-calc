"""
Stamp duty calculations for Australian property purchases.
"""

from ...config.australian_config import (
    STAMP_DUTY_BRACKETS, 
    FHB_STAMP_DUTY_EXEMPT_THRESHOLD, 
    FHB_STAMP_DUTY_FULL_THRESHOLD
)


class StampDutyCalculator:
    """Calculator for Australian stamp duty on property purchases."""
    
    def calculate_stamp_duty(self, property_price: float, is_first_home_buyer: bool = False) -> float:
        """
        Calculate stamp duty for a property purchase.
        
        Args:
            property_price: Purchase price of the property
            is_first_home_buyer: Whether buyer qualifies for FHB concessions
        
        Returns:
            Stamp duty amount
        """
        if property_price <= 0:
            return 0
        
        # Calculate base stamp duty
        base_duty = self._calculate_base_stamp_duty(property_price)
        
        # Apply first home buyer concessions if applicable
        if is_first_home_buyer:
            return self._apply_fhb_concessions(base_duty, property_price)
        
        return base_duty
    
    def _calculate_base_stamp_duty(self, property_price: float) -> float:
        """Calculate stamp duty using the progressive bracket system."""
        stamp_duty = 0
        
        for bracket in STAMP_DUTY_BRACKETS:
            if property_price <= bracket["min"]:
                break
                
            # Calculate taxable amount in this bracket
            taxable_in_bracket = min(property_price, bracket["max"]) - bracket["min"] + 1
            
            if taxable_in_bracket > 0:
                stamp_duty = bracket["base"] + (taxable_in_bracket * bracket["rate"])
        
        # Apply minimum amount if specified
        if "min_amount" in STAMP_DUTY_BRACKETS[0] and stamp_duty < STAMP_DUTY_BRACKETS[0]["min_amount"]:
            return STAMP_DUTY_BRACKETS[0]["min_amount"]
        
        return stamp_duty
    
    def _apply_fhb_concessions(self, base_duty: float, property_price: float) -> float:
        """Apply first home buyer concessions to stamp duty."""
        if property_price <= FHB_STAMP_DUTY_EXEMPT_THRESHOLD:
            # No stamp duty for FHB under threshold
            return 0
        elif property_price <= FHB_STAMP_DUTY_FULL_THRESHOLD:
            # Scaled concession between thresholds
            concession_range = FHB_STAMP_DUTY_FULL_THRESHOLD - FHB_STAMP_DUTY_EXEMPT_THRESHOLD
            price_above_exempt = property_price - FHB_STAMP_DUTY_EXEMPT_THRESHOLD
            concession_factor = price_above_exempt / concession_range
            return base_duty * concession_factor
        else:
            # Full stamp duty for FHB over upper threshold
            return base_duty
    
    def get_stamp_duty_breakdown(self, property_price: float, is_first_home_buyer: bool = False) -> dict:
        """
        Get detailed breakdown of stamp duty calculation.
        
        Returns:
            Dictionary with calculation details
        """
        base_duty = self._calculate_base_stamp_duty(property_price)
        final_duty = self.calculate_stamp_duty(property_price, is_first_home_buyer)
        
        return {
            "property_price": property_price,
            "base_stamp_duty": base_duty,
            "is_first_home_buyer": is_first_home_buyer,
            "fhb_savings": base_duty - final_duty if is_first_home_buyer else 0,
            "final_stamp_duty": final_duty,
            "effective_rate": final_duty / property_price if property_price > 0 else 0
        } 