"""
AWS Theme CSS for Outliers Demo Dashboard
"""

def get_aws_css():
    """Return AWS-style CSS for Streamlit"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amazon+Ember:wght@400;500;700&family=Open+Sans:wght@400;600;700&display=swap');
    
    /* AWS Color Palette */
    :root {
        --aws-squid-ink: #232F3E;
        --aws-orange: #FF9900;
        --aws-blue: #146EB4;
        --aws-light-blue: #00A8E1;
        --aws-dark-bg: #16191f;
        --aws-card-bg: #232F3E;
    }
    
    * { 
        font-family: 'Open Sans', 'Amazon Ember', sans-serif; 
    }
    
    /* Main Background - AWS Dark Theme */
    .main { 
        background: linear-gradient(135deg, #0d1117 0%, #16191f 50%, #1c2128 100%);
    }
    
    /* Sidebar - AWS Style */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #232F3E 0%, #1a252f 100%);
        border-right: 2px solid #FF9900;
    }
    
    [data-testid="stSidebar"] h1 {
        color: #FF9900 !important;
        background: none !important;
        -webkit-text-fill-color: #FF9900 !important;
    }
    
    /* Metric Cards - AWS CloudWatch Style */
    .stMetric { 
        background: linear-gradient(135deg, #232F3E 0%, #2a3f54 100%);
        border-radius: 8px; 
        padding: 20px; 
        border-left: 4px solid #FF9900;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 6px 20px rgba(255, 153, 0, 0.3);
        border-left-color: #00A8E1;
    }
    
    .stMetric label {
        color: #AAB7B8 !important;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
        font-weight: 700;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        font-weight: 600;
    }
    
    /* Headers - AWS Style */
    h1 { 
        color: #FFFFFF !important;
        font-weight: 700;
        background: none !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-bottom: 3px solid #FF9900;
        padding-bottom: 10px;
    }
    
    h3 {
        color: #FF9900 !important;
        font-weight: 600;
        margin-top: 20px;
    }
    
    /* Tabs - AWS Console Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #232F3E;
        border-radius: 8px 8px 0 0;
        padding: 0;
        border-bottom: 2px solid #FF9900;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0;
        color: #AAB7B8;
        font-weight: 600;
        padding: 12px 24px;
        background-color: transparent;
        border-right: 1px solid #3d4466;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 153, 0, 0.1);
        color: #FF9900;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #146EB4;
        color: white;
        border-bottom: 3px solid #FF9900;
    }
    
    /* Dataframe - AWS Table Style */
    [data-testid="stDataFrame"] {
        background-color: #232F3E;
        border: 1px solid #3d4466;
        border-radius: 8px;
    }
    
    /* Dividers */
    hr {
        border-color: #FF9900;
        opacity: 0.3;
    }
    
    /* Info/Success/Error Boxes - AWS Alert Style */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    /* Buttons and Inputs */
    .stButton button {
        background-color: #FF9900;
        color: #232F3E;
        border: none;
        border-radius: 4px;
        font-weight: 600;
        padding: 8px 16px;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background-color: #EC7211;
        box-shadow: 0 4px 12px rgba(255, 153, 0, 0.4);
    }
    
    /* Markdown text */
    .markdown-text-container {
        color: #D5DBDB;
    }
    
    /* Plotly Charts - Dark theme integration */
    .js-plotly-plot {
        border-radius: 8px;
        background-color: #232F3E;
    }
    </style>
    """
