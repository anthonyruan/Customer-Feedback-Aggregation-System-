# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Customer Feedback Aggregation System** - an AI-powered Streamlit dashboard for analyzing customer feedback with strategic alignment categorization, executive summaries, and opportunity scoring designed for Product Managers.

## Development Commands

### Setup and Run
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Testing
No test framework is configured. Manual testing through the Streamlit interface is currently used.

## Architecture

### Core Components

1. **app.py** - Main Streamlit application that orchestrates the entire UI and workflow
   - Manages session state for data persistence
   - Handles data loading (sample or uploaded CSV)
   - Triggers AI processing
   - Creates interactive filters and visualizations
   - Displays metrics and data tables

2. **data_processor.py** - Data loading, validation, and transformation logic
   - `DataProcessor` class handles CSV validation and cleaning
   - Calculates opportunity scores based on severity and region
   - Filters data based on user selections
   - Provides summary statistics

3. **ai_analyzer.py** - OpenAI integration for AI-powered analysis
   - `AIAnalyzer` class manages OpenAI API interactions
   - Categorizes feedback into 3 strategic priorities
   - Generates executive summaries (max 25 words)
   - Falls back to sample data when API not configured

### Data Flow

1. User loads CSV or sample data ’ `DataProcessor.load_uploaded_file()`
2. Opportunity scores calculated ’ `DataProcessor.calculate_opportunity_score()`
3. AI processing triggered ’ `AIAnalyzer.process_batch()`
4. Filters applied ’ `DataProcessor.filter_data()`
5. Visualizations and metrics displayed ’ Streamlit components

### Strategic Categories

The system categorizes feedback into exactly 3 priorities (defined in `ai_analyzer.py`):
- "Win Enterprise Deals"
- "Ensure Regulatory & Data Compliance"
- "Improve Platform Usability & Performance"

### Scoring System

Opportunity Score = Severity Score + Region Score (range: 3-8)

Defined in `data_processor.py`:
- Severity: Critical=5, High=4, Medium=3, Low=2
- Region: US=3, EU=2, APAC=1, LATAM=1

## Environment Configuration

### Required Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

The system works without the API key by using sample AI data for demonstrations.

## CSV Format Requirements

Required columns (validated in `DataProcessor._validate_and_clean_data()`):
- `Feedback` - Customer feedback text
- `Product` - Product/module name
- `Severity` - Critical, High, Medium, or Low
- `Region` - US, EU, APAC, or LATAM
- `Category` - (Optional) Human-assigned category

## Key Implementation Details

- Session state management prevents data loss during Streamlit reruns
- AI processing includes retry logic with exponential backoff
- Invalid severity/region values default to Medium/APAC respectively
- Dataframe styling applies color coding based on severity and opportunity scores
- Progress bars provide feedback during AI processing
- All AI calls use GPT-3.5-turbo with low temperature (0.1) for consistency