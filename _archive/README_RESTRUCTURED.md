# Australian Property Calculator - Domain-Driven Architecture

## Overview

This document describes the restructured version of the Australian Property Investment Calculator, which has been refactored using domain-driven design principles for improved maintainability, testability, and scalability.

## New Architecture

### Directory Structure

```
src/
├── domain/                    # Business logic and domain models
│   ├── tax/
│   │   └── australian_tax.py        # Australian tax calculations
│   ├── property/
│   │   ├── stamp_duty.py           # Stamp duty calculations
│   │   └── mortgage.py             # Mortgage calculations
│   ├── investment/
│   │   └── stock_calculator.py     # Stock investment calculations
│   └── scenarios/
│       └── scenario_calculator.py  # Main scenario orchestrator
├── ui/                        # User interface components
│   └── components/
│       ├── input_forms.py          # Input form management
│       ├── charts.py              # Chart visualization
│       └── summary_tables.py      # Summary displays
├── utils/                     # Utility functions
│   ├── formatters.py              # Currency/percentage formatting
│   └── validators.py              # Input validation
└── config/                    # Configuration and constants
    ├── defaults.py               # Default values
    └── australian_config.py      # Australian-specific constants
```

## Key Components

### Domain Layer

#### Tax Domain (`src/domain/tax/`)
- **AustralianTaxCalculator**: Handles all Australian tax calculations including:
  - Income tax and Medicare levy
  - Marginal tax rate calculations
  - Capital gains tax (with 50% discount)
  - Negative gearing benefits

#### Property Domain (`src/domain/property/`)
- **StampDutyCalculator**: Australian stamp duty calculations with FHB concessions
- **MortgageCalculator**: Mortgage payments, balances, and interest calculations

#### Investment Domain (`src/domain/investment/`)
- **StockInvestmentCalculator**: Stock market investment projections and compound growth

#### Scenarios Domain (`src/domain/scenarios/`)
- **ScenarioCalculator**: Main orchestrator that coordinates all domain calculations for the three investment scenarios

### UI Layer (`src/ui/`)

#### Input Components
- **InputFormManager**: Manages all Streamlit input forms with validation and defaults

#### Visualization Components  
- **ChartManager**: Creates and renders Plotly charts for scenario comparisons
- **SummaryTableManager**: Handles summary metrics, comparison tables, and cash flow displays

### Configuration Layer (`src/config/`)
- **defaults.py**: Default values for all parameters
- **australian_config.py**: Australian-specific constants (tax brackets, stamp duty rates, etc.)

### Utilities (`src/utils/`)
- **formatters.py**: Currency and percentage formatting utilities
- **validators.py**: Input validation functions

## Architecture Benefits

### 🏗️ Modularity
- **Separated Concerns**: Each domain handles its specific business logic
- **Reusable Components**: UI components can be easily reused or modified
- **Clear Dependencies**: Explicit imports make dependencies obvious
- **Easier Testing**: Isolated components are easier to unit test

### 🔧 Maintainability
- **Single Responsibility**: Each class has a single, well-defined purpose
- **Domain Expertise**: Tax logic is separate from mortgage logic is separate from UI logic
- **Enhanced Readability**: Code is organized by business domain rather than technical layers
- **Simplified Debugging**: Issues can be isolated to specific domains

### 📈 Scalability
- **Easy Extensions**: New scenarios or calculations can be added without affecting existing code
- **Configuration Management**: Australian-specific constants are centralized and easily updated
- **Plugin Architecture**: The modular design supports future plugin development
- **UI Independence**: Business logic is decoupled from presentation layer

## Running the Applications

### Original Application
```bash
streamlit run app.py
```

### Restructured Demo
```bash
streamlit run app_restructured.py
```

The restructured demo shows the new architecture while maintaining 100% compatibility with existing calculations.

## Migration Benefits

### For Developers
- **Faster Feature Development**: New features can be added to specific domains without understanding the entire codebase
- **Easier Onboarding**: New developers can focus on specific domains
- **Better Code Reviews**: Changes are isolated to relevant domains
- **Improved Testing**: Each component can be tested independently

### For Maintenance
- **Bug Isolation**: Issues can be quickly isolated to specific domains
- **Regulatory Updates**: Australian tax changes only require updates to the tax domain
- **UI Updates**: Interface changes don't affect business logic
- **Performance Optimization**: Specific calculators can be optimized independently

## Example Usage

### Using Domain Components Directly

```python
from src.domain.tax.australian_tax import AustralianTaxCalculator
from src.domain.property.stamp_duty import StampDutyCalculator

# Calculate tax for a specific income
tax_calc = AustralianTaxCalculator()
income_tax = tax_calc.calculate_income_tax(100000)
marginal_rate = tax_calc.calculate_marginal_tax_rate(100000)

# Calculate stamp duty with FHB concessions
stamp_calc = StampDutyCalculator()
stamp_duty = stamp_calc.calculate_stamp_duty(800000, is_first_home_buyer=True)
```

### Using UI Components

```python
from src.ui.components.input_forms import InputFormManager
from src.ui.components.charts import ChartManager

# Render input forms
input_manager = InputFormManager()
params = input_manager.render_all_inputs()

# Create charts
chart_manager = ChartManager()
chart_manager.render_all_charts(btl_analysis, btr_analysis, ri_analysis)
```

## Future Enhancements

The new architecture supports several future enhancements:

1. **State-Specific Calculations**: Easy to add state-specific stamp duty and land tax
2. **International Support**: Framework for adding other countries' tax systems
3. **Advanced Scenarios**: New investment scenarios can be added as plugins
4. **API Development**: Business logic can be exposed as REST APIs
5. **Mobile Apps**: Domain logic can be reused in mobile applications
6. **Batch Processing**: Calculations can be run on multiple scenarios simultaneously

## Conclusion

The domain-driven restructure provides a solid foundation for future development while maintaining all existing functionality. The modular design makes the codebase more maintainable, testable, and scalable, setting the stage for continued enhancement of the Australian Property Investment Calculator. 