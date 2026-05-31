# Australian Property Investment Calculator

A comprehensive Streamlit web application for comparing different property investment strategies in Australia. This tool helps users make informed decisions by forecasting and comparing the financial outcomes of buying vs. renting vs. investing scenarios with full Australian tax implications.

## 🎯 Project Overview

This calculator compares three primary investment strategies:
1. **Buy to Live**: Purchase a property and live in it (CGT exempt)
2. **Buy to Rent**: Purchase an investment property while renting your residence (with negative gearing benefits)
3. **Rent & Invest**: Rent your residence and invest the capital difference in the stock market

## 🧭 Project Status

- **Architecture**: The app has been refactored into a clean, domain-driven structure with domain calculators and UI components clearly separated.
- **UI**: Streamlit interface is fully functional with live scenario comparison and charts.
- **Testing**: Foundational automated tests are in place for core financial calculators and scenario horizon behavior.
- **Known limitations**: Export/reporting and sensitivity analysis are still pending (see roadmap below).

If you're considering contributions, the roadmap section below highlights the highest-impact additions.

## ✨ Features

- **Unified Comparison Interface**: All three scenarios compared side-by-side
- **Configurable Financial Modeling Horizon (10–40 years)**: Comprehensive year-by-year analysis with ROI tracking
- **Australian Tax Integration**: 
  - **Stamp Duty Calculations**: Progressive brackets with First Home Buyer concessions
  - **Capital Gains Tax**: 50% discount for assets held >12 months, main residence exemption
  - **Negative Gearing Benefits**: Tax deductible investment property losses
  - **Australian Tax Brackets**: Current rates including Medicare levy
- **Interactive Visualizations & Reporting**: 
  - Net worth progression charts (after-tax) for all scenarios
  - ROI comparison over time
  - Year-by-year cash flow tables with net worth tracking
  - CSV/XLSX export downloads for cash flow and scenario summaries
- **Perfect Comparison**: Equal total cash invested across all scenarios
- **Australian-Specific**: 
  - Progressive stamp duty with FHB concessions
  - Investment property expense modeling
  - Rental inflation and property growth
  - Mortgage interest vs principal separation for tax purposes
- **Key Milestone Analysis**: 5, 10, 15, 20, 30-year performance snapshots

## 🚀 Quick Start

### Installation & Running
```bash
# Clone the repository
git clone https://github.com/your-username/aus-prop-calc.git
cd aus-prop-calc

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📊 How It Works

The calculator performs comprehensive financial modeling by:
1. **Unified Input Interface**: All parameters configured including income for tax calculations
2. **Australian Tax Engine**: Full integration of stamp duty, CGT, and negative gearing
3. **Parallel Scenario Analysis**: Simultaneously calculates all three strategies
4. **Configurable Projections (10–40 years)**: Year-by-year tracking with compound growth and tax changes
5. **Equal Investment Logic**: Ensures fair comparison with identical total cash invested
6. **After-Tax Analysis**: All comparisons show true after-tax outcomes

## 🏗️ Technical Architecture

### Clean Domain-Driven Design
```
src/
├── domain/                 # Business logic
│   ├── scenarios/         # Main scenario calculations
│   ├── property/          # Property & mortgage logic
│   ├── investment/        # Stock investment calculations
│   └── tax/              # Australian tax calculations
├── ui/                    # User interface components
│   └── components/       # Streamlit UI modules
├── config/               # Configuration & constants
└── utils/                # Shared utilities
```

- **Modular Architecture**: Separated business logic from UI
- **Single Responsibility**: Each module has a clear purpose
- **Testable Components**: Independent, focused classes
- **Maintainable Code**: Easy to extend and modify

## 📈 Investment Scenarios

### Buy to Live 🏡
- Property purchase with Australian stamp duty calculations
- First Home Buyer concessions (zero stamp duty under $800k)
- **Main residence CGT exemption** (no capital gains tax when sold)
- Owner-occupier benefits and tax implications

### Buy to Rent 🏠
- Investment property purchase with full Australian tax implications
- **Negative Gearing Benefits**: Tax deductions for mortgage interest and property expenses
- **Capital Gains Tax**: Applied when sold (50% discount after 12 months)
- Rental income with inflation adjustments
- Net worth includes accumulated tax savings

### Rent & Invest 📈
- Residential rental payments with inflation adjustments
- Stock market investment with remaining capital
- **Capital Gains Tax**: Applied to stock portfolio gains (50% discount after 12 months)
- Compound growth modeling with configurable return rates
- Flexibility and liquidity advantages

## 💰 Australian Tax Features

### Stamp Duty Calculations
- Progressive bracket system from $1.25/$100 to $7.00/$100
- **First Home Buyer Benefits**:
  - $0 stamp duty for properties under $800,000
  - Scaled concessions for $800k-$1M properties

### Capital Gains Tax (CGT)
- **Buy to Live**: Completely exempt (main residence)
- **Buy to Rent**: Property CGT with 50% discount if held >12 months
- **Rent & Invest**: Stock portfolio CGT with 50% discount if held >12 months

### Negative Gearing
- **Deductible Expenses**: Mortgage interest + property expenses
- **Tax Savings**: Property losses × marginal tax rate
- **Cumulative Benefits**: Added to net worth over time

### Australian Tax Brackets (2023-24)
- Tax-free threshold: $18,200
- 19% tax rate: $18,201 - $45,000
- 32.5% tax rate: $45,001 - $120,000
- 37% tax rate: $120,001 - $180,000
- 45% tax rate: $180,001+
- Medicare levy: 2% on income over $24,276

## 🧪 Testing

```bash
# Run tests (when implemented)
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src
```

## 🗺️ Roadmap / Ideas to Add

- **Expand automated tests**: Grow coverage for mortgage schedules, stamp duty, tax brackets, and scenario calculators to lock in financial accuracy.
- **Scenario assumptions presets**: Offer prebuilt profiles (e.g., conservative/base/aggressive) for quicker comparisons.
- **Sensitivity analysis**: Let users sweep rates (interest, growth, rental inflation) and visualize outcome ranges.

## 🤝 Contributing

We welcome contributions! Please ensure:
- Follow the coding standards in `.cursorrules`
- Test your changes locally with `streamlit run app.py`
- Financial calculations are thoroughly tested
- Maintain the clean architecture patterns

## 📁 Project History

This project was restructured from a monolithic codebase to a clean, domain-driven architecture. Original files are preserved in the `_archive/` directory for reference.

## 📝 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This calculator is for educational purposes only and should not be considered financial advice. Tax calculations are based on current Australian tax law and may not reflect all individual circumstances. Please consult with a qualified financial advisor and tax professional for personalized investment and tax advice.

## 🙏 Acknowledgments

- Australian Taxation Office for tax information
- Australian Bureau of Statistics for housing data
- Reserve Bank of Australia for economic indicators
- Open source Python community for excellent libraries

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/your-username/aus-prop-calc/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/aus-prop-calc/discussions)
