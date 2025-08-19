import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_processor import DataProcessor
from ai_analyzer import AIAnalyzer

st.set_page_config(
    page_title="Customer Feedback Aggregation System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'ai_processed' not in st.session_state:
        st.session_state.ai_processed = False
    
    # Add a reset button in sidebar
    if st.sidebar.button("🔄 Reset All Data", help="Clear all cached data and start fresh"):
        st.session_state.data = None
        st.session_state.processed_data = None
        st.session_state.ai_processed = False
        st.rerun()

def load_data():
    data_processor = DataProcessor()
    
    st.sidebar.header("📁 Data Input")
    
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
                st.success(f"Sample data loaded successfully! {len(df)} rows with categories: {df['Category'].unique().tolist()}")
                st.info("Now click 'Process with AI' to analyze the feedback")
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
                    st.success(f"Loaded {len(df)} feedback items successfully!")

def process_with_ai():
    if st.session_state.data is None:
        st.warning("Please load data first.")
        return
    
    ai_analyzer = AIAnalyzer()
    
    if not ai_analyzer.is_configured():
        st.error("OpenAI API not configured. Please check your .env file.")
        st.info("Using sample AI data for demonstration.")
        
    st.subheader("🤖 AI Processing")
    
    if st.button("Process with AI", type="primary"):
        with st.spinner("Processing feedback with AI..."):
            # Clear old processed data
            st.session_state.processed_data = None
            
            processed_df = ai_analyzer.process_batch(st.session_state.data)
            
            # Debug: Check what we received
            st.write("DEBUG after process_batch returned:")
            st.write(f"  - DataFrame shape: {processed_df.shape}")
            st.write(f"  - Columns: {processed_df.columns.tolist()}")
            
            if 'AI_Category' in processed_df.columns:
                st.write("  - AI_Category first 10 values:")
                for i in range(min(10, len(processed_df))):
                    st.write(f"    Row {i}: {processed_df.iloc[i]['AI_Category']}")
            
            st.session_state.processed_data = processed_df
            st.session_state.ai_processed = True
            
            # Debug info
            if 'AI_Category' in processed_df.columns:
                unique_categories = processed_df['AI_Category'].unique()
                category_counts = processed_df['AI_Category'].value_counts()
                st.success(f"AI processing completed! Found {len(unique_categories)} categories:")
                for cat in unique_categories:
                    count = category_counts.get(cat, 0)
                    st.write(f"- {cat}: {count} items")
            else:
                st.success("AI processing completed!")

def create_filters():
    if st.session_state.processed_data is None:
        return {}
    
    # IMPORTANT: Use the full unfiltered data for filter options
    df = st.session_state.processed_data
    
    st.sidebar.header("🔍 Filters")
    
    # Debug: Show what categories are available in the FULL dataset
    all_categories = df['AI_Category'].unique().tolist() if 'AI_Category' in df.columns else []
    if all_categories:
        st.sidebar.info(f"Available categories: {all_categories}")
    
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
    
    return {
        'categories': categories,
        'products': products,
        'severities': severities,
        'regions': regions
    }

def display_metrics(df):
    data_processor = DataProcessor()
    stats = data_processor.get_summary_stats(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Feedback",
            value=stats['total_feedback']
        )
    
    with col2:
        st.metric(
            label="Critical Issues", 
            value=stats['critical_issues'],
            delta=f"{stats['critical_issues']/stats['total_feedback']*100:.1f}%" if stats['total_feedback'] > 0 else "0%"
        )
    
    with col3:
        st.metric(
            label="Compliance Issues",
            value=stats['compliance_issues'],
            delta=f"{stats['compliance_issues']/stats['total_feedback']*100:.1f}%" if stats['total_feedback'] > 0 else "0%"
        )
    
    with col4:
        st.metric(
            label="Avg Opportunity Score",
            value=f"{stats['avg_opportunity_score']:.1f}"
        )

def create_visualizations(df):
    if df.empty:
        st.warning("No data to display.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Feedback by Strategic Category")
        category_counts = df['AI_Category'].value_counts()
        
        # Debug: Show category counts
        st.write(f"Category distribution: {category_counts.to_dict()}")
        
        fig_bar = px.bar(
            x=category_counts.values,
            y=category_counts.index,
            orientation='h',
            labels={'x': 'Number of Feedback Items', 'y': 'Strategic Category'},
            color=category_counts.values,
            color_continuous_scale='viridis'
        )
        fig_bar.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Severity Distribution")
        severity_counts = df['Severity'].value_counts()
        fig_pie = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

def display_data_table(df):
    if df.empty:
        st.warning("No data matches the current filters.")
        return
    
    st.subheader("📋 Feedback Data")
    
    display_columns = [
        'Feedback', 'AI_Category', 'AI_Summary', 'Product', 
        'Severity', 'Region', 'Opportunity_Score'
    ]
    
    available_columns = [col for col in display_columns if col in df.columns]
    
    styled_df = df[available_columns].copy()
    
    def color_severity(val):
        if val == 'Critical':
            return 'background-color: #ffebee'
        elif val == 'High':
            return 'background-color: #fff3e0'
        elif val == 'Medium':
            return 'background-color: #f3e5f5'
        else:
            return 'background-color: #e8f5e8'
    
    def color_score(val):
        if val >= 7:
            return 'background-color: #ffcdd2'
        elif val >= 5:
            return 'background-color: #ffe0b2'
        else:
            return 'background-color: #c8e6c9'
    
    # Apply styling properly by chaining styles correctly
    styler = styled_df.style
    
    if 'Severity' in styled_df.columns:
        styler = styler.applymap(color_severity, subset=['Severity'])
    
    if 'Opportunity_Score' in styled_df.columns:
        styler = styler.applymap(color_score, subset=['Opportunity_Score'])
    
    styled_df = styler
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400
    )
    
    if st.button("📥 Download Filtered Data"):
        csv = df[available_columns].to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_feedback_data.csv",
            mime="text/csv"
        )

def main():
    initialize_session_state()
    
    st.title("📊 Customer Feedback Aggregation System")
    st.markdown("AI-powered strategic analysis and opportunity ranking for Product Managers")
    
    load_data()
    
    if st.session_state.data is not None:
        process_with_ai()
        
        if st.session_state.ai_processed and st.session_state.processed_data is not None:
            filters = create_filters()
            
            data_processor = DataProcessor()
            filtered_df = data_processor.filter_data(st.session_state.processed_data, filters)
            
            st.header("📈 Dashboard Overview")
            display_metrics(filtered_df)
            
            st.header("📊 Analytics")
            create_visualizations(filtered_df)
            
            display_data_table(filtered_df)
        
        elif not st.session_state.ai_processed:
            st.info("Data loaded. Click 'Process with AI' to analyze feedback and enable the dashboard.")
    
    else:
        st.info("👈 Please load data using the sidebar to get started.")
        
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Load Data**: Use sample data or upload your own CSV file
        2. **AI Processing**: Let AI categorize and summarize your feedback
        3. **Explore**: Use filters to dive deep into specific insights
        4. **Export**: Download filtered results for further analysis
        
        ### 📋 Required CSV Format
        Your CSV file should contain these columns:
        - `Feedback`: Customer feedback text
        - `Product`: Product or module name  
        - `Severity`: Critical, High, Medium, or Low
        - `Region`: US, EU, APAC, or LATAM
        - `Category`: (Optional) Human-assigned category for validation
        """)

if __name__ == "__main__":
    main()