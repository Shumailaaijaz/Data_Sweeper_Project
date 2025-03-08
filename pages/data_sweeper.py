# imports
import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
from streamlit_option_menu import option_menu
import time

# Configure the Streamlit app's appearance and layout
st.set_page_config(
    page_title="Advanced Data Sweeper",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling the app with modern aesthetics
st.markdown(
    """
    <style>
        /* Main theme colors and styling */
        :root {
            --primary-color: #4361ee;
            --secondary-color: #3a0ca3;
            --background-color: #f8f9fa;
            --card-background: #ffffff;
            --text-color: #1a1a1a;
            --success-color: #4cc9f0;
            --warning-color: #f72585;
            --border-radius: 10px;
            --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            :root {
                --background-color: #121212;
                --card-background: #1e1e1e;
                --text-color: #f8f9fa;
            }
        }
        
        /* Main container styling */
        .main {
            background-color: var(--background-color);
            padding: 1rem;
        }
        
        /* Card styling for sections */
        .css-1r6slb0, .css-keje6w {
            background-color: var(--card-background);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--box-shadow);
            margin-bottom: 1rem;
        }
        
        /* Header styling */
        h1, h2, h3 {
            color: var(--primary-color);
            font-weight: 700;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-align: center;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 0.5rem 0;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: var(--secondary-color);
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
        }
        
        /* File uploader styling */
        .uploadedFile {
            border: 2px dashed var(--primary-color);
            border-radius: var(--border-radius);
            padding: 1rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        /* Progress bar styling */
        .stProgress > div > div {
            background-color: var(--primary-color);
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: var(--border-radius);
            overflow: hidden;
            border: 1px solid #e0e0e0;
        }
        
        .dataframe thead th {
            background-color: var(--primary-color);
            color: white;
            font-weight: 600;
            text-align: center;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background-color: rgba(67, 97, 238, 0.05);
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-1wrcr25 {
            background-color: var(--card-background);
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: var(--border-radius);
            padding: 0.5rem 1rem;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-color);
            color: white;
        }
        
        /* Animation for loading */
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        
        .loading {
            animation: pulse 1.5s infinite;
        }
        
        /* Custom badges */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }
        
        .badge-primary {
            background-color: var(--primary-color);
            color: white;
        }
        
        .badge-success {
            background-color: var(--success-color);
            color: white;
        }
        
        .badge-warning {
            background-color: var(--warning-color);
            color: white;
        }
        
        /* Tooltip styling */
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: pointer;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        
        /* Custom file stats card */
        .file-stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
        }
        
        .stat-card {
            background-color: var(--card-background);
            border-radius: var(--border-radius);
            padding: 1rem;
            box-shadow: var(--box-shadow);
            flex: 1;
            margin: 0 0.5rem;
            text-align: center;
        }
        
        .stat-card h4 {
            margin: 0;
            color: var(--text-color);
        }
        
        .stat-card p {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
            color: var(--primary-color);
        }
        
        /* Custom column selector */
        .column-selector {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 1rem 0;
        }
        
        .column-chip {
            background-color: rgba(67, 97, 238, 0.1);
            border: 1px solid var(--primary-color);
            border-radius: 20px;
            padding: 0.25rem 0.75rem;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .column-chip:hover, .column-chip.selected {
            background-color: var(--primary-color);
            color: white;
        }
        
        /* Custom download button */
        .download-btn {
            display: inline-block;
            background-color: var(--success-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: var(--border-radius);
            text-decoration: none;
            font-weight: 600;
            margin-top: 1rem;
            transition: all 0.3s ease;
        }
        
        .download-btn:hover {
            background-color: #3da5d9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Helper functions
def get_file_size_display(size_bytes):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def get_download_link(df, filename, file_format):
    """Generate a download link for the dataframe"""
    if file_format == "CSV":
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'data:text/csv;base64,{b64}'
        ext = 'csv'
    elif file_format == "Excel":
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode()
        href = f'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}'
        ext = 'xlsx'
    elif file_format == "JSON":
        json_str = df.to_json(orient='records')
        b64 = base64.b64encode(json_str.encode()).decode()
        href = f'data:application/json;base64,{b64}'
        ext = 'json'
    
    download_filename = filename.split('.')[0] + f'.{ext}'
    return f'<a href="{href}" class="download-btn" download="{download_filename}">⬇️ Download {file_format}</a>'

def create_file_stats_cards(df):
    """Create statistics cards for the dataframe"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h4>Rows</h4>
            <p>{:,}</p>
        </div>
        """.format(df.shape[0]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <h4>Columns</h4>
            <p>{:,}</p>
        </div>
        """.format(df.shape[1]), unsafe_allow_html=True)
    
    with col3:
        missing_values = df.isna().sum().sum()
        st.markdown("""
        <div class="stat-card">
            <h4>Missing Values</h4>
            <p>{:,}</p>
        </div>
        """.format(missing_values), unsafe_allow_html=True)
    
    with col4:
        duplicates = df.duplicated().sum()
        st.markdown("""
        <div class="stat-card">
            <h4>Duplicates</h4>
            <p>{:,}</p>
        </div>
        """.format(duplicates), unsafe_allow_html=True)

# App header with logo and title
st.markdown("""
<div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
    <div style="font-size: 2.5rem; margin-right: 0.5rem;">🧹</div>
    <h1>Advanced Data Sweeper</h1>
</div>
<p style="text-align: center; margin-bottom: 2rem;">Transform, clean, and visualize your data with ease</p>
""", unsafe_allow_html=True)

# Create sidebar navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/broom.png", width=80)
    st.markdown("<h2 style='text-align: center;'>Data Sweeper</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=["Upload", "Preview", "Clean", "Visualize", "Convert"],
        icons=["cloud-upload", "table", "tools", "bar-chart", "arrow-repeat"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "var(--primary-color)", "font-size": "1rem"},
            "nav-link": {"font-size": "0.9rem", "text-align": "left", "margin": "0px", "--hover-color": "rgba(67, 97, 238, 0.1)"},
            "nav-link-selected": {"background-color": "var(--primary-color)"},
        }
    )
    
    st.markdown("---")
    st.markdown("### Files")
    
    # Session state initialization
    if 'files' not in st.session_state:
        st.session_state.files = {}
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = {}

