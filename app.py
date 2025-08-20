import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_processor import DataProcessor
from ai_analyzer import AIAnalyzer
from styles import inject_robinhood_css, RobinhoodColors
from components import (
    render_robinhood_header, render_metric_card, create_robinhood_donut_chart,
    create_robinhood_bar_chart, create_opportunity_trend_chart, render_sidebar_header,
    render_chart_container, render_loading_spinner, create_metrics_overview_section,
    style_dataframe_robinhood, render_sidebar_info_card
)

st.set_page_config(
    page_title="Customer Feedback Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Robinhood-inspired CSS styling
inject_robinhood_css()

def initialize_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'ai_processed' not in st.session_state:
        st.session_state.ai_processed = False
    
    # Enhanced sidebar with info cards and styling
    with st.sidebar:
        render_sidebar_info_card(
            "Quick Actions",
            "Reset all data to start fresh with new analysis.",
            "🔄",
            "rgba(139, 92, 246, 0.05)",
            "#8B5CF6"
        )
        
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        if st.button("🔄 Reset All Data", help="Clear all cached data and start fresh"):
            st.session_state.data = None
            st.session_state.processed_data = None
            st.session_state.ai_processed = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def load_data():
    data_processor = DataProcessor()
    
    render_sidebar_header("Data Input", "📁")
    
    use_sample_data = st.sidebar.checkbox("Use Sample Data", value=True)
    
    if use_sample_data:
        if st.sidebar.button("Load Sample Data"):
            with st.spinner("Loading sample data..."):
                # Clear ALL session state to ensure fresh start
                st.session_state.data = None
                st.session_state.processed_data = None
                st.session_state.ai_processed = False
                
                df = data_processor.create_sample_data()
                st.session_state.data = df
                st.success(f"✅ Sample data loaded! {len(df)} rows ready for analysis")
                st.info("👉 Click 'Process with AI' to categorize feedback")
                
                # Add data overview in sidebar
                with st.sidebar:
                    render_sidebar_info_card(
                        "Data Overview",
                        f"Loaded {len(df)} feedback items with {len(df['Product'].unique())} products across {len(df['Region'].unique())} regions.",
                        "📈",
                        "rgba(0, 200, 83, 0.05)",
                        "#00C853"
                    )
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload CSV file", 
            type=['csv'],
            help="CSV should contain columns: Feedback, Product, Severity, Region"
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing uploaded file..."):
                df = data_processor.load_uploaded_file(uploaded_file)
                if not df.empty:
                    df = data_processor.calculate_opportunity_score(df)
                    st.session_state.data = df
                    st.session_state.ai_processed = False
                    st.success(f"✅ Loaded {len(df)} feedback items successfully!")

def process_with_ai():
    if st.session_state.data is None:
        st.warning("⚠️ Please load data first.")
        return
    
    st.markdown('<div class="section-spacing">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #111418; font-family: Inter, sans-serif; font-weight: 600;">🤖 AI Processing</h3>', unsafe_allow_html=True)
    
    # Add option to force sample data
    use_sample_ai = st.checkbox("Force use sample AI data (ignore API)", value=False, 
                                 help="Check this to use pre-defined sample AI categorization instead of calling OpenAI API")
    
    ai_analyzer = AIAnalyzer()
    
    # Override client if user wants to force sample data
    if use_sample_ai:
        ai_analyzer.client = None
        st.info("🔧 Using sample AI data as requested.")
    elif not ai_analyzer.is_configured():
        st.warning("⚙️ OpenAI API not configured. Using sample AI data.")
    
    if st.button("🚀 Process with AI", type="primary"):
        progress_container = st.empty()
        
        with progress_container:
            render_loading_spinner("Processing feedback with AI...")
        
        # Clear old processed data
        st.session_state.processed_data = None
        
        processed_df = ai_analyzer.process_batch(st.session_state.data)
        st.session_state.processed_data = processed_df
        st.session_state.ai_processed = True
        
        progress_container.empty()
        
        # Show completion message with category breakdown
        if 'AI_Category' in processed_df.columns:
            unique_categories = processed_df['AI_Category'].unique()
            category_counts = processed_df['AI_Category'].value_counts()
            
            st.success(f"✅ AI processing completed! Categorized {len(processed_df)} items into {len(unique_categories)} strategic priorities")
            
            # Show category breakdown in a clean format
            col1, col2, col3 = st.columns(3)
            for i, (cat, count) in enumerate(category_counts.items()):
                with [col1, col2, col3][i % 3]:
                    st.metric(label=cat.split()[-2:][0] if len(cat.split()) > 2 else cat, value=count)
        else:
            st.success("✅ AI processing completed!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_filters():
    if st.session_state.processed_data is None:
        return {}
    
    # IMPORTANT: Use the full unfiltered data for filter options
    df = st.session_state.processed_data
    
    render_sidebar_header("Smart Filters", "🎛️")
    
    # Add filter tips and information
    with st.sidebar:
        render_sidebar_info_card(
            "Pro Tip", 
            "Use multiple filters to drill down into specific feedback segments for targeted insights.",
            "💡",
            "rgba(30, 64, 175, 0.05)",
            "#1E40AF"
        )
    st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
    
    # Show available categories for user information
    all_categories = df['AI_Category'].unique().tolist() if 'AI_Category' in df.columns else []
    
    # Get all unique values from the FULL dataset for filter options
    categories = st.sidebar.multiselect(
        "Strategic Priority",
        options=df['AI_Category'].unique() if 'AI_Category' in df.columns else [],
        default=df['AI_Category'].unique() if 'AI_Category' in df.columns else []
    )
    
    products = st.sidebar.multiselect(
        "Product/Module",
        options=df['Product'].unique() if 'Product' in df.columns else [],
        default=df['Product'].unique() if 'Product' in df.columns else []
    )
    
    severities = st.sidebar.multiselect(
        "Severity Level", 
        options=df['Severity'].unique() if 'Severity' in df.columns else [],
        default=df['Severity'].unique() if 'Severity' in df.columns else []
    )
    
    regions = st.sidebar.multiselect(
        "Region",
        options=df['Region'].unique() if 'Region' in df.columns else [], 
        default=df['Region'].unique() if 'Region' in df.columns else []
    )
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'categories': categories,
        'products': products,
        'severities': severities,
        'regions': regions
    }

def display_metrics(df):
    data_processor = DataProcessor()
    stats = data_processor.get_summary_stats(df)
    
    # Use the new Robinhood-style metrics overview
    create_metrics_overview_section(stats)

def create_visualizations(df):
    if df.empty:
        st.warning("⚠️ No data to display.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Strategic Category Bar Chart
        category_counts = df['AI_Category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        
        fig_bar = create_robinhood_bar_chart(
            category_counts,
            "📊 Feedback by Strategic Priority",
            'Count',
            'Category'
        )
        render_chart_container(fig_bar)
    
    with col2:
        # Severity Donut Chart
        severity_counts = df['Severity'].value_counts().reset_index()
        severity_counts.columns = ['Severity', 'Count']
        
        fig_donut = create_robinhood_donut_chart(
            severity_counts,
            "🎯 Severity Distribution",
            'Severity',
            'Count'
        )
        render_chart_container(fig_donut)
    
    # Add opportunity score trend chart
    if 'Opportunity_Score' in df.columns:
        st.markdown('<div class="section-spacing">', unsafe_allow_html=True)
        trend_fig = create_opportunity_trend_chart(df)
        render_chart_container(trend_fig, "📈 Opportunity Score Trends")
        st.markdown('</div>', unsafe_allow_html=True)

def display_data_table(df):
    if df.empty:
        st.warning("⚠️ No data matches the current filters.")
        return
    
    st.markdown('<div class="section-spacing">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #111418; font-family: Inter, sans-serif; font-weight: 600; margin-bottom: 1rem;">📋 Detailed Feedback Analysis</h3>', unsafe_allow_html=True)
    
    display_columns = [
        'Feedback', 'AI_Category', 'AI_Summary', 'Product', 
        'Severity', 'Region', 'Opportunity_Score'
    ]
    
    available_columns = [col for col in display_columns if col in df.columns]
    
    # Apply Robinhood-style dataframe styling
    filtered_df = df[available_columns].copy()
    styled_df = style_dataframe_robinhood(filtered_df)
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400
    )
    
    # Download section with better styling
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📥 Download Filtered Data", use_container_width=True):
            csv = df[available_columns].to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name="filtered_feedback_data.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    initialize_session_state()
    
    # Render the Robinhood-inspired header
    render_robinhood_header()
    
    load_data()
    
    if st.session_state.data is not None:
        process_with_ai()
        
        if st.session_state.ai_processed and st.session_state.processed_data is not None:
            filters = create_filters()
            
            data_processor = DataProcessor()
            filtered_df = data_processor.filter_data(st.session_state.processed_data, filters)
            
            # Executive Dashboard Header with enhanced styling
            st.markdown('''
            <div style="background: linear-gradient(90deg, rgba(0, 200, 83, 0.03) 0%, rgba(139, 92, 246, 0.03) 50%, rgba(30, 64, 175, 0.03) 100%);
                        padding: 1.5rem;
                        border-radius: 16px;
                        margin: 2rem 0 1.5rem 0;
                        border: 1px solid rgba(209, 213, 219, 0.2);">
                <h2 style="color: #111418; font-family: Inter, sans-serif; font-weight: 800; margin: 0;">
                    <span style="font-size: 2rem;">📈</span> Executive Dashboard
                </h2>
                <p style="color: #6b7280; margin: 0.5rem 0 0 0; font-family: Inter, sans-serif;">Real-time strategic insights from customer feedback analysis</p>
            </div>
            ''', unsafe_allow_html=True)
            display_metrics(filtered_df)
            
            # Strategic Analytics Header with enhanced styling
            st.markdown('''
            <div style="background: linear-gradient(90deg, rgba(139, 92, 246, 0.03) 0%, rgba(0, 200, 83, 0.03) 50%, rgba(245, 124, 0, 0.03) 100%);
                        padding: 1.5rem;
                        border-radius: 16px;
                        margin: 2rem 0 1.5rem 0;
                        border: 1px solid rgba(209, 213, 219, 0.2);">
                <h2 style="color: #111418; font-family: Inter, sans-serif; font-weight: 800; margin: 0;">
                    <span style="font-size: 2rem;">📊</span> Strategic Analytics
                </h2>
                <p style="color: #6b7280; margin: 0.5rem 0 0 0; font-family: Inter, sans-serif;">Visual breakdown of feedback categories and opportunity distribution</p>
            </div>
            ''', unsafe_allow_html=True)
            create_visualizations(filtered_df)
            
            display_data_table(filtered_df)
        
        elif not st.session_state.ai_processed:
            # Enhanced info card with gradient background
            st.markdown('''
            <div style="background: linear-gradient(135deg, rgba(30, 64, 175, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%); 
                        border-left: 4px solid #1E40AF; 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        margin: 2rem 0;">
                <h4 style="color: #1E40AF; margin: 0 0 0.5rem 0; font-family: Inter, sans-serif;">📊 Data Loaded Successfully!</h4>
                <p style="color: #374151; margin: 0; font-family: Inter, sans-serif;">Click <strong>'Process with AI'</strong> above to unlock the executive dashboard with strategic insights.</p>
            </div>
            ''', unsafe_allow_html=True)
    
    else:
        # Welcome section with Robinhood styling
        st.markdown('''
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e5e7eb 100%); padding: 2rem; border-radius: 12px; border: 1px solid #d1d5db; margin: 2rem 0;">
            <h3 style="color: #111418; font-family: Inter, sans-serif; font-weight: 600; margin: 0 0 1rem 0;">👈 Get Started</h3>
            <p style="color: #6b7280; font-family: Inter, sans-serif; margin: 0;">Load data using the sidebar to unlock your AI-powered feedback analytics dashboard.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('''
            <div class="chart-container">
                <h4 style="color: #111418; font-family: Inter, sans-serif; font-weight: 600;">🚀 Quick Start Guide</h4>
                <ol style="color: #374151; font-family: Inter, sans-serif; line-height: 1.8;">
                    <li><strong>Load Data</strong>: Use sample data or upload your CSV file</li>
                    <li><strong>AI Processing</strong>: Let AI categorize and analyze feedback</li>
                    <li><strong>Explore Insights</strong>: Use filters for strategic analysis</li>
                    <li><strong>Export Results</strong>: Download insights for stakeholders</li>
                </ol>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown('''
            <div class="chart-container">
                <h4 style="color: #111418; font-family: Inter, sans-serif; font-weight: 600;">📋 CSV Requirements</h4>
                <div style="color: #374151; font-family: Inter, sans-serif; line-height: 1.6;">
                    <p><strong>Required columns:</strong></p>
                    <ul>
                        <li><code>Feedback</code>: Customer feedback text</li>
                        <li><code>Product</code>: Product or module name</li>
                        <li><code>Severity</code>: Critical, High, Medium, or Low</li>
                        <li><code>Region</code>: US, EU, APAC, or LATAM</li>
                    </ul>
                    <p><em>Optional:</em> <code>Category</code> for validation</p>
                </div>
            </div>
            ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()