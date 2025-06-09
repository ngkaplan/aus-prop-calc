# Australian Property Investment Calculator

A comprehensive Streamlit web application for comparing different property investment strategies in Australia. This tool helps users make informed decisions by forecasting and comparing the financial outcomes of buying vs. renting vs. investing scenarios with full Australian tax implications.

## 🎯 Project Overview

This calculator compares three primary investment strategies:
1. **Buy to Live**: Purchase a property and live in it (CGT exempt)
2. **Buy to Rent**: Purchase an investment property while renting your residence (with negative gearing benefits)
3. **Rent & Invest**: Rent your residence and invest the capital difference in the stock market

## ✨ Features

### ✅ Current Features (v3.0)
- **Unified Comparison Interface**: All three scenarios compared side-by-side on one page
- **30-Year Financial Modeling**: Comprehensive year-by-year analysis with ROI tracking
- **Australian Tax Integration**: 
  - **Stamp Duty Calculations**: Progressive bracket system with First Home Buyer concessions
  - **Capital Gains Tax**: 50% discount for assets held >12 months, main residence exemption
  - **Negative Gearing Benefits**: Tax deductible investment property losses
  - **Australian Tax Brackets**: Current 2023-24 rates including Medicare levy
  - **Income Growth Modeling**: Salary growth affects tax brackets over time
- **Interactive Visualizations**: 
  - Combined net worth vs. investment charts (after-tax) for all scenarios
  - ROI comparison charts over time
  - Year-by-year cash flow tables (0-30 years) with net worth tracking
- **Perfect Apples-to-Apples Comparison**: Equal total cash invested across all scenarios
- **Australian-Specific Calculations**: 
  - Progressive stamp duty with FHB concessions ($0 under $800k, scaled $800k-$1M)
  - Investment property expenses growing with property values
  - Rental inflation and property growth modeling
  - Mortgage interest vs principal separation for tax purposes
- **Key Milestone Analysis**: 5, 10, 15, 20, 30-year performance snapshots
- **Responsive Input Controls**: Organized parameter sections with tax considerations
- **Real-Time Updates**: All charts and tables update instantly with input changes
- **Tax Impact Visualization**: Clear display of CGT liabilities and negative gearing benefits