# Upload section
if selected == "Upload":
    st.markdown("## 📤 Upload Your Data")
    st.markdown("Upload CSV or Excel files to begin processing. You can upload multiple files and switch between them.")
    
    uploaded_files = st.file_uploader("Choose files:", type=["csv", "xlsx", "xls"], accept_multiple_files=True)
    
    if uploaded_files:
        for file in uploaded_files:
            # Check if file is already in session state
            if file.name not in st.session_state.files:
                # Show progress bar for file loading
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(101):
                    progress_bar.progress(i)
                    status_text.text(f"Loading {file.name}... {i}%")
                    time.sleep(0.01)
                
                # Read the file
                file_extension = os.path.splitext(file.name)[-1].lower()
                try:
                    if file_extension == ".csv":
                        df = pd.read_csv(file)
                    elif file_extension in [".xlsx", ".xls"]:
                        df = pd.read_excel(file)
                    
                    # Store file in session state
                    st.session_state.files[file.name] = {
                        "data": df,
                        "size": file.size,
                        "type": file_extension
                    }
                    
                    # Set as current file if none selected
                    if st.session_state.current_file is None:
                        st.session_state.current_file = file.name
                    
                    # Store processed data
                    st.session_state.processed_data[file.name] = df
                    
                    status_text.success(f"✅ {file.name} loaded successfully!")
                except Exception as e:
                    status_text.error(f"❌ Error loading {file.name}: {str(e)}")
        
        # Display uploaded files
        st.markdown("### 📁 Uploaded Files")
        
        for file_name, file_info in st.session_state.files.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                if st.button(f"📄 {file_name}", key=f"select_{file_name}"):
                    st.session_state.current_file = file_name
            
            with col2:
                st.markdown(f"**Size:** {get_file_size_display(file_info['size'])}")
            
            with col3:
                if st.button("🗑️", key=f"delete_{file_name}"):
                    del st.session_state.files[file_name]
                    if file_name in st.session_state.processed_data:
                        del st.session_state.processed_data[file_name]
                    
                    if st.session_state.current_file == file_name:
                        if st.session_state.files:
                            st.session_state.current_file = list(st.session_state.files.keys())[0]
                        else:
                            st.session_state.current_file = None
                    
                    st.experimental_rerun()
    
    else:
        st.info("👆 Upload your files to get started!")
        
        # Sample data option
        if st.button("🧪 Load Sample Data"):
            # Create sample data
            sample_data = pd.DataFrame({
                'ID': range(1, 101),
                'Name': [f"Product {i}" for i in range(1, 101)],
                'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Other'], 100),
                'Price': np.random.uniform(10, 1000, 100).round(2),
                'Stock': np.random.randint(0, 100, 100),
                'Rating': np.random.uniform(1, 5, 100).round(1),
                'Date Added': pd.date_range(start='2023-01-01', periods=100)
            })
            
            # Add some missing values and duplicates
            sample_data.loc[np.random.choice(sample_data.index, 10), 'Price'] = np.nan
            sample_data.loc[np.random.choice(sample_data.index, 5), 'Category'] = np.nan
            sample_data = pd.concat([sample_data, sample_data.iloc[0:5]])
            
            # Store in session state
            sample_filename = "sample_data.csv"
            st.session_state.files[sample_filename] = {
                "data": sample_data,
                "size": len(sample_data.to_csv().encode('utf-8')),
                "type": ".csv"
            }
            st.session_state.current_file = sample_filename
            st.session_state.processed_data[sample_filename] = sample_data
            
            st.success("✅ Sample data loaded successfully!")
            st.experimental_rerun()

