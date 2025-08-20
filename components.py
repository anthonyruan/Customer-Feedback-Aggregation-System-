import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from styles import RobinhoodColors, get_severity_color, get_opportunity_score_color, get_chart_colors

def render_robinhood_header():
    """Render the main header with Robinhood-inspired design"""
    st.markdown("""
    <div class="robinhood-header">
        <div style="position: relative; z-index: 1;">
            <h1 class="header-title">
                <span style="font-size: 3.5rem;">📊</span> Customer Feedback Analytics
            </h1>
            <p class="header-subtitle">AI-powered strategic insights and opportunity ranking for Product Managers</p>
            <div style="margin-top: 1rem;">
                <span style="display: inline-block; padding: 0.25rem 0.75rem; background: rgba(0, 200, 83, 0.1); border-radius: 20px; font-size: 0.875rem; color: #00C853; font-weight: 600; margin-right: 0.5rem;">✨ Real-time Analysis</span>
                <span style="display: inline-block; padding: 0.25rem 0.75rem; background: rgba(139, 92, 246, 0.1); border-radius: 20px; font-size: 0.875rem; color: #8B5CF6; font-weight: 600; margin-right: 0.5rem;">🎯 Strategic Insights</span>
                <span style="display: inline-block; padding: 0.25rem 0.75rem; background: rgba(30, 64, 175, 0.1); border-radius: 20px; font-size: 0.875rem; color: #1E40AF; font-weight: 600;">📈 Opportunity Scoring</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(label, value, delta=None, delta_type="neutral", help_text=None, icon="📊"):
    """Render a financial-style metric card using Streamlit native components"""
    
    # Determine delta styling and colors
    delta_color = None
    if delta_type == "positive":
        delta_color = "normal"
    elif delta_type == "negative":
        delta_color = "inverse"
    else:
        delta_color = "off"
    
    # Create a styled container
    with st.container():
        # Icon and value row
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<div style='font-size: 2rem; text-align: center; padding: 0.5rem;'>{icon}</div>", unsafe_allow_html=True)
        with col2:
            st.metric(
                label=label,
                value=value,
                delta=delta,
                delta_color=delta_color,
                help=help_text
            )

def create_robinhood_donut_chart(data, title, names_col, values_col):
    """Create a Robinhood-style donut chart"""
    colors = get_chart_colors()
    
    # Create color palette based on data
    color_sequence = [colors['primary'], colors['secondary'], colors['tertiary'], colors['quaternary']]
    
    fig = go.Figure(data=[go.Pie(
        labels=data[names_col],
        values=data[values_col],
        hole=.6,
        marker=dict(
            colors=color_sequence[:len(data)],
            line=dict(color=colors['background'], width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(
            family="Inter, sans-serif",
            size=12,
            color=RobinhoodColors.PRIMARY_TEXT
        )
    )])
    
    # Calculate total for center display
    total = data[values_col].sum()
    
    fig.add_annotation(
        text=f"<b>{total}</b><br><span style='font-size:14px;color:{RobinhoodColors.SECONDARY_TEXT}'>Total</span>",
        x=0.5, y=0.5,
        font_size=24,
        font_color=RobinhoodColors.PRIMARY_TEXT,
        font_family="Inter, sans-serif",
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(
                family="Inter, sans-serif",
                size=16,
                color=RobinhoodColors.PRIMARY_TEXT
            ),
            x=0.5
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(
                family="Inter, sans-serif",
                size=11,
                color=RobinhoodColors.SECONDARY_TEXT
            )
        ),
        margin=dict(t=50, b=80, l=20, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig

def create_robinhood_bar_chart(data, title, x_col, y_col, orientation='h'):
    """Create a Robinhood-style bar chart"""
    colors = get_chart_colors()
    
    if orientation == 'h':
        fig = px.bar(
            data, 
            x=x_col, 
            y=y_col,
            orientation='h',
            color=x_col,
            color_discrete_sequence=[colors['primary'], colors['secondary'], colors['tertiary']]
        )
        
        fig.update_layout(
            xaxis_title="Number of Items",
            yaxis_title="Category"
        )
    else:
        fig = px.bar(
            data,
            x=x_col,
            y=y_col,
            color=x_col,
            color_discrete_sequence=[colors['primary'], colors['secondary'], colors['tertiary']]
        )
        
        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Number of Items"
        )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(
                family="Inter, sans-serif",
                size=16,
                color=RobinhoodColors.PRIMARY_TEXT
            ),
            x=0.5
        ),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=50, l=50, r=50),
        height=400,
        font=dict(
            family="Inter, sans-serif",
            color=RobinhoodColors.PRIMARY_TEXT
        ),
        xaxis=dict(
            gridcolor=RobinhoodColors.MEDIUM_GRAY,
            gridwidth=1,
            zeroline=False
        ),
        yaxis=dict(
            gridcolor=RobinhoodColors.MEDIUM_GRAY,
            gridwidth=1,
            zeroline=False
        )
    )
    
    # Update bar styling
    fig.update_traces(
        marker_line_width=0,
        opacity=0.9,
        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>' if orientation == 'h' else '<b>%{x}</b><br>Count: %{y}<extra></extra>'
    )
    
    return fig

def create_opportunity_trend_chart(data):
    """Create a trend chart for opportunity scores"""
    colors = get_chart_colors()
    
    # Group by opportunity score and count
    score_counts = data['Opportunity_Score'].value_counts().sort_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=score_counts.index,
        y=score_counts.values,
        mode='lines+markers',
        line=dict(
            color=colors['primary'],
            width=3,
            shape='spline'
        ),
        marker=dict(
            color=colors['primary'],
            size=8,
            line=dict(color='white', width=2)
        ),
        fill='tonexty',
        fillcolor=f"rgba(0, 200, 83, 0.1)",
        name="Opportunity Score Distribution"
    ))
    
    fig.update_layout(
        title=dict(
            text="Opportunity Score Distribution",
            font=dict(
                family="Inter, sans-serif",
                size=16,
                color=RobinhoodColors.PRIMARY_TEXT
            ),
            x=0.5
        ),
        xaxis=dict(
            title="Opportunity Score",
            gridcolor=RobinhoodColors.MEDIUM_GRAY,
            gridwidth=1,
            zeroline=False,
            tickfont=dict(family="Inter, sans-serif", color=RobinhoodColors.PRIMARY_TEXT)
        ),
        yaxis=dict(
            title="Number of Items",
            gridcolor=RobinhoodColors.MEDIUM_GRAY,
            gridwidth=1,
            zeroline=False,
            tickfont=dict(family="Inter, sans-serif", color=RobinhoodColors.PRIMARY_TEXT)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=50, l=50, r=50),
        height=300,
        showlegend=False,
        font=dict(
            family="Inter, sans-serif",
            color=RobinhoodColors.PRIMARY_TEXT
        )
    )
    
    return fig

def render_severity_badge(severity):
    """Render a severity badge with appropriate styling"""
    severity_lower = severity.lower()
    badge_html = f'<span class="severity-badge severity-{severity_lower}">{severity}</span>'
    return badge_html

def render_opportunity_score(score):
    """Render opportunity score with color coding"""
    score_class = "score-low"
    if score >= 7:
        score_class = "score-high"
    elif score >= 5:
        score_class = "score-medium"
    
    score_html = f'<span class="opportunity-score {score_class}"><strong>{score}</strong></span>'
    return score_html

def render_sidebar_header(title, icon="🔧"):
    """Render enhanced sidebar section header with icon and modern styling"""
    st.markdown(f'''
    <div class="sidebar-header">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="width: 32px; height: 32px; 
                       background: linear-gradient(135deg, {RobinhoodColors.SUCCESS_GREEN} 0%, {RobinhoodColors.CHART_PURPLE} 100%);
                       border-radius: 8px; 
                       display: flex; 
                       align-items: center; 
                       justify-content: center; 
                       font-size: 1rem;
                       color: white;
                       box-shadow: 0 2px 4px rgba(0, 200, 83, 0.3);">
                {icon}
            </div>
            <span style="flex: 1;">{title}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_sidebar_info_card(title, description, icon="💡", bg_color="rgba(30, 64, 175, 0.05)", border_color="#1E40AF"):
    """Render an info card in the sidebar"""
    st.markdown(f'''
    <div style="background: {bg_color}; 
                border-left: 3px solid {border_color}; 
                padding: 1rem; 
                border-radius: 12px; 
                margin: 1rem 0;
                font-size: 0.875rem;
                color: #374151;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);">
        <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
            <span style="font-size: 1.25rem;">{icon}</span>
            <div>
                <div style="font-weight: 600; color: {RobinhoodColors.PRIMARY_TEXT}; margin-bottom: 0.25rem;">{title}</div>
                <div>{description}</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_chart_container(chart_fig, title=None):
    """Render a chart within a styled container"""
    container_html = '<div class="chart-container">'
    if title:
        container_html += f'<h3 class="chart-title">{title}</h3>'
    
    st.markdown(container_html, unsafe_allow_html=True)
    st.plotly_chart(chart_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_loading_spinner(text="Processing..."):
    """Render a Robinhood-style loading spinner"""
    loading_html = f"""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <span style="margin-left: 1rem; color: {RobinhoodColors.SECONDARY_TEXT};">{text}</span>
    </div>
    """
    return st.markdown(loading_html, unsafe_allow_html=True)

def create_metrics_overview_section(stats):
    """Create the complete metrics overview section with Robinhood styling"""
    st.markdown('<div class="section-spacing">', unsafe_allow_html=True)
    
    # Add a subtle gradient background for the metrics section
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(0, 200, 83, 0.02) 0%, rgba(139, 92, 246, 0.02) 100%); 
                border-radius: 20px; padding: 1.5rem; margin-bottom: 1.5rem;">
        <h4 style="color: #374151; font-family: Inter, sans-serif; font-weight: 600; margin: 0 0 1rem 0; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.7;">KEY PERFORMANCE INDICATORS</h4>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            label="Total Feedback",
            value=str(stats['total_feedback']),
            delta_type="neutral",
            help_text="All feedback items in dataset",
            icon="📝"
        )
    
    with col2:
        critical_percentage = (stats['critical_issues'] / stats['total_feedback'] * 100) if stats['total_feedback'] > 0 else 0
        render_metric_card(
            label="Critical Issues",
            value=str(stats['critical_issues']),
            delta=f"{critical_percentage:.1f}%",
            delta_type="negative" if critical_percentage > 25 else "neutral",
            help_text="High-priority issues requiring immediate attention",
            icon="🚨"
        )
    
    with col3:
        compliance_percentage = (stats['compliance_issues'] / stats['total_feedback'] * 100) if stats['total_feedback'] > 0 else 0
        render_metric_card(
            label="Compliance Issues",
            value=str(stats['compliance_issues']),
            delta=f"{compliance_percentage:.1f}%",
            delta_type="negative" if compliance_percentage > 20 else "neutral",
            help_text="Regulatory and data compliance concerns",
            icon="⚖️"
        )
    
    with col4:
        avg_score = stats['avg_opportunity_score']
        render_metric_card(
            label="Avg Opportunity Score",
            value=f"{avg_score:.1f}",
            delta_type="positive" if avg_score >= 6 else "negative" if avg_score <= 4 else "neutral",
            help_text="Average priority score (3-8 scale)",
            icon="🎯"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

def style_dataframe_robinhood(df):
    """Apply Robinhood-inspired styling to a dataframe"""
    
    def severity_styler(val):
        color = get_severity_color(val)
        return f'background-color: {color}15; color: {color}; font-weight: 600;'
    
    def score_styler(val):
        color = get_opportunity_score_color(val)
        return f'background-color: {color}15; color: {color}; font-weight: 600;'
    
    def category_styler(val):
        colors = get_chart_colors()
        if "Enterprise" in val:
            color = colors['primary']
        elif "Compliance" in val:
            color = colors['secondary']
        else:
            color = colors['tertiary']
        return f'background-color: {color}15; color: {color}; font-weight: 500;'
    
    styled_df = df.style
    
    if 'Severity' in df.columns:
        styled_df = styled_df.applymap(severity_styler, subset=['Severity'])
    
    if 'Opportunity_Score' in df.columns:
        styled_df = styled_df.applymap(score_styler, subset=['Opportunity_Score'])
    
    if 'AI_Category' in df.columns:
        styled_df = styled_df.applymap(category_styler, subset=['AI_Category'])
    
    return styled_df