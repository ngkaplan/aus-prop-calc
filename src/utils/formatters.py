"""
Formatting utilities for currency, percentages, and other display values.
"""

def format_currency(amount: float) -> str:
    """Format currency for Australian dollars"""
    return f"${amount:,.0f}"

def format_hover_currency(amount: float) -> str:
    """Format currency for hover display (to nearest 1k)"""
    if amount >= 1000000:
        return f"${amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"${amount/1000:.0f}k"
    else:
        return f"${amount:.0f}"

def format_hover_percent(percent: float) -> str:
    """Format percentage for hover display (to nearest whole %)"""
    return f"{percent:.0f}%"

def format_percentage(value: float, decimal_places: int = 1) -> str:
    """Format a decimal as a percentage"""
    return f"{value * 100:.{decimal_places}f}%" 