# Preview section
elif selected == "Preview":
    if st.session_state.current_file:
        file_name = st.session_state.current_file
        file_info = st.session_state.files[file_name]
        df = file_info["data"]
        
        st.markdown(f"## 🔍 Previewing: {file_name}")
        
        # File statistics
        create_file_stats_cards(df)
        
        # Data preview
        st.markdown("### Data Preview")
        
        # Add column filter
        all_columns = df.columns.tolist()
        
        # Create column selector with chips
        st.markdown("<p>Select columns to display:</p>", unsafe_allow_html=True)
        
        # Initialize selected columns in session state if not present
        if f"selected_columns_{file_name}" not in st.session_state:
            st.session_state[f"selected_columns_{file_name}"] = all_columns
        
        # Create column selector with chips
        cols_container = st.container()
        col_html = '<div class="column-selector">'
        
        for col in all_columns:
            is_selected = col in st.session_state[f"selected_columns_{file_name}"]
            selected_class = "selected" if is_selected else ""
            col_html += f'<div class="column-chip {selected_class}" onclick="this.classList.toggle(\'selected\'); Streamlit.setComponentValue(\'{col}\')">{col}</div>'
        
        col_html += '</div>'
        cols_container.markdown(col_html, unsafe_allow_html=True)
        
        # Handle column selection with a workaround (since the JS click won't work directly)
        col_select = st.multiselect(
            "Filter columns:",
            options=all_columns,
            default=st.session_state[f"selected_columns_{file_name}"],
            key=f"col_select_{file_name}"
        )
        
        st.session_state[f"selected_columns_{file_name}"] = col_select
        
        # Display dataframe with selected columns
        if col_select:
            st.dataframe(df[col_select].head(10), use_container_width=True)
            
            # Show data types
            st.markdown("### Data Types")
            dtypes_df = pd.DataFrame(df[col_select].dtypes, columns=["Data Type"])
            dtypes_df = dtypes_df.reset_index().rename(columns={"index": "Column"})
            st.dataframe(dtypes_df, use_container_width=True)
            
            # Show summary statistics for numeric columns
            numeric_cols = df[col_select].select_dtypes(include=['number']).columns
            if not numeric_cols.empty:
                st.markdown("### Summary Statistics")
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        else:
            st.warning("Please select at least one column to display.")
    else:
        st.info("Please upload a file in the Upload section first.")

