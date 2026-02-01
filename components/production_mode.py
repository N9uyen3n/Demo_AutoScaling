
import streamlit as st
from pathlib import Path


def render_production_mode_controls():
    """
    Render controls for production mode
    
    Returns:
        dict: Production mode settings
    """
    st.sidebar.divider()
    st.sidebar.markdown("### 🎯 Mode Selection")
    
    mode = st.sidebar.radio(
        "Operation Mode",
        ["Simulation", "Production (Real Data)"],
        help="Simulation: Dùng dữ liệu giả lập | Production: Dùng dữ liệu thực"
    )
    
    settings = {
        'mode': mode,
        'data_source': None,
        'model_path': None,
        'uploaded_data': None
    }
    
    if mode == "Production (Real Data)":
        st.sidebar.markdown("#### 📊 Data Source")
        
        data_source = st.sidebar.selectbox(
            "Select Data Source",
            ["Upload CSV", "Load from File", "API (Coming Soon)"]
        )
        
        settings['data_source'] = data_source
        
        if data_source == "Upload CSV":
            uploaded_file = st.sidebar.file_uploader(
                "Upload CSV file",
                type=['csv'],
                help="CSV với columns: timestamp, requests_per_minute"
            )
            settings['uploaded_data'] = uploaded_file
            
            if uploaded_file:
                st.sidebar.success(f"✅ Uploaded: {uploaded_file.name}")
        
        elif data_source == "Load from File":
            data_path = st.sidebar.text_input(
                "Data File Path",
                value="DATA/sample_data.csv",
                help="Path to CSV file"
            )
            settings['data_path'] = data_path
            
            if Path(data_path).exists():
                st.sidebar.success(f"✅ File found: {data_path}")
            else:
                st.sidebar.warning(f"⚠️ File not found: {data_path}")
        
        st.sidebar.markdown("#### 🤖 Model Configuration")
        
        use_model = st.sidebar.checkbox(
            "Use Trained Model",
            value=False,
            help="Load model đã train thay vì simulation"
        )
        
        if use_model:
            model_path = st.sidebar.text_input(
                "Model File Path",
                value="models/xgboost_model.joblib",
                help="Path to .pkl or .joblib model file"
            )
            settings['model_path'] = model_path
            
            if Path(model_path).exists():
                st.sidebar.success(f"✅ Model found: {model_path}")
            else:
                st.sidebar.warning(f"⚠️ Model not found: {model_path}")
    
    return settings


def render_data_info(df):
    """
    Display information about loaded data
    
    Args:
        df: Loaded DataFrame
    """
    with st.expander("📊 Data Information", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", len(df))
        
        with col2:
            if 'timestamp' in df.columns:
                st.metric("Time Range", f"{(df['timestamp'].max() - df['timestamp'].min()).days} days")
        
        with col3:
            if 'requests_per_minute' in df.columns:
                st.metric("Avg Load", f"{df['requests_per_minute'].mean():.1f} req/m")
        
        st.dataframe(df.head(10), use_container_width=True)


def render_model_info(model_manager):
    """
    Display information about loaded model
    
    Args:
        model_manager: ModelManager instance
    """
    info = model_manager.get_model_info()
    
    if info['loaded']:
        with st.expander("🤖 Model Information", expanded=False):
            st.success(f"**Model Type:** {info['type']}")
            
            if info['parameters']:
                st.json(info['parameters'])
    else:
        st.info("💡 No model loaded. Using simulation mode.")
