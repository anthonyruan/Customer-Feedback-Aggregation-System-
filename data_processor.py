import pandas as pd
import streamlit as st
from typing import Dict, List, Optional

class DataProcessor:
    
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
    
    REQUIRED_COLUMNS = ['Feedback', 'Product', 'Severity', 'Region']
    
    def __init__(self):
        pass
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return self._validate_and_clean_data(df)
        except Exception as e:
            st.error(f"Error loading CSV file: {str(e)}")
            return pd.DataFrame()
    
    def load_uploaded_file(self, uploaded_file) -> pd.DataFrame:
        try:
            df = pd.read_csv(uploaded_file)
            return self._validate_and_clean_data(df)
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")
            return pd.DataFrame()
    
    def _validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
            return pd.DataFrame()
        
        df = df.dropna(subset=self.REQUIRED_COLUMNS)
        
        df['Severity'] = df['Severity'].str.strip().str.title()
        df['Region'] = df['Region'].str.strip().str.upper()
        
        invalid_severities = df[~df['Severity'].isin(self.SEVERITY_SCORES.keys())]
        if not invalid_severities.empty:
            st.warning(f"Found {len(invalid_severities)} rows with invalid severity values. Using 'Medium' as default.")
            df.loc[~df['Severity'].isin(self.SEVERITY_SCORES.keys()), 'Severity'] = 'Medium'
        
        invalid_regions = df[~df['Region'].isin(self.REGION_SCORES.keys())]
        if not invalid_regions.empty:
            st.warning(f"Found {len(invalid_regions)} rows with invalid region values. Using 'APAC' as default.")
            df.loc[~df['Region'].isin(self.REGION_SCORES.keys()), 'Region'] = 'APAC'
        
        return df
    
    def calculate_opportunity_score(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['Severity_Score'] = df['Severity'].map(self.SEVERITY_SCORES)
        df['Region_Score'] = df['Region'].map(self.REGION_SCORES)
        df['Opportunity_Score'] = df['Severity_Score'] + df['Region_Score']
        return df
    
    def filter_data(self, df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        filtered_df = df.copy()
        
        if filters.get('categories') and len(filters['categories']) > 0:
            filtered_df = filtered_df[filtered_df['AI_Category'].isin(filters['categories'])]
        
        if filters.get('products') and len(filters['products']) > 0:
            filtered_df = filtered_df[filtered_df['Product'].isin(filters['products'])]
        
        if filters.get('severities') and len(filters['severities']) > 0:
            filtered_df = filtered_df[filtered_df['Severity'].isin(filters['severities'])]
        
        if filters.get('regions') and len(filters['regions']) > 0:
            filtered_df = filtered_df[filtered_df['Region'].isin(filters['regions'])]
        
        return filtered_df
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict:
        stats = {
            'total_feedback': len(df),
            'critical_issues': len(df[df['Severity'] == 'Critical']),
            'compliance_issues': 0,
            'avg_opportunity_score': df['Opportunity_Score'].mean() if 'Opportunity_Score' in df.columns else 0,
            'top_product': df['Product'].value_counts().index[0] if not df.empty else 'N/A',
            'regional_distribution': df['Region'].value_counts().to_dict() if not df.empty else {}
        }
        
        if 'AI_Category' in df.columns:
            stats['compliance_issues'] = len(df[df['AI_Category'] == 'Ensure Regulatory & Data Compliance'])
        
        return stats
    
    def create_sample_data(self) -> pd.DataFrame:
        sample_data = {
            'Feedback': [
                'The new enterprise dashboard is missing critical security features required for SOX compliance',
                'Mobile app crashes frequently when processing large datasets, affecting productivity',
                'Need SSO integration with Okta and Active Directory for our Fortune 500 deployment',
                'GDPR data export functionality is broken and causing compliance violations',
                'Dashboard loading times are unacceptable for our daily operations',
                'Missing advanced role-based access controls and multi-tenancy for enterprise customers',
                'Performance degrades significantly with more than 1000 concurrent users',
                'Need white-label customization and API access for our enterprise integration',
                'Data encryption at rest is not meeting our security requirements',
                'User interface is confusing and requires extensive training'
            ],
            'Product': [
                'Enterprise Dashboard', 'Mobile App', 'API Platform', 'Data Export', 'Analytics Dashboard',
                'Access Control', 'Core Platform', 'Collaboration Tools', 'Security Module', 'User Interface'
            ],
            'Severity': ['Critical', 'High', 'Medium', 'Critical', 'High', 'Critical', 'High', 'Medium', 'Critical', 'Medium'],
            'Region': ['US', 'EU', 'APAC', 'EU', 'US', 'US', 'APAC', 'US', 'EU', 'LATAM'],
            'Category': [
                'Ensure Regulatory & Data Compliance', 'Improve Platform Usability & Performance',
                'Win Enterprise Deals', 'Ensure Regulatory & Data Compliance', 
                'Improve Platform Usability & Performance', 'Win Enterprise Deals',
                'Improve Platform Usability & Performance', 'Win Enterprise Deals',
                'Ensure Regulatory & Data Compliance', 'Improve Platform Usability & Performance'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        return self.calculate_opportunity_score(df)