# Clean section
elif selected == "Clean":
    if st.session_state.current_file:
        file_name = st.session_state.current_file
        
        # Get the original data
        original_df = st.session_state.files[file_name]["data"]
        
        # Get the processed data (or use original if not yet processed)
        if file_name in st.session_state.processed_data:
            df = st.session_state.processed_data[file_name]
        else:
            df = original_df.copy()
            st.session_state.processed_data[file_name] = df
        
        st.markdown(f"## 🧹 Cleaning: {file_name}")
        
        # File statistics
        create_file_stats_cards(df)
        
        # Cleaning options
        st.markdown("### Cleaning Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Data Quality")
            
            # Remove duplicates
            if st.checkbox("Remove duplicate rows", key="remove_duplicates"):
                duplicate_count = df.duplicated().sum()
                if duplicate_count > 0:
                    if st.button(f"Remove {duplicate_count} duplicates"):
                        df = df.drop_duplicates()
                        st.session_state.processed_data[file_name] = df
                        st.success(f"✅ Removed {duplicate_count} duplicate rows!")
                        st.experimental_rerun()
                else:
                    st.info("No duplicates found in the data.")
            
            # Handle missing values
            if st.checkbox("Handle missing values", key="handle_missing"):
                missing_cols = df.columns[df.isna().any()].tolist()
                
                if missing_cols:
                    missing_strategy = st.selectbox(
                        "Choose strategy for missing values:",
                        ["Drop rows with any missing values", 
                         "Fill numeric with mean", 
                         "Fill numeric with median",
                         "Fill with custom value"]
                    )
                    
                    if missing_strategy == "Drop rows with any missing values":
                        missing_count = df.isna().any(axis=1).sum()
                        if st.button(f"Drop {missing_count} rows with missing values"):
                            df = df.dropna()
                            st.session_state.processed_data[file_name] = df
                            st.success(f"✅ Dropped {missing_count} rows with missing values!")
                            st.experimental_rerun()
                    
                    elif missing_strategy == "Fill numeric with mean":
                        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                        numeric_missing = [col for col in numeric_cols if col in missing_cols]
                        
                        if numeric_missing:
                            if st.button(f"Fill {len(numeric_missing)} numeric columns with mean"):
                                for col in numeric_missing:
                                    df[col] = df[col].fillna(df[col].mean())
                                st.session_state.processed_data[file_name] = df
                                st.success(f"✅ Filled missing values in {len(numeric_missing)} columns with mean!")
                                st.experimental_rerun()
                        else:
                            st.info("No numeric columns with missing values found.")
                    
                    elif missing_strategy == "Fill numeric with median":
                        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                        numeric_missing = [col for col in numeric_cols if col in missing_cols]
                        
                        if numeric_missing:
                            if st.button(f"Fill {len(numeric_missing)} numeric columns with median"):
                                for col in numeric_missing:
                                    df[col] = df[col].fillna(df[col].median())
                                st.session_state.processed_data[file_name] = df
                                st.success(f"✅ Filled missing values in {len(numeric_missing)} columns with median!")
                                st.experimental_rerun()
                        else:
                            st.info("No numeric columns with missing values found.")
                    
                    elif missing_strategy == "Fill with custom value":
                        col_to_fill = st.selectbox("Select column to fill:", missing_cols)
                        fill_value = st.text_input("Enter value to fill missing data:")
                        
                        if st.button("Fill missing values"):
                            df[col_to_fill] = df[col_to_fill].fillna(fill_value)
                            st.session_state.processed_data[file_name] = df
                            st.success(f"✅ Filled missing values in {col_to_fill}!")
                            st.experimental_rerun()
                else:
                    st.info("No missing values found in the data.")
        
        with col2:
            st.markdown("#### Data Transformation")
            
            # Column operations
            if st.checkbox("Column operations", key="column_ops"):
                operation = st.selectbox(
                    "Choose operation:",
                    ["Rename columns", "Drop columns", "Create new column"]
                )
                
                if operation == "Rename columns":
                    col_to_rename = st.selectbox("Select column to rename:", df.columns)
                    new_name = st.text_input("Enter new column name:")
                    
                    if st.button("Rename column"):
                        if new_name and new_name != col_to_rename:
                            df = df.rename(columns={col_to_rename: new_name})
                            st.session_state.processed_data[file_name] = df
                            st.success(f"✅ Renamed column '{col_to_rename}' to '{new_name}'!")
                            st.experimental_rerun()
                
                elif operation == "Drop columns":
                    cols_to_drop = st.multiselect("Select columns to drop:", df.columns)
                    
                    if cols_to_drop and st.button(f"Drop {len(cols_to_drop)} columns"):
                        df = df.drop(columns=cols_to_drop)
                        st.session_state.processed_data[file_name] = df
                        st.success(f"✅ Dropped {len(cols_to_drop)} columns!")
                        st.experimental_rerun()
                
                elif operation == "Create new column":
                    new_col_name = st.text_input("Enter new column name:")
                    
                    formula_type = st.radio(
                        "Formula type:",
                        ["Simple calculation", "Custom expression"]
                    )
                    
                    if formula_type == "Simple calculation":
                        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                        
                        if len(numeric_cols) >= 2:
                            col1_calc = st.selectbox("First column:", numeric_cols, key="col1_calc")
                            operation = st.selectbox("Operation:", ["+", "-", "*", "/"], key="operation")
                            col2_calc = st.selectbox("Second column:", numeric_cols, key="col2_calc")
                            
                            if st.button("Create column"):
                                if new_col_name:
                                    if operation == "+":
                                        df[new_col_name] = df[col1_calc] + df[col2_calc]
                                    elif operation == "-":
                                        df[new_col_name] = df[col1_calc] - df[col2_calc]
                                    elif operation == "*":
                                        df[new_col_name] = df[col1_calc] * df[col2_calc]
                                    elif operation == "/":
                                        df[new_col_name] = df[col1_calc] / df[col2_calc]
                                    
                                    st.session_state.processed_data[file_name] = df
                                    st.success(f"✅ Created new column '{new_col_name}'!")
                                    st.experimental_rerun()
                        else:
                            st.warning("Need at least 2 numeric columns for calculations.")
                    
                    elif formula_type == "Custom expression":
                        st.markdown("Enter a Python expression using column names, e.g., `df['A'] * 2 + df['B']`")
                        custom_expr = st.text_area("Expression:")
                        
                        if st.button("Create column with expression"):
                            if new_col_name and custom_expr:
                                try:
                                    # Safely evaluate the expression
                                    result = eval(custom_expr)
                                    df[new_col_name] = result
                                    st.session_state.processed_data[file_name] = df
                                    st.success(f"✅ Created new column '{new_col_name}'!")
                                    st.experimental_rerun()
                                except Exception as e:
                                    st.error(f"Error creating column: {str(e)}")
            
            # Data type conversion
            if st.checkbox("Convert data types", key="convert_types"):
                col_to_convert = st.selectbox("Select column to convert:", df.columns)
                current_type = df[col_to_convert].dtype
                
                target_type = st.selectbox(
                    "Convert to:",
                    ["string", "integer", "float", "datetime", "category"]
                )
                
                if st.button(f"Convert {col_to_convert} to {target_type}"):
                    try:
                        if target_type == "string":
                            df[col_to_convert] = df[col_to_convert].astype(str)
                        elif target_type == "integer":
                            df[col_to_convert] = pd.to_numeric(df[col_to_convert], errors='coerce').astype('Int64')
                        elif target_type == "float":
                            df[col_to_convert] = pd.to_numeric(df[col_to_convert], errors='coerce')
                        elif target_type == "datetime":
                            df[col_to_convert] = pd.to_datetime(df[col_to_convert], errors='coerce')
                        elif target_type == "category":
                            df[col_to_convert] = df[col_to_convert].astype('category')
                        
                        st.session_state.processed_data[file_name] = df
                        st.success(f"✅ Converted {col_to_convert} to {target_type}!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error converting data type: {str(e)}")
        
        # Advanced cleaning
        with st.expander("Advanced Cleaning Options"):
            st.markdown("#### Text Cleaning")
            
            # Text cleaning operations
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if text_cols:
                text_col = st.selectbox("Select text column:", text_cols)
                
                text_operations = st.multiselect(
                    "Choose text operations:",
                    ["Lowercase", "Uppercase", "Remove whitespace", "Remove special characters", "Extract numbers"]
                )
                
                if text_operations and st.button("Apply text operations"):
                    modified = False
                    
                    if "Lowercase" in text_operations:
                        df[text_col] = df[text_col].str.lower()
                        modified = True
                    
                    if "Uppercase" in text_operations:
                        df[text_col] = df[text_col].str.upper()
                        modified = True
                    
                    if "Remove whitespace" in text_operations:
                        df[text_col] = df[text_col].str.strip()
                        modified = True
                    
                    if "Remove special characters" in text_operations:
                        df[text_col] = df[text_col].str.replace(r'[^\w\s]', '', regex=True)
                        modified = True
                    
                    if "Extract numbers" in text_operations:
                        new_col = f"{text_col}_numbers"
                        df[new_col] = df[text_col].str.extract(r'(\d+)', expand=False)
                        modified = True
                    
                    if modified:
                        st.session_state.processed_data[file_name] = df
                        st.success("✅ Applied text operations successfully!")
                        st.experimental_rerun()
            else:
                st.info("No text columns found in the data.")
            
            st.markdown("#### Outlier Detection")
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if numeric_cols:
                outlier_col = st.selectbox("Select column for outlier detection:", numeric_cols)
                
                outlier_method = st.radio(
                    "Outlier detection method:",
                    ["Z-Score", "IQR (Interquartile Range)"]
                )
                
                if outlier_method == "Z-Score":
                    z_threshold = st.slider("Z-Score threshold:", 1.0, 5.0, 3.0, 0.1)
                    
                    if st.button("Detect outliers (Z-Score)"):
                        z_scores = np.abs((df[outlier_col] - df[outlier_col].mean()) / df[outlier_col].std())
                        outliers = df[z_scores > z_threshold]
                        
                        if not outliers.empty:
                            st.warning(f"Found {len(outliers)} outliers using Z-Score method.")
                            st.dataframe(outliers, use_container_width=True)
                            
                            if st.button("Remove these outliers"):
                                df = df[z_scores <= z_threshold]
                                st.session_state.processed_data[file_name] = df
                                st.success(f"✅ Removed {len(outliers)} outliers!")
                                st.experimental_rerun()
                        else:
                            st.success("No outliers detected using Z-Score method.")
                
                elif outlier_method == "IQR (Interquartile Range)":
                    iqr_factor = st.slider("IQR factor:", 1.0, 3.0, 1.5, 0.1)
                    
                    if st.button("Detect outliers (IQR)"):
                        Q1 = df[outlier_col].quantile(0.25)
                        Q3 = df[outlier_col].quantile(0.75)
                        IQR = Q3 - Q1
                        
                        lower_bound = Q1 - iqr_factor * IQR
                        upper_bound = Q3 + iqr_factor * IQR
                        
                        outliers = df[(df[outlier_col] < lower_bound) | (df[outlier_col] > upper_bound)]
                        
                        if not outliers.empty:
                            st.warning(f"Found {len(outliers)} outliers using IQR method.")
                            st.dataframe(outliers, use_container_width=True)
                            
                            if st.button("Remove these outliers"):
                                df = df[(df[outlier_col] >= lower_bound) & (df[outlier_col] <= upper_bound)]
                                st.session_state.processed_data[file_name] = df
                                st.success(f"✅ Removed {len(outliers)} outliers!")
                                st.experimental_rerun()
                        else:
                            st.success("No outliers detected using IQR method.")
            else:
                st.info("No numeric columns found in the data.")
        
        # Reset to original data
        if st.button("Reset to original data"):
            st.session_state.processed_data[file_name] = original_df.copy()
            st.success("✅ Reset to original data!")
            st.experimental_rerun()
        
        # Preview cleaned data
        st.markdown("### Preview Cleaned Data")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Show changes summary
        if not df.equals(original_df):
            st.markdown("### Changes Summary")
            
            changes = []
            
            # Check for row count changes
            if len(df) != len(original_df):
                changes.append(f"Rows: {len(original_df)} → {len(df)} ({len(df) - len(original_df):+d})")
            
            # Check for column count changes
            if len(df.columns) != len(original_df.columns):
                changes.append(f"Columns: {len(original_df.columns)} → {len(df.columns)} ({len(df.columns) - len(original_df.columns):+d})")
            
            # Check for missing values changes
            original_missing = original_df.isna().sum().sum()
            current_missing = df.isna().sum().sum()
            if original_missing != current_missing:
                changes.append(f"Missing values: {original_missing} → {current_missing} ({current_missing - original_missing:+d})")
            
            # Check for duplicate changes
            original_dupes = original_df.duplicated().sum()
            current_dupes = df.duplicated().sum()
            if original_dupes != current_dupes:
                changes.append(f"Duplicates: {original_dupes} → {current_dupes} ({current_dupes - original_dupes:+d})")
            
            # Display changes
            for change in changes:
                st.markdown(f"- {change}")
    else:
        st.info("Please upload a file in the Upload section first.")