### 🔮 Planned Features
- **Historical Analysis**: Backtest strategies using historical CSV data
- **Monte Carlo Simulation**: Model uncertainty with probabilistic scenarios
- **Sensitivity Analysis**: Parameter impact studies
- **CSV Data Integration**: Historical property and stock market data
- **Regional Analysis**: Location-specific market insights
- **Export Functionality**: PDF reports and CSV data export

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/your-username/aus-prop-calc.git
cd aus-prop-calc

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Streamlit Cloud Deployment
1. Push your code to GitHub
2. Connect your repository at [share.streamlit.io](https://share.streamlit.io)
3. Deploy with one click!

## 📊 How It Works

The calculator performs comprehensive financial modeling by:
1. **Unified Input Interface**: All parameters configured including income for tax calculations
2. **Australian Tax Engine**: Full integration of stamp duty, CGT, and negative gearing
3. **Parallel Scenario Analysis**: Simultaneously calculates all three strategies with tax implications
4. **30-Year Projections**: Year-by-year tracking with compound growth, inflation, and tax changes
5. **Equal Investment Logic**: Ensures fair comparison with identical total cash invested
6. **After-Tax Analysis**: All comparisons show true after-tax outcomes
7. **Real-Time Tax Calculations**: Marginal tax rates update with income growth
8. **Comprehensive Reporting**: ROI analysis, tax impact, milestone comparisons, cash flow breakdowns

## 🏗️ Technical Architecture

- **Frontend & Backend**: Streamlit (single application)
- **Calculations**: Python with comprehensive Australian tax calculations
- **Tax Engine**: Full Australian tax brackets, CGT, and negative gearing implementation
- **Visualization**: Plotly for interactive charts showing after-tax performance
- **Data Sources**: CSV files for historical market data
- **Deployment**: Streamlit Cloud (simple, free, automatic)

## 📈 Investment Scenarios

### Buy to Live 🏡
- Property purchase with Australian stamp duty calculations
- First Home Buyer concessions (zero stamp duty under $800k)
- **Main residence CGT exemption** (no capital gains tax when sold)
- Owner-occupier benefits and tax implications
- Opportunity cost of capital tied up in deposit

### Buy to Rent 🏠
- Investment property purchase with full Australian tax implications
- **Negative Gearing Benefits**: Tax deductions for:
  - Mortgage interest payments (not principal)
  - Property expenses (maintenance, rates, insurance)
  - Property management and depreciation
- **Capital Gains Tax**: Applied when sold (50% discount after 12 months)
- Rental income with inflation adjustments
- Separate residential rental costs
- Net worth includes accumulated tax savings

### Rent & Invest 📈
- Residential rental payments with inflation adjustments
- Stock market investment with remaining capital (property equivalent minus rent)
- **Capital Gains Tax**: Applied to stock portfolio gains (50% discount after 12 months)
- Compound growth modeling with configurable return rates  
- Perfect comparison with equal total cash invested
- Flexibility and liquidity advantages

## 💰 Australian Tax Features

### Stamp Duty Calculations
- Progressive bracket system from $1.25/$100 to $7.00/$100
- **First Home Buyer Benefits**:
  - $0 stamp duty for properties under $800,000
  - Scaled concessions for $800k-$1M properties
  - Standard rates for properties over $1M

### Capital Gains Tax (CGT)
- **Buy to Live**: Completely exempt (main residence)
- **Buy to Rent**: Property CGT with 50% discount if held >12 months
- **Rent & Invest**: Stock portfolio CGT with 50% discount if held >12 months
- Uses current income and marginal tax rates for calculations

### Negative Gearing
- **Deductible Expenses**: Mortgage interest + property expenses
- **Tax Savings**: Property losses × marginal tax rate
- **Cumulative Benefits**: Added to net worth over time
- **Real Cash Flow Impact**: Reduces out-of-pocket costs significantly

### Australian Tax Brackets (2023-24)
- Tax-free threshold: $18,200
- 19% tax rate: $18,201 - $45,000
- 32.5% tax rate: $45,001 - $120,000
- 37% tax rate: $120,001 - $180,000
- 45% tax rate: $180,001+
- Medicare levy: 2% on income over $24,276

## 🔧 Development Roadmap

### Phase 1: Core Calculator ✅ COMPLETE
- [x] Basic project setup
- [x] Core calculation engine with all three scenarios
- [x] Unified Streamlit UI implementation  
- [x] Input validation and error handling
- [x] Advanced interactive visualizations
- [x] ROI analysis and milestone tracking
- [x] Year-by-year cash flow analysis
- [x] Equal total investment comparison logic

### Phase 2: Australian Tax Integration ✅ COMPLETE
- [x] Australian stamp duty calculations with FHB concessions
- [x] Capital gains tax implementation with 50% discount
- [x] Negative gearing tax benefits for investment properties
- [x] Australian tax brackets with Medicare levy
- [x] Income growth and marginal tax rate calculations
- [x] After-tax net worth and cash flow analysis

### Phase 3: Enhanced Analysis
- [ ] Historical CSV data integration
- [ ] Monte Carlo simulation engine
- [ ] Advanced depreciation schedules
- [ ] Sensitivity analysis tools

### Phase 4: Advanced Features
- [ ] Regional market CSV datasets
- [ ] Portfolio optimization
- [ ] Advanced charting and reporting
- [ ] Export functionality

## 📁 Data Sources

All historical data will be stored as CSV files in the `/data` directory:
- Property price histories by suburb/region
- Stock market index data (ASX 200, All Ordinaries)
- Interest rate histories
- Rental yield data
- Economic indicators (inflation, unemployment)

## 🤝 Contributing

We welcome contributions! Please ensure:
- Follow the coding standards in `.cursorrules`
- Test your changes locally with `streamlit run app.py`
- Financial calculations are thoroughly tested
- Tax calculations comply with Australian regulations
- CSV data follows established formats

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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
