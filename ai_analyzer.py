import openai
import pandas as pd
import streamlit as st
import time
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    
    STRATEGIC_CATEGORIES = [
        "Win Enterprise Deals",
        "Ensure Regulatory & Data Compliance", 
        "Improve Platform Usability & Performance"
    ]
    
    def __init__(self):
        self.client = None
        self._setup_openai()
    
    def _setup_openai(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            st.error("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
            return
        
        try:
            self.client = openai.OpenAI(api_key=api_key)
        except Exception as e:
            st.error(f"Error setting up OpenAI client: {str(e)}")
    
    def categorize_feedback(self, feedback_text: str, max_retries: int = 3) -> str:
        if not self.client:
            return "Error: OpenAI not configured"
        
        prompt = f"""
You are an AI assistant for a financial software company. Your task is to categorize customer feedback into one of three strategic priorities based on the content and business impact.

Categories:
1. "Win Enterprise Deals" - Features, integrations, or capabilities needed to attract and close large enterprise customers
2. "Ensure Regulatory & Data Compliance" - Security, privacy, regulatory compliance, data governance, and audit requirements  
3. "Improve Platform Usability & Performance" - User experience, performance optimization, stability, and general usability improvements

Instructions:
- Read the feedback carefully and identify the primary business concern
- Choose the category that best aligns with the core issue described
- Respond with ONLY the category name (exactly as written above)
- If multiple categories apply, choose the most critical one based on business impact

Feedback: "{feedback_text}"

Category:"""

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a business analyst specializing in product feedback categorization."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50,
                    temperature=0.1
                )
                
                category = response.choices[0].message.content.strip()
                
                if category in self.STRATEGIC_CATEGORIES:
                    return category
                else:
                    return "Improve Platform Usability & Performance"
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    st.error(f"Error categorizing feedback: {str(e)}")
                    return "Improve Platform Usability & Performance"
    
    def generate_summary(self, feedback_text: str, max_retries: int = 3) -> str:
        if not self.client:
            return "Error: OpenAI not configured"
        
        prompt = f"""
You are an AI assistant helping Product Managers quickly understand customer feedback. 

Your task: Create a concise, one-sentence executive summary that captures the core problem or request.

Requirements:
- Maximum 25 words
- Focus on the specific issue or need, not generic descriptions
- Use business-friendly language suitable for executive dashboards
- Highlight the impact or urgency if mentioned
- Be specific about what the customer needs or what's broken

Feedback: "{feedback_text}"

Executive Summary:"""

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a product management assistant specializing in concise business communication."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=60,
                    temperature=0.1
                )
                
                summary = response.choices[0].message.content.strip()
                return summary
                
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    st.error(f"Error generating summary: {str(e)}")
                    return "Unable to generate summary"
    
    def process_batch(self, df: pd.DataFrame, show_progress: bool = True) -> pd.DataFrame:
        if not self.client:
            st.info("OpenAI API not configured. Using sample AI data for demonstration.")
            
            # Show progress bar even for sample data
            if show_progress:
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_text.text('Generating sample AI categorization...')
                progress_bar.progress(0.5)
            
            result = self._add_sample_ai_data(df)
            
            if show_progress:
                progress_bar.progress(1.0)
                status_text.text('Sample AI processing complete!')
                time.sleep(0.5)  # Brief pause to show completion
            
            return result
        
        df_copy = df.copy()
        total_rows = len(df_copy)
        
        if show_progress:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        ai_categories = []
        ai_summaries = []
        
        for idx, row in df_copy.iterrows():
            if show_progress:
                progress = (idx + 1) / total_rows
                progress_bar.progress(progress)
                status_text.text(f'Processing feedback {idx + 1} of {total_rows}...')
            
            category = self.categorize_feedback(row['Feedback'])
            summary = self.generate_summary(row['Feedback'])
            
            ai_categories.append(category)
            ai_summaries.append(summary)
            
            time.sleep(0.5)
        
        df_copy['AI_Category'] = ai_categories
        df_copy['AI_Summary'] = ai_summaries
        
        if show_progress:
            progress_bar.progress(1.0)
            status_text.text('AI processing complete!')
        
        return df_copy
    
    def _add_sample_ai_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        
        # Directly assign categories to ensure all three are present
        # For 10 rows: 3 Win Enterprise, 3 Compliance, 4 Usability
        if len(df_copy) == 10:
            # Explicit assignment for exactly 10 rows
            df_copy['AI_Category'] = [
                "Win Enterprise Deals",                      # Row 0
                "Ensure Regulatory & Data Compliance",       # Row 1  
                "Improve Platform Usability & Performance",  # Row 2
                "Win Enterprise Deals",                      # Row 3
                "Improve Platform Usability & Performance",  # Row 4
                "Win Enterprise Deals",                      # Row 5
                "Improve Platform Usability & Performance",  # Row 6
                "Ensure Regulatory & Data Compliance",       # Row 7
                "Ensure Regulatory & Data Compliance",       # Row 8
                "Improve Platform Usability & Performance"   # Row 9
            ]
        else:
            # For other row counts, cycle through categories
            sample_categories = [
                "Win Enterprise Deals",
                "Ensure Regulatory & Data Compliance",
                "Improve Platform Usability & Performance"
            ]
            num_rows = len(df_copy)
            categories_to_assign = []
            for i in range(num_rows):
                categories_to_assign.append(sample_categories[i % 3])
            df_copy['AI_Category'] = categories_to_assign
        
        # Sample summaries
        sample_summaries = [
            "Missing enterprise-grade security features for SOX compliance",
            "Mobile app crashes with large dataset processing",
            "SSO integration needed for Fortune 500 enterprise deployment",
            "GDPR data export broken causing compliance violations",
            "Dashboard loading times affecting daily operations",
            "Enterprise multi-tenancy and RBAC features missing",
            "Performance issues with 1000+ concurrent users",
            "White-label customization required for enterprise integration",
            "Data encryption doesn't meet security requirements", 
            "User interface requires extensive training"
        ]
        
        num_rows = len(df_copy)
        summaries_to_assign = (sample_summaries * ((num_rows // len(sample_summaries)) + 1))[:num_rows]
        df_copy['AI_Summary'] = summaries_to_assign
        
        return df_copy
    
    def is_configured(self) -> bool:
        return self.client is not None