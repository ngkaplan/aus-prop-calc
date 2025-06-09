# Australian Property Investment Calculator

A comprehensive Streamlit web application for comparing different property investment strategies in Australia. This tool helps users make informed decisions by forecasting and comparing the financial outcomes of buying vs. renting vs. investing scenarios.

## 🎯 Project Overview

This calculator compares three primary investment strategies:
1. **Buy to Live**: Purchase a property and live in it
2. **Buy to Rent**: Purchase an investment property while renting your residence
3. **Rent & Invest**: Rent your residence and invest the capital difference in the stock market

## ✨ Features

### ✅ Current Features (v2.0)
- **Unified Comparison Interface**: All three scenarios compared side-by-side on one page
- **30-Year Financial Modeling**: Comprehensive year-by-year analysis with ROI tracking
- **Interactive Visualizations**: 
  - Combined net worth vs. investment charts for all scenarios
  - ROI comparison charts over time
  - Year-by-year cash flow tables (0-30 years)
- **Perfect Apples-to-Apples Comparison**: Equal total cash invested across all scenarios
- **Australian-Specific Calculations**: Property expenses, rental yields, tax implications
- **Key Milestone Analysis**: 5, 10, 15, 20, 30-year performance snapshots
- **Responsive Input Controls**: Sliders and organized parameter sections
- **Real-Time Updates**: All charts and tables update instantly with input changes

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
1. **Unified Input Interface**: All parameters configured in organized sections
2. **Parallel Scenario Analysis**: Simultaneously calculates all three strategies
3. **30-Year Projections**: Year-by-year tracking with compound growth and inflation
4. **Equal Investment Logic**: Ensures fair comparison with identical total cash invested
5. **Australian Tax Modeling**: Property expenses, rental yields, growth assumptions
6. **Real-Time Visualization**: Interactive charts and tables update instantly
7. **Comprehensive Reporting**: ROI analysis, milestone comparisons, cash flow breakdowns

## 🏗️ Technical Architecture

- **Frontend & Backend**: Streamlit (single application)
- **Calculations**: Python with pandas, numpy for financial modeling
- **Visualization**: Plotly for interactive charts
- **Data Sources**: CSV files for historical market data
- **Deployment**: Streamlit Cloud (simple, free, automatic)

## 📈 Investment Scenarios

### Buy to Live
- Property purchase and mortgage payments
- Owner-occupier benefits and tax implications
- Opportunity cost of capital tied up in deposit

### Buy to Rent (Investment Property)
- Investment property purchase with rental income
- Tax deductions for investment expenses
- Capital gains tax considerations
- Separate residential rental costs

### Rent & Invest
- Residential rental payments with inflation adjustments
- Stock market investment with remaining capital (property equivalent minus rent)
- Compound growth modeling with configurable return rates  
- Perfect comparison with equal total cash invested
- Flexibility and liquidity advantages

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

### Phase 2: Enhanced Analysis
- [ ] Historical CSV data integration
- [ ] Monte Carlo simulation engine
- [ ] Advanced tax calculations
- [ ] Sensitivity analysis tools

### Phase 3: Advanced Features
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
- CSV data follows established formats

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Australian Bureau of Statistics for housing data
- Reserve Bank of Australia for economic indicators
- Open source Python community for excellent libraries

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/your-username/aus-prop-calc/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/aus-prop-calc/discussions)