# Visualize section
elif selected == "Visualize":
    if st.session_state.current_file:
        file_name = st.session_state.current_file
        
        # Get the processed data
        if file_name in st.session_state.processed_data:
            df = st.session_state.processed_data[file_name]
        else:
            df = st.session_state.files[file_name]["data"]
            st.session_state.processed_data[file_name] = df
        
        st.markdown(f"## 📊 Visualizing: {file_name}")
        
        # Chart type selection
        chart_type = st.selectbox(
            "Select chart type:",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Pie Chart", "Heatmap", "Pair Plot"]
        )
        
        # Get numeric and categorical columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if chart_type == "Bar Chart":
            st.markdown("### Bar Chart")
            
            if categorical_cols and numeric_cols:
                x_axis = st.selectbox("X-axis (categorical):", categorical_cols)
                y_axis = st.selectbox("Y-axis (numeric):", numeric_cols)
                
                orientation = st.radio("Orientation:", ["Vertical", "Horizontal"])
                
                color_option = None
                if len(categorical_cols) > 1:
                    use_color = st.checkbox("Use color grouping")
                    if use_color:
                        color_cols = [col for col in categorical_cols if col != x_axis]
                        color_option = st.selectbox("Color by:", color_cols)
                
                if st.button("Generate Bar Chart"):
                    if orientation == "Vertical":
                        if color_option:
                            fig = px.bar(df, x=x_axis, y=y_axis, color=color_option, 
                                         title=f"{y_axis} by {x_axis}", 
                                         template="plotly_dark")
                        else:
                            fig = px.bar(df, x=x_axis, y=y_axis, 
                                         title=f"{y_axis} by {x_axis}", 
                                         template="plotly_dark")
                    else:
                        if color_option:
                            fig = px.bar(df, y=x_axis, x=y_axis, color=color_option, 
                                         title=f"{y_axis} by {x_axis}", 
                                         orientation='h', template="plotly_dark")
                        else:
                            fig = px.bar(df, y=x_axis, x=y_axis, 
                                         title=f"{y_axis} by {x_axis}", 
                                         orientation='h', template="plotly_dark")
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white")
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Bar charts require both categorical and numeric columns.")
        
        elif chart_type == "Line Chart":
            st.markdown("### Line Chart")
            
            if numeric_cols:
                # Check if there's a date column
                date_cols = []
                for col in df.columns:
                    if df[col].dtype == 'datetime64[ns]' or pd.api.types.is_datetime64_any_dtype(df[col]):
                        date_cols.append(col)
                
                if date_cols:
                    x_axis = st.selectbox("X-axis (date):", date_cols)
                else:
                    x_axis = st.selectbox("X-axis:", df.columns)
                
                y_axes = st.multiselect("Y-axis (numeric):", numeric_cols)
                
                if y_axes and st.button("Generate Line Chart"):
                    fig = px.line(df, x=x_axis, y=y_axes, 
                                  title=f"Line Chart of {', '.join(y_axes)} over {x_axis}", 
                                  template="plotly_dark")
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white")
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Line charts require numeric columns.")
        
        elif chart_type == "Scatter Plot":
            st.markdown("### Scatter Plot")
            
            if len(numeric_cols) >= 2:
                x_axis = st.selectbox("X-axis (numeric):", numeric_cols)
                y_axis = st.selectbox("Y-axis (numeric):", [col for col in numeric_cols if col != x_axis])
                
                color_option = None
                size_option = None
                
                use_color = st.checkbox("Use color grouping")
                if use_color:
                    color_option = st.selectbox("Color by:", df.columns)
                
                use_size = st.checkbox("Use size variation")
                if use_size:
                    size_cols = [col for col in numeric_cols if col != x_axis and col != y_axis]
                    if size_cols:
                        size_option = st.selectbox("Size by:", size_cols)
                
                if st.button("Generate Scatter Plot"):
                    fig = px.scatter(
                        df, x=x_axis, y=y_axis, 
                        color=color_option, size=size_option,
                        title=f"Scatter Plot of {y_axis} vs {x_axis}",
                        template="plotly_dark"
                    )
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white")
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Scatter plots require at least 2 numeric columns.")
        
        elif chart_type == "Histogram":
            st.markdown("### Histogram")
            
            if numeric_cols:
                column = st.selectbox("Select column:", numeric_cols)
                bins = st.slider("Number of bins:", 5, 100, 20)
                
                color_option = None
                if categorical_cols:
                    use_color = st.checkbox("Group by category")
                    if use_color:
                        color_option = st.selectbox("Group by:", categorical_cols)
                
                if st.button("Generate Histogram"):
                    if color_option:
                        fig = px.histogram(
                            df, x=column, color=color_option, 
                            nbins=bins, 
                            title=f"Histogram of {column} grouped by {color_option}",
                            template="plotly_dark"
                        )
                    else:
                        fig = px.histogram(
                            df, x=column, 
                            nbins=bins, 
                            title=f"Histogram of {column}",
                            template="plotly_dark"
                        )
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white")
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Histograms require numeric columns.")
        
        elif chart_type == "Box Plot":
            st.markdown("### Box Plot")
            
            if numeric_cols:
                y_axis = st.selectbox("Value column (numeric):", numeric_cols)
                
                x_axis = None
                if categorical_cols:
                    use_category = st.checkbox("Group by category")
                    if use_category:
                        x_axis = st.selectbox("Group by:", categorical_cols)
                
                if st.button("Generate Box Plot"):
                    if x_axis:
                        fig = px.box(
                            df, x=x_axis, y=y_axis, 
                            title=f"Box Plot of {y_axis} grouped by {x_axis}",
                            template="plotly_dark"
                        )
                    else:
                        fig = px.box(
                            df, y=y_axis, 
                            title=f"Box Plot of {y_axis}",
                            template="plotly_dark"
                        )
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white")
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Box plots require numeric columns.")
        
        elif chart_type == "Pie Chart":
            st.markdown("### Pie Chart")
            
            if categorical_cols and numeric_cols:
                names = st.selectbox("Category column:", categorical_cols)
                values = st.selectbox("Value column (numeric):", numeric_cols)
                
                if st.button("Generate Pie Chart"):
                    # Aggregate data for pie chart
                    pie_data = df.groupby(names)[values].sum().reset_index()
                    
                    fig = px.pie(
                        pie_data, names=names, values=values,
                        title=f"Pie Chart of {values} by {names}",
                        template="plotly_dark"
                    )
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white")
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Pie charts require both categorical and numeric columns.")
        
        elif chart_type == "Heatmap":
            st.markdown("### Heatmap")
            
            if len(numeric_cols) >= 2:
                columns_for_heatmap = st.multiselect("Select columns for correlation:", numeric_cols, default=numeric_cols[:5])
                
                if columns_for_heatmap and len(columns_for_heatmap) >= 2:
                    if st.button("Generate Heatmap"):
                        corr = df[columns_for_heatmap].corr()
                        
                        fig = px.imshow(
                            corr, text_auto=True, 
                            title="Correlation Heatmap",
                            color_continuous_scale='RdBu_r',
                            template="plotly_dark"
                        )
                        
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="white")
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Please select at least 2 columns for the heatmap.")
            else:
                st.warning("Heatmaps require at least 2 numeric columns.")
        
        elif chart_type == "Pair Plot":
            st.markdown("### Pair Plot")
            
            if len(numeric_cols) >= 2:
                columns_for_pairplot = st.multiselect("Select columns:", numeric_cols, default=numeric_cols[:3])
                
                color_option = None
                if categorical_cols:
                    use_color = st.checkbox("Color by category")
                    if use_color:
                        color_option = st.selectbox("Color by:", categorical_cols)
                
                if columns_for_pairplot and len(columns_for_pairplot) >= 2:
                    if st.button("Generate Pair Plot"):
                        fig = px.scatter_matrix(
                            df, dimensions=columns_for_pairplot, color=color_option,
                            title="Pair Plot",
                            template="plotly_dark"
                        )
                        
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="white")
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Please select at least 2 columns for the pair plot.")
            else:
                st.warning("Pair plots require at least 2 numeric columns.")
        
        # Data insights
        with st.expander("Data Insights"):
            if numeric_cols:
                st.markdown("### Numeric Column Statistics")
                
                for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
                    st.markdown(f"#### {col}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Mean", f"{df[col].mean():.2f}")
                    
                    with col2:
                        st.metric("Median", f"{df[col].median():.2f}")
                    
                    with col3:
                        st.metric("Std Dev", f"{df[col].std():.2f}")
                    
                    # Create a small histogram
                    fig = px.histogram(df, x=col, template="plotly_dark")
                    fig.update_layout(
                        height=200,
                        margin=dict(l=20, r=20, t=30, b=20),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white")
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            if categorical_cols:
                st.markdown("### Categorical Column Statistics")
                
                for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
                    st.markdown(f"#### {col}")
                    
                    # Get value counts
                    value_counts = df[col].value_counts().reset_index()
                    value_counts.columns = [col, 'Count']
                    
                    # Display top categories
                    st.dataframe(value_counts.head(5), use_container_width=True)
                    
                    # Create a small bar chart
                    fig = px.bar(
                        value_counts.head(10), x=col, y='Count',
                        template="plotly_dark"
                    )
                    fig.update_layout(
                        height=200,
                        margin=dict(l=20, r=20, t=30, b=20),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white")
                    )
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please upload a file in the Upload section first.")

# Convert section
elif selected == "Convert":
    if st.session_state.current_file:
        file_name = st.session_state.current_file
        
        # Get the processed data
        if file_name in st.session_state.processed_data:
            df = st.session_state.processed_data[file_name]
        else:
            df = st.session_state.files[file_name]["data"]
        
        st.markdown(f"## 🔄 Converting: {file_name}")
        
        # File statistics
        create_file_stats_cards(df)
        
        # Conversion options
        st.markdown("### Conversion Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Output format
            output_format = st.radio(
                "Output format:",
                ["CSV", "Excel", "JSON", "HTML", "Markdown"]
            )
            
            # Include index
            include_index = st.checkbox("Include row index", value=False)
            
            # Compression options for CSV
            compression = None
            if output_format == "CSV":
                use_compression = st.checkbox("Compress output file")
                if use_compression:
                    compression = st.selectbox("Compression type:", ["gzip", "zip", "bz2", "xz"])
        
        with col2:
            # Column selection
            st.markdown("#### Columns to Include")
            all_columns = df.columns.tolist()
            selected_columns = st.multiselect("Select columns:", all_columns, default=all_columns)
            
            if not selected_columns:
                st.warning("Please select at least one column.")
            
            # Row filtering
            st.markdown("#### Row Filtering")
            use_row_filter = st.checkbox("Filter rows")
            
            row_filter_expr = None
            if use_row_filter:
                st.markdown("Enter a Python expression to filter rows, e.g., `df['Age'] > 30`")
                row_filter_expr = st.text_area("Filter expression:")
        
        # Preview filtered data
        if selected_columns:
            filtered_df = df[selected_columns]
            
            if use_row_filter and row_filter_expr:
                try:
                    filtered_df = filtered_df[eval(row_filter_expr)]
                    st.success(f"Filter applied: {len(filtered_df)} rows match the criteria.")
                except Exception as e:
                    st.error(f"Error applying filter: {str(e)}")
            
            st.markdown("### Preview")
            st.dataframe(filtered_df.head(5), use_container_width=True)
            
            # Generate download link
            if st.button("Generate Download Link"):
                try:
                    if output_format == "CSV":
                        download_link = get_download_link(filtered_df, file_name, "CSV")
                    elif output_format == "Excel":
                        download_link = get_download_link(filtered_df, file_name, "Excel")
                    elif output_format == "JSON":
                        download_link = get_download_link(filtered_df, file_name, "JSON")
                    elif output_format == "HTML":
                        html = filtered_df.to_html(index=include_index)
                        b64 = base64.b64encode(html.encode()).decode()
                        href = f'data:text/html;base64,{b64}'
                        download_filename = file_name.split('.')[0] + '.html'
                        download_link = f'<a href="{href}" class="download-btn" download="{download_filename}">⬇️ Download HTML</a>'
                    elif output_format == "Markdown":
                        markdown = filtered_df.to_markdown(index=include_index)
                        b64 = base64.b64encode(markdown.encode()).decode()
                        href = f'data:text/markdown;base64,{b64}'
                        download_filename = file_name.split('.')[0] + '.md'
                        download_link = f'<a href="{href}" class="download-btn" download="{download_filename}">⬇️ Download Markdown</a>'
                    
                    st.markdown(download_link, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating download link: {str(e)}")
    else:
        st.info("Please upload a file in the Upload section first.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #888;">
        <p>Advanced Data Sweeper | Made with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)