# Customer Feedback Aggregation System

An AI-powered dashboard for analyzing customer feedback with strategic alignment categorization, executive summaries, and opportunity scoring designed for Product Managers.

## 🚀 Features

- **AI Strategic Alignment**: Automatically categorizes feedback into 3 key strategic priorities
- **Executive Summaries**: AI-generated one-sentence summaries for quick understanding
- **Opportunity Scoring**: Rule-based ranking system combining severity and region impact
- **Interactive Dashboard**: Advanced filtering and real-time data exploration
- **Data Visualizations**: Charts showing feedback distribution and trends
- **Export Capabilities**: Download filtered results for further analysis

## 📋 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (optional - sample data works without API)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "Customer Feedback Aggregation System"
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API (Optional)**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key:
   # OPENAI_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎯 Strategic Categories

The AI categorizes feedback into three strategic priorities:

1. **Win Enterprise Deals** - Features needed to attract large enterprise customers
2. **Ensure Regulatory & Data Compliance** - Security, privacy, and regulatory requirements  
3. **Improve Platform Usability & Performance** - UX optimization and stability improvements

## 📊 Opportunity Scoring

Feedback is ranked using a simple scoring system:

**Severity Scores:**
- Critical: 5 points
- High: 4 points
- Medium: 3 points
- Low: 2 points

**Region Scores:**
- US: 3 points
- EU: 2 points
- APAC: 1 point
- LATAM: 1 point

**Total Score = Severity Score + Region Score** (Range: 3-8)

## 📁 Required CSV Format

Your CSV file should contain these columns:

| Column | Description | Example |
|--------|-------------|---------|
| Feedback | Customer feedback text | "Dashboard loading is too slow" |
| Product | Product/module name | "Analytics Dashboard" |
| Severity | Issue severity level | "High" |
| Region | Customer region | "US" |
| Category | (Optional) Human-assigned category | "Improve Platform Usability & Performance" |

## 💡 Usage Guide

### Using Sample Data
1. Check "Use Sample Data" in the sidebar
2. Click "Load Sample Data"
3. Click "Process with AI" to analyze feedback
4. Use filters to explore specific insights

### Using Your Own Data
1. Uncheck "Use Sample Data" in the sidebar
2. Upload your CSV file using the file uploader
3. Click "Process with AI" to analyze feedback
4. Use filters to explore specific insights

### Dashboard Features
- **Metrics Overview**: Total feedback, critical issues, compliance issues, average opportunity score
- **Interactive Filters**: Filter by strategic priority, product, severity, and region
- **Visualizations**: Bar charts and pie charts showing feedback distribution
- **Data Table**: Sortable table with all feedback details and AI analysis
- **Export**: Download filtered data as CSV

## 🏗 Project Structure

```
Customer Feedback Aggregation System/
├── app.py                 # Main Streamlit application
├── data_processor.py      # Data loading and processing functions
├── ai_analyzer.py         # OpenAI integration for AI analysis
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── Todo.md               # Detailed implementation plan
├── README.md             # This file
└── venv/                 # Virtual environment (created after setup)
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Without OpenAI API
The system works with sample AI data when no API key is configured, perfect for demonstrations and testing.

## 🎨 Customization

### Adding New Categories
Edit the `STRATEGIC_CATEGORIES` list in `ai_analyzer.py`:
```python
STRATEGIC_CATEGORIES = [
    "Your Custom Category 1",
    "Your Custom Category 2", 
    "Your Custom Category 3"
]
```

### Modifying Scoring Algorithm
Update the scoring dictionaries in `data_processor.py`:
```python
SEVERITY_SCORES = {
    'Critical': 5,
    'High': 4,
    'Medium': 3,
    'Low': 2
}

REGION_SCORES = {
    'US': 3,
    'EU': 2,
    'APAC': 1,
    'LATAM': 1
}
```

## 🚨 Troubleshooting

### Common Issues

**"ModuleNotFoundError"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**"OpenAI API Error"**
- Check your API key in `.env` file
- Verify you have sufficient API credits
- The app will use sample data if API is unavailable

**"Empty CSV Error"**
- Ensure your CSV has the required columns
- Check for proper formatting and encoding (UTF-8)

**Streamlit Issues**
- Try restarting the app with `streamlit run app.py`
- Clear browser cache if interface issues occur

## 📈 Performance Notes

- Processing time depends on dataset size and OpenAI API response times
- Large datasets (1000+ items) may take several minutes to process
- Consider batch processing for very large datasets
- The app includes progress indicators for long-running operations

## 🔮 Future Enhancements

- Real-time data integration with CRM systems
- Advanced analytics and trend analysis
- User authentication and role-based access
- Automated report generation
- Machine learning model training for improved categorization
- Integration with project management tools

## 📄 License

This project is built for internal use. Modify and distribute according to your organization's policies.

## 🤝 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the detailed implementation plan in `Todo.md`
3. Examine the code comments for technical details

---

**Built for Product Managers who need fast, AI-powered insights from customer feedback.**