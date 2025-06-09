# Australian Property Investment Calculator

A comprehensive Streamlit web application for comparing different property investment strategies in Australia. This tool helps users make informed decisions by forecasting and comparing the financial outcomes of buying vs. renting vs. investing scenarios.

## 🎯 Project Overview

This calculator compares three primary investment strategies:
1. **Buy to Live**: Purchase a property and live in it
2. **Buy to Rent**: Purchase an investment property while renting your residence
3. **Rent & Invest**: Rent your residence and invest the capital difference in the stock market

## ✨ Features

### Current (v1.0)
- Point-in-time financial forecasting over mortgage lifetime
- Comprehensive input parameters (property price, growth rates, costs, etc.)
- Side-by-side comparison of investment strategies
- Interactive Streamlit web interface
- Australian-specific calculations (stamp duty, capital gains tax, etc.)

### Planned Features
- **Historical Analysis**: Backtest strategies using historical CSV data
- **Monte Carlo Simulation**: Model uncertainty with probabilistic scenarios
- **Sensitivity Analysis**: Understand how key parameters affect outcomes
- **CSV Data Integration**: Historical property and stock market data from CSV files
- **Advanced Visualizations**: Interactive charts and scenario comparisons
- **Regional Analysis**: Location-specific property market insights from CSV datasets

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
1. Taking user inputs through an intuitive Streamlit interface
2. Calculating all upfront and ongoing costs for each strategy
3. Projecting cash flows over the mortgage term (typically 25-30 years)
4. Accounting for Australian tax implications
5. Computing net present value and total returns
6. Providing detailed breakdowns and interactive visualizations

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
- Residential rental payments
- Stock market investment with available capital
- Tax implications of investment returns
- Flexibility and liquidity advantages

## 🔧 Development Roadmap

### Phase 1: Core Calculator (Current)
- [x] Basic project setup
- [ ] Core calculation engine
- [ ] Streamlit UI implementation
- [ ] Input validation and error handling
- [ ] Basic visualizations

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
