import streamlit as st

# Robinhood-Inspired Color Palette
class RobinhoodColors:
    # Primary Colors
    SUCCESS_GREEN = "#00C853"
    DANGER_RED = "#D50000" 
    
    # Neutral Colors
    BACKGROUND_WHITE = "#FFFFFF"
    PRIMARY_TEXT = "#111418"
    SECONDARY_TEXT = "#6B7280"
    LIGHT_GRAY = "#F8F9FA"
    MEDIUM_GRAY = "#E5E7EB"
    BORDER_GRAY = "#D1D5DB"
    
    # Highlight Accent
    ACCENT_YELLOW = "#CCFF00"
    
    # Additional Financial App Colors
    POSITIVE_LIGHT = "#E8F5E8"
    NEGATIVE_LIGHT = "#FFEBEE"
    NEUTRAL_BLUE = "#1E40AF"
    CHART_PURPLE = "#8B5CF6"

def inject_robinhood_css():
    """Inject custom CSS to achieve Robinhood-inspired styling"""
    
    css = f"""
    <style>
    /* Import Inter font for modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {{
        background: linear-gradient(180deg, #FFFFFF 0%, #FAFBFC 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: {RobinhoodColors.PRIMARY_TEXT};
        line-height: 1.5;
        position: relative;
    }}
    
    /* Animated background pattern */
    .main::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(0, 200, 83, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(30, 64, 175, 0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }}
    
    /* Hide Streamlit default elements but keep sidebar toggle */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Keep header visible but style it minimally */
    header[data-testid="stHeader"] {{
        background-color: transparent;
        height: 3rem;
    }}
    
    /* Style the sidebar toggle button */
    button[kind="header"] {{
        color: {RobinhoodColors.PRIMARY_TEXT};
    }}
    
    /* Custom Header */
    .robinhood-header {{
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 50%, #E0F2FE 100%);
        padding: 3rem 0;
        margin-bottom: 2rem;
        border-bottom: 2px solid transparent;
        border-image: linear-gradient(90deg, {RobinhoodColors.SUCCESS_GREEN}, {RobinhoodColors.CHART_PURPLE}, {RobinhoodColors.NEUTRAL_BLUE}) 1;
        position: relative;
        overflow: hidden;
    }}
    
    .robinhood-header::after {{
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 40%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 200, 83, 0.05), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%) rotate(45deg); }}
        100% {{ transform: translateX(200%) rotate(45deg); }}
    }}
    
    .header-title {{
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, {RobinhoodColors.PRIMARY_TEXT} 0%, {RobinhoodColors.NEUTRAL_BLUE} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.025em;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    .header-subtitle {{
        font-size: 1.125rem;
        color: {RobinhoodColors.SECONDARY_TEXT};
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }}
    
    /* Streamlit Metric Cards Enhancement */
    div[data-testid="metric-container"] {{
        background: linear-gradient(135deg, #FFFFFF 0%, #FAFBFC 100%);
        border: 1px solid rgba(209, 213, 219, 0.5);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 1px 3px rgba(0, 0, 0, 0.06),
            0 10px 20px rgba(0, 0, 0, 0.04);
        position: relative;
        overflow: hidden;
    }}
    
    div[data-testid="metric-container"]:hover {{
        box-shadow: 
            0 4px 12px rgba(0, 0, 0, 0.1),
            0 20px 40px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
        border-color: {RobinhoodColors.SUCCESS_GREEN};
    }}
    
    /* Metric value styling */
    div[data-testid="metric-container"] [data-testid="metric-value"] {{
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1 !important;
    }}
    
    /* Metric label styling */
    div[data-testid="metric-container"] [data-testid="metric-label"] {{
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: {RobinhoodColors.SECONDARY_TEXT} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* Metric delta styling */
    div[data-testid="metric-container"] [data-testid="metric-delta"] {{
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* Container styling for better layout */
    .stContainer > div {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 250, 252, 0.8) 100%);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(209, 213, 219, 0.3);
    }}
    
    /* Enhanced Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #FFFFFF 0%, #F8F9FA 50%, #E5E7EB 100%);
        border-right: none;
        box-shadow: 
            4px 0 12px rgba(0, 0, 0, 0.05),
            inset -1px 0 0 rgba(209, 213, 219, 0.3);
        position: relative;
    }}
    
    /* Sidebar gradient overlay */
    section[data-testid="stSidebar"]::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(180deg, {RobinhoodColors.SUCCESS_GREEN} 0%, {RobinhoodColors.CHART_PURPLE} 50%, {RobinhoodColors.NEUTRAL_BLUE} 100%);
        z-index: 10;
    }}
    
    section[data-testid="stSidebar"] > div {{
        padding: 2rem 1rem 1rem 1rem;
    }}
    
    /* Sidebar header enhancement */
    section[data-testid="stSidebar"] .sidebar-header {{
        font-size: 1rem;
        font-weight: 700;
        color: {RobinhoodColors.PRIMARY_TEXT};
        margin: 2rem 0 1rem 0;
        padding: 0.75rem 1rem;
        background: linear-gradient(135deg, rgba(0, 200, 83, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
        border-radius: 12px;
        border-left: 4px solid {RobinhoodColors.SUCCESS_GREEN};
        position: relative;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.875rem;
    }}
    
    /* Sidebar widgets styling */
    section[data-testid="stSidebar"] .stSelectbox > div > div {{
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
        border: 1px solid rgba(209, 213, 219, 0.4);
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    }}
    
    section[data-testid="stSidebar"] .stMultiSelect > div > div {{
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
        border: 1px solid rgba(209, 213, 219, 0.4);
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    }}
    
    section[data-testid="stSidebar"] .stCheckbox {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 250, 252, 0.8) 100%);
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid rgba(209, 213, 219, 0.3);
        margin: 0.5rem 0;
    }}
    
    /* Sidebar button styling */
    section[data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        background: linear-gradient(135deg, {RobinhoodColors.SUCCESS_GREEN} 0%, #00A843 100%);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        padding: 0.875rem 1rem;
        margin: 0.75rem 0;
        box-shadow: 
            0 4px 6px rgba(0, 200, 83, 0.25),
            0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Inter', sans-serif;
    }}
    
    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: linear-gradient(135deg, #00A843 0%, {RobinhoodColors.SUCCESS_GREEN} 100%);
        box-shadow: 
            0 6px 12px rgba(0, 200, 83, 0.35),
            0 2px 4px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }}
    
    /* This is now handled in the sidebar section above */
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, {RobinhoodColors.SUCCESS_GREEN} 0%, #00A843 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 0.875rem 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 6px rgba(0, 200, 83, 0.25),
            0 1px 3px rgba(0, 0, 0, 0.08);
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #00A843 0%, {RobinhoodColors.SUCCESS_GREEN} 100%);
        box-shadow: 
            0 6px 12px rgba(0, 200, 83, 0.35),
            0 2px 4px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px) scale(1.05);
    }}
    
    .stButton > button:hover::before {{
        width: 300px;
        height: 300px;
    }}
    
    /* Progress Bar */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {RobinhoodColors.SUCCESS_GREEN} 0%, #00A843 100%);
        border-radius: 4px;
    }}
    
    /* Charts Container */
    .chart-container {{
        background: linear-gradient(135deg, #FFFFFF 0%, #FAFBFC 100%);
        border: 1px solid rgba(209, 213, 219, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.04),
            0 10px 15px rgba(0, 0, 0, 0.03);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }}
    
    .chart-container:hover {{
        box-shadow: 
            0 6px 12px rgba(0, 0, 0, 0.06),
            0 20px 30px rgba(0, 0, 0, 0.04);
        transform: translateY(-2px);
    }}
    
    .chart-title {{
        font-size: 1.25rem;
        font-weight: 600;
        color: {RobinhoodColors.PRIMARY_TEXT};
        margin: 0 0 1rem 0;
    }}
    
    /* Data Table */
    .dataframe {{
        border: none;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 
            0 1px 3px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(0, 0, 0, 0.03);
    }}
    
    .dataframe th {{
        background: linear-gradient(135deg, #F8F9FA 0%, #E5E7EB 100%);
        color: {RobinhoodColors.PRIMARY_TEXT};
        font-weight: 700;
        padding: 1.25rem;
        border-bottom: 2px solid {RobinhoodColors.BORDER_GRAY};
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
    }}
    
    .dataframe td {{
        padding: 0.75rem 1rem;
        border-bottom: 1px solid {RobinhoodColors.MEDIUM_GRAY};
    }}
    
    /* Severity Badges */
    .severity-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .severity-critical {{
        background-color: {RobinhoodColors.NEGATIVE_LIGHT};
        color: {RobinhoodColors.DANGER_RED};
    }}
    
    .severity-high {{
        background-color: #FFF3E0;
        color: #F57C00;
    }}
    
    .severity-medium {{
        background-color: #F3E5F5;
        color: {RobinhoodColors.CHART_PURPLE};
    }}
    
    .severity-low {{
        background-color: {RobinhoodColors.POSITIVE_LIGHT};
        color: {RobinhoodColors.SUCCESS_GREEN};
    }}
    
    /* Opportunity Score Indicators */
    .opportunity-score {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .score-high {{
        color: {RobinhoodColors.DANGER_RED};
        font-weight: 700;
    }}
    
    .score-medium {{
        color: #F57C00;
        font-weight: 600;
    }}
    
    .score-low {{
        color: {RobinhoodColors.SUCCESS_GREEN};
        font-weight: 600;
    }}
    
    /* Loading Animation */
    .loading-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        background: linear-gradient(135deg, rgba(0, 200, 83, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
        border-radius: 16px;
        margin: 2rem 0;
    }}
    
    .loading-spinner {{
        width: 32px;
        height: 32px;
        border: 3px solid transparent;
        border-top: 3px solid {RobinhoodColors.SUCCESS_GREEN};
        border-right: 3px solid {RobinhoodColors.CHART_PURPLE};
        border-radius: 50%;
        animation: spin 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Enhanced Filter Section */
    .filter-section {{
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
        border: 1px solid rgba(209, 213, 219, 0.4);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 2px 4px rgba(0, 0, 0, 0.04),
            inset 0 1px 0 rgba(255, 255, 255, 0.7);
        position: relative;
        backdrop-filter: blur(10px);
    }}
    
    .filter-section::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, {RobinhoodColors.SUCCESS_GREEN}, {RobinhoodColors.CHART_PURPLE});
        border-radius: 16px 16px 0 0;
    }}
    
    /* Alert Styling */
    .stAlert {{
        border-radius: 8px;
        border: none;
        font-family: 'Inter', sans-serif;
    }}
    
    .stSuccess {{
        background-color: {RobinhoodColors.POSITIVE_LIGHT};
        color: {RobinhoodColors.SUCCESS_GREEN};
    }}
    
    .stError {{
        background-color: {RobinhoodColors.NEGATIVE_LIGHT};
        color: {RobinhoodColors.DANGER_RED};
    }}
    
    /* Custom Spacing */
    .section-spacing {{
        margin: 2rem 0;
    }}
    
    .compact-spacing {{
        margin: 1rem 0;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def get_severity_color(severity):
    """Get color for severity level"""
    colors = {
        'Critical': RobinhoodColors.DANGER_RED,
        'High': '#F57C00',
        'Medium': RobinhoodColors.CHART_PURPLE,
        'Low': RobinhoodColors.SUCCESS_GREEN
    }
    return colors.get(severity, RobinhoodColors.SECONDARY_TEXT)

def get_opportunity_score_color(score):
    """Get color for opportunity score"""
    if score >= 7:
        return RobinhoodColors.DANGER_RED
    elif score >= 5:
        return '#F57C00'
    else:
        return RobinhoodColors.SUCCESS_GREEN

def format_metric_delta(value, total, is_percentage=False):
    """Format metric delta with appropriate styling"""
    if total == 0:
        return "0%"
    
    percentage = (value / total) * 100
    formatted = f"{percentage:.1f}%"
    
    return formatted

def get_chart_colors():
    """Get consistent color palette for charts"""
    return {
        'primary': RobinhoodColors.SUCCESS_GREEN,
        'secondary': RobinhoodColors.DANGER_RED,
        'tertiary': RobinhoodColors.CHART_PURPLE,
        'quaternary': '#F57C00',
        'neutral': RobinhoodColors.SECONDARY_TEXT,
        'background': RobinhoodColors.LIGHT_GRAY,
        'grid': RobinhoodColors.MEDIUM_GRAY
    }