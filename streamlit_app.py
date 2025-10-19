import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Local Waste Management System",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)




# Custom CSS for VS Code dark theme
st.markdown("""
<style>
    /* Global body and html styling */
    html, body, #root, .main {
        background-color: #ffffff !important;
        color: #569cd6 !important;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #ffffff !important;
        color: #569cd6 !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Force white background on all main content elements */
    .main > div,
    .main > div > div,
    .main .block-container > div,
    .main .block-container > div > div {
        background-color: #ffffff !important;
    }
    
    /* Sidebar styling - multiple selectors for compatibility */
    .css-1d391kg, 
    .css-1cypcdb, 
    .css-17eq0hr,
    .sidebar .sidebar-content,
    [data-testid="stSidebar"] {
        background-color: #252526 !important;
    }
    
    /* Sidebar content */
    .css-1d391kg .css-1v0mbdj,
    .css-1cypcdb .css-1v0mbdj,
    .sidebar .sidebar-content .css-1v0mbdj {
        background-color: #252526 !important;
    }
    
    /* Sidebar title */
    .css-1d391kg h1,
    .css-1cypcdb h1,
    .sidebar h1 {
        color: #569cd6 !important;
    }
    
    /* Radio buttons styling */
    .css-1d391kg .stRadio > div > label > div[data-testid="stMarkdownContainer"],
    .css-1cypcdb .stRadio > div > label > div[data-testid="stMarkdownContainer"],
    .sidebar .stRadio > div > label > div[data-testid="stMarkdownContainer"] {
        color: #569cd6 !important;
    }
    
    .css-1d391kg .stRadio > div > label > div[data-testid="stMarkdownContainer"]:hover,
    .css-1cypcdb .stRadio > div > label > div[data-testid="stMarkdownContainer"]:hover,
    .sidebar .stRadio > div > label > div[data-testid="stMarkdownContainer"]:hover {
        color: #4fc1ff !important;
    }
    
    /* Selected radio button */
    .css-1d391kg .stRadio > div > label > div[data-testid="stMarkdownContainer"]:has(+ input:checked),
    .css-1cypcdb .stRadio > div > label > div[data-testid="stMarkdownContainer"]:has(+ input:checked),
    .sidebar .stRadio > div > label > div[data-testid="stMarkdownContainer"]:has(+ input:checked) {
        color: #4fc1ff !important;
        font-weight: bold;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #569cd6 !important;
    }
    
    /* Text content */
    .main .block-container p, 
    .main .block-container div,
    .main p,
    .main div {
        color: #569cd6 !important;
    }
    
    /* Code blocks */
    .main .block-container pre,
    .main pre {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: #569cd6 !important;
    }
    
    /* DataFrames */
    .dataframe {
        background-color: #1e1e1e !important;
        color: #569cd6 !important;
    }
    
    /* Tables */
    table {
        background-color: #1e1e1e !important;
        color: #569cd6 !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #3c3c3c !important;
        color: #569cd6 !important;
        border: 1px solid #007acc !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #007acc !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
    }
    
    .stButton > button:hover {
        background-color: #005a9e !important;
    }
    
    /* Form styling */
    .stForm {
        background-color: #2d2d30 !important;
        border: 1px solid #3c3c3c !important;
        border-radius: 4px !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #3c3c3c !important;
        color: #569cd6 !important;
        border: 1px solid #007acc !important;
    }
    
    /* Metrics */
    .metric-container {
        background-color: #2d2d30 !important;
        border: 1px solid #3c3c3c !important;
        border-radius: 4px !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #0d4f3c !important;
        color: #4caf50 !important;
        border: 1px solid #4caf50 !important;
    }
    
    .stError {
        background-color: #4f0d0d !important;
        color: #f44336 !important;
        border: 1px solid #f44336 !important;
    }
    
    .stWarning {
        background-color: #4f3d0d !important;
        color: #ff9800 !important;
        border: 1px solid #ff9800 !important;
    }
    
    .stInfo {
        background-color: #0d3d4f !important;
        color: #2196f3 !important;
        border: 1px solid #2196f3 !important;
    }
    
    /* Footer */
    .main .block-container div[data-testid="stMarkdownContainer"]:last-child {
        background-color: #252526 !important;
        padding: 1rem !important;
        border-radius: 4px !important;
        margin-top: 2rem !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e1e1e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #007acc;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #005a9e;
    }
    
    /* Additional Streamlit specific selectors */
    .stApp {
        background-color: #1e1e1e !important;
    }
    
    .stApp > header {
        background-color: #252526 !important;
    }
    
    /* Additional comprehensive text styling */
    .main .block-container *,
    .main *,
    .stMarkdown,
    .stMarkdown *,
    .stDataFrame,
    .stDataFrame *,
    .dataframe,
    .dataframe *,
    .stTable,
    .stTable *,
    table,
    table *,
    td,
    th,
    tr,
    .stSelectbox label,
    .stTextInput label,
    .stNumberInput label,
    .stButton label,
    .stForm label,
    .stRadio label,
    .stCheckbox label,
    .stSlider label,
    .stTextArea label,
    .stDateInput label,
    .stTimeInput label,
    .stFileUploader label,
    .stColorPicker label,
    .stMultiselect label,
    .stTextArea textarea,
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox select,
    .stMultiselect select,
    .stDateInput input,
    .stTimeInput input,
    .stFileUploader input,
    .stColorPicker input,
    .stSlider input,
    .stCheckbox input,
    .stRadio input,
    .stButton button,
    .stForm button,
    .stSuccess,
    .stError,
    .stWarning,
    .stInfo,
    .stSuccess *,
    .stError *,
    .stWarning *,
    .stInfo *,
    .stAlert,
    .stAlert *,
    .stExpander,
    .stExpander *,
    .stTabs,
    .stTabs *,
    .stContainer,
    .stContainer *,
    .stColumns,
    .stColumns *,
    .stColumn,
    .stColumn *,
    .stMetric,
    .stMetric *,
    .stProgress,
    .stProgress *,
    .stSpinner,
    .stSpinner *,
    .stEmpty,
    .stEmpty *,
    .stException,
    .stException *,
    .stHelp,
    .stHelp *,
    .stCaption,
    .stCaption *,
    .stCode,
    .stCode *,
    .stJson,
    .stJson *,
    .stPlotlyChart,
    .stPlotlyChart *,
    .stPyplot,
    .stPyplot *,
    .stAltairChart,
    .stAltairChart *,
    .stVegaLiteChart,
    .stVegaLiteChart *,
    .stGraphvizChart,
    .stGraphvizChart *,
    .stMap,
    .stMap *,
    .stDeckGlChart,
    .stDeckGlChart *,
    .stBokehChart,
    .stBokehChart *,
    .stPydeckChart,
    .stPydeckChart *,
    .stFoliumChart,
    .stFoliumChart *,
    .stImage,
    .stImage *,
    .stAudio,
    .stAudio *,
    .stVideo,
    .stVideo *,
    .stDownloadButton,
    .stDownloadButton *,
    .stLinkButton,
    .stLinkButton *,
    .stSidebar,
    .stSidebar *,
    .stSidebar .stSelectbox,
    .stSidebar .stSelectbox *,
    .stSidebar .stTextInput,
    .stSidebar .stTextInput *,
    .stSidebar .stNumberInput,
    .stSidebar .stNumberInput *,
    .stSidebar .stButton,
    .stSidebar .stButton *,
    .stSidebar .stRadio,
    .stSidebar .stRadio *,
    .stSidebar .stCheckbox,
    .stSidebar .stCheckbox *,
    .stSidebar .stSlider,
    .stSidebar .stSlider *,
    .stSidebar .stTextArea,
    .stSidebar .stTextArea *,
    .stSidebar .stDateInput,
    .stSidebar .stDateInput *,
    .stSidebar .stTimeInput,
    .stSidebar .stTimeInput *,
    .stSidebar .stFileUploader,
    .stSidebar .stFileUploader *,
    .stSidebar .stColorPicker,
    .stSidebar .stColorPicker *,
    .stSidebar .stMultiselect,
    .stSidebar .stMultiselect *,
    .stSidebar .stForm,
    .stSidebar .stForm *,
    .stSidebar .stAlert,
    .stSidebar .stAlert *,
    .stSidebar .stExpander,
    .stSidebar .stExpander *,
    .stSidebar .stTabs,
    .stSidebar .stTabs *,
    .stSidebar .stContainer,
    .stSidebar .stContainer *,
    .stSidebar .stColumns,
    .stSidebar .stColumns *,
    .stSidebar .stColumn,
    .stSidebar .stColumn *,
    .stSidebar .stMetric,
    .stSidebar .stMetric *,
    .stSidebar .stProgress,
    .stSidebar .stProgress *,
    .stSidebar .stSpinner,
    .stSidebar .stSpinner *,
    .stSidebar .stEmpty,
    .stSidebar .stEmpty *,
    .stSidebar .stException,
    .stSidebar .stException *,
    .stSidebar .stHelp,
    .stSidebar .stHelp *,
    .stSidebar .stCaption,
    .stSidebar .stCaption *,
    .stSidebar .stCode,
    .stSidebar .stCode *,
    .stSidebar .stJson,
    .stSidebar .stJson *,
    .stSidebar .stPlotlyChart,
    .stSidebar .stPlotlyChart *,
    .stSidebar .stPyplot,
    .stSidebar .stPyplot *,
    .stSidebar .stAltairChart,
    .stSidebar .stAltairChart *,
    .stSidebar .stVegaLiteChart,
    .stSidebar .stVegaLiteChart *,
    .stSidebar .stGraphvizChart,
    .stSidebar .stGraphvizChart *,
    .stSidebar .stMap,
    .stSidebar .stMap *,
    .stSidebar .stDeckGlChart,
    .stSidebar .stDeckGlChart *,
    .stSidebar .stBokehChart,
    .stSidebar .stBokehChart *,
    .stSidebar .stPydeckChart,
    .stSidebar .stPydeckChart *,
    .stSidebar .stFoliumChart,
    .stSidebar .stFoliumChart *,
    .stSidebar .stImage,
    .stSidebar .stImage *,
    .stSidebar .stAudio,
    .stSidebar .stAudio *,
    .stSidebar .stVideo,
    .stSidebar .stVideo *,
    .stSidebar .stDownloadButton,
    .stSidebar .stDownloadButton *,
    .stSidebar .stLinkButton,
    .stSidebar .stLinkButton * {
        color: #569cd6 !important;
    }
    
    
    
    
    
    /* Force text visibility in all containers */
    .main .block-container div,
    .main .block-container span,
    .main .block-container p,
    .main .block-container li,
    .main .block-container td,
    .main .block-container th {
        color: #569cd6 !important;
        background-color: transparent !important;
    }
    
    /* Add background color to specific Streamlit element */
    .st-emotion-cache-14vh5up {
        background-color: #1E1E1E; !important;
    }
    
    
</style>

<script>
// JavaScript to force styling after page load
document.addEventListener('DOMContentLoaded', function() {
    // Force white background on main content
    function forceWhiteBackground() {
        const mainElements = document.querySelectorAll('.main, .main .block-container, .main > div');
        mainElements.forEach(el => {
            el.style.backgroundColor = '#ffffff';
            el.style.color = '#569cd6';
        });
    }
    
    // Force DataFrame styling
    function styleDataFrames() {
        const dataFrames = document.querySelectorAll('.stDataFrame, .stDataFrameGlideDataEditor, .dvn-scroller, .dataframe, table');
        dataFrames.forEach(df => {
            df.style.backgroundColor = '#ffffff';
            df.style.color = '#000000';
            
            // Style all nested elements
            const allElements = df.querySelectorAll('*');
            allElements.forEach(el => {
                el.style.backgroundColor = '#ffffff';
            });
            
            // Style all table cells
            const cells = df.querySelectorAll('td, th, tr');
            cells.forEach(cell => {
                cell.style.backgroundColor = '#ffffff';
                cell.style.color = '#000000';
                cell.style.borderColor = '#dee2e6';
            });
        });
    }
    
    // Run immediately
    forceWhiteBackground();
    styleDataFrames();
    
    // Run after any Streamlit updates
    setTimeout(() => {
        forceWhiteBackground();
        styleDataFrames();
    }, 100);
    setTimeout(() => {
        forceWhiteBackground();
        styleDataFrames();
    }, 500);
    setTimeout(() => {
        forceWhiteBackground();
        styleDataFrames();
    }, 1000);
    
    // Use MutationObserver to catch dynamic updates
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                forceWhiteBackground();
                styleDataFrames();
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
</script>
""", unsafe_allow_html=True)

# Database connection function
def get_db_connection():
    """Create and return a database connection"""
    db_path = r"C:\Users\Naveen Anand\Downloads\Python\test\food_wastage.db"
    conn = sqlite3.connect(db_path)
    return conn

# Helper function to display results with custom styling
def display_results(df, title="Results"):
    """Display DataFrame results with custom styling"""
    st.markdown(f"### 📊 {title}")
    st.dataframe(df, use_container_width=True, hide_index=True)

# Sidebar navigation
st.sidebar.title("♻️ Waste Management System")
st.sidebar.markdown("---")

# Navigation options
nav_options = {
    "📋 Introduction": "intro",
    "📊 Database Tables": "tables", 
    "🔧 CRUD Operations": "crud",
    "📈 Analytics": "analytics"
}

selected_page = st.sidebar.radio("Navigate to:", list(nav_options.keys()))

# Introduction Page
if nav_options[selected_page] == "intro":
    st.title("🏠 Local Waste Management System")
    st.markdown("---")
    
    st.markdown("""
    ## 📋 Project Overview
    
    Welcome to the **Local Waste Management System** - a comprehensive platform designed to efficiently manage food waste and connect providers with receivers in local communities.
    
    ### 🎯 Key Features:
    
    - **Provider Management**: Track food providers across different cities
    - **Receiver Management**: Manage organizations and individuals who can receive food donations
    - **Food Listings**: Catalog available food items with detailed information
    - **Claims System**: Handle food donation claims and track their status
    - **Analytics Dashboard**: Comprehensive insights into waste management patterns
    
    ### 🏗️ System Architecture:
    
    The system utilizes a SQLite database with four main tables:
    
    1. **Providers** - Stores information about food providers (restaurants, cafes, etc.)
    2. **Receivers** - Contains data about organizations that can receive food donations
    3. **Food Listings** - Details about available food items
    4. **Claims** - Tracks donation claims and their processing status
    
    ### 🌟 Benefits:
    
    - Reduces food waste in local communities
    - Connects surplus food with those in need
    - Provides data-driven insights for better resource management
    - Streamlines the donation process
    - Tracks impact and effectiveness of waste reduction efforts
    
    ### 📊 Data Insights:
    
    The system provides comprehensive analytics including:
    - Geographic distribution of providers and receivers
    - Most popular food types and quantities
    - Claim success rates and patterns
    - Provider performance metrics
    - Community impact measurements
    
    ---
    
    **Navigate using the sidebar to explore different sections of the system.**
    """)

# Database Tables Page
elif nav_options[selected_page] == "tables":
    st.title("📊 Database Tables")
    st.markdown("---")
    
    # Table selection dropdown
    table_options = {
        "Providers": "providers",
        "Receivers": "receivers", 
        "Claims": "claims",
        "Food Listings": "food_listings"
    }
    
    selected_table = st.selectbox("Select a table to view:", list(table_options.keys()))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get table data
        table_name = table_options[selected_table]
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]
        
        if result:
            # Convert to DataFrame
            df = pd.DataFrame(result, columns=column_names)
            
            st.subheader(f"📋 {selected_table} Table")
            st.markdown(f"**Total Records:** {len(df)}")
            
            # Display the table with custom styling
            display_results(df, f"{selected_table} Data")
            
            # Show basic statistics
            st.subheader("📈 Table Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Records", len(df))
            
            with col2:
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    st.metric("Numeric Columns", len(numeric_cols))
                else:
                    st.metric("Numeric Columns", 0)
            
            with col3:
                st.metric("Text Columns", len(df.select_dtypes(include=['object']).columns))
            
        else:
            st.warning(f"No data found in the {selected_table} table.")
            
        conn.close()
        
    except Exception as e:
        st.error(f"Error accessing database: {str(e)}")
        st.info("Make sure the 'food_wastage.db' file exists in the same directory as this app.")

# CRUD Operations Page
elif nav_options[selected_page] == "crud":
    st.title("🔧 CRUD Operations")
    st.markdown("---")
    
    # Table selection for CRUD operations
    crud_table_options = {
        "Providers": "providers",
        "Receivers": "receivers",
        "Claims": "claims", 
        "Food Listings": "food_listings"
    }
    
    crud_selected_table = st.selectbox("Select table for operations:", list(crud_table_options.keys()))
    table_name = crud_table_options[crud_selected_table]
    
    # Operation selection
    operation = st.radio("Select operation:", ["Create", "Read", "Update", "Delete"])
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if operation == "Read":
            st.subheader(f"📖 Read {crud_selected_table}")
            
            # Get all data
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            
            if result:
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns_info = cursor.fetchall()
                column_names = [col[1] for col in columns_info]
                
                df = pd.DataFrame(result, columns=column_names)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No records found.")
        
        elif operation == "Create":
            st.subheader(f"➕ Create New {crud_selected_table} Record")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            
            # Create form for new record
            with st.form(f"create_{table_name}"):
                form_data = {}
                for col in columns_info:
                    col_name = col[1]
                    col_type = col[2]
                    
                    if "INTEGER" in col_type.upper():
                        form_data[col_name] = st.number_input(f"{col_name}:", value=0)
                    elif "TEXT" in col_type.upper():
                        form_data[col_name] = st.text_input(f"{col_name}:")
                    elif "REAL" in col_type.upper():
                        form_data[col_name] = st.number_input(f"{col_name}:", value=0.0)
                    else:
                        form_data[col_name] = st.text_input(f"{col_name}:")
                
                submitted = st.form_submit_button("Create Record")
                
                if submitted:
                    try:
                        columns = list(form_data.keys())
                        values = list(form_data.values())
                        placeholders = ", ".join(["?" for _ in values])
                        
                        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                        cursor.execute(query, values)
                        conn.commit()
                        st.success(f"Record created successfully in {crud_selected_table}!")
                    except Exception as e:
                        st.error(f"Error creating record: {str(e)}")
        
        elif operation == "Update":
            st.subheader(f"✏️ Update {crud_selected_table} Record")
            
            # Get existing records for selection
            cursor.execute(f"SELECT * FROM {table_name}")
            existing_records = cursor.fetchall()
            
            if existing_records:
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns_info = cursor.fetchall()
                column_names = [col[1] for col in columns_info]
                
                df = pd.DataFrame(existing_records, columns=column_names)
                
                # Let user select a record to update
                selected_index = st.selectbox("Select record to update:", range(len(df)), 
                                            format_func=lambda x: f"Record {x+1}")
                
                if selected_index is not None:
                    selected_record = df.iloc[selected_index]
                    
                    with st.form(f"update_{table_name}"):
                        st.write("**Current Values:**")
                        for col in column_names:
                            st.write(f"{col}: {selected_record[col]}")
                        
                        st.write("**New Values:**")
                        update_data = {}
                        for col in columns_info:
                            col_name = col[1]
                            col_type = col[2]
                            
                            if "INTEGER" in col_type.upper():
                                update_data[col_name] = st.number_input(f"New {col_name}:", 
                                                                       value=int(selected_record[col_name]))
                            elif "TEXT" in col_type.upper():
                                update_data[col_name] = st.text_input(f"New {col_name}:", 
                                                                     value=str(selected_record[col_name]))
                            elif "REAL" in col_type.upper():
                                update_data[col_name] = st.number_input(f"New {col_name}:", 
                                                                       value=float(selected_record[col_name]))
                            else:
                                update_data[col_name] = st.text_input(f"New {col_name}:", 
                                                                     value=str(selected_record[col_name]))
                        
                        submitted = st.form_submit_button("Update Record")
                        
                        if submitted:
                            try:
                                # Build UPDATE query
                                set_clause = ", ".join([f"{col} = ?" for col in column_names])
                                query = f"UPDATE {table_name} SET {set_clause} WHERE rowid = ?"
                                
                                values = list(update_data.values()) + [selected_index + 1]
                                cursor.execute(query, values)
                                conn.commit()
                                st.success("Record updated successfully!")
                            except Exception as e:
                                st.error(f"Error updating record: {str(e)}")
            else:
                st.info("No records found to update.")
        
        elif operation == "Delete":
            st.subheader(f"🗑️ Delete {crud_selected_table} Record")
            
            # Get existing records
            cursor.execute(f"SELECT * FROM {table_name}")
            existing_records = cursor.fetchall()
            
            if existing_records:
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns_info = cursor.fetchall()
                column_names = [col[1] for col in columns_info]
                
                df = pd.DataFrame(existing_records, columns=column_names)
                
                # Let user select a record to delete
                selected_index = st.selectbox("Select record to delete:", range(len(df)),
                                            format_func=lambda x: f"Record {x+1}")
                
                if selected_index is not None:
                    selected_record = df.iloc[selected_index]
                    
                    st.write("**Record to be deleted:**")
                    st.dataframe(selected_record.to_frame().T)
                    
                    if st.button("Confirm Delete", type="primary"):
                        try:
                            query = f"DELETE FROM {table_name} WHERE rowid = ?"
                            cursor.execute(query, [selected_index + 1])
                            conn.commit()
                            st.success("Record deleted successfully!")
                        except Exception as e:
                            st.error(f"Error deleting record: {str(e)}")
            else:
                st.info("No records found to delete.")
        
        conn.close()
        
    except Exception as e:
        st.error(f"Error accessing database: {str(e)}")

# Analytics Page
elif nav_options[selected_page] == "analytics":
    st.title("📈 Analytics Dashboard")
    st.markdown("---")
    
    # Question selection dropdown
    question_options = {
        "Question 1: Providers and receivers by city": 1,
        "Question 2: Provider type with highest quantity": 2,
        "Question 3: Contact details in New Jessica": 3,
        "Question 4: Receiver with most claims": 4,
        "Question 5: Total quantity by provider": 5,
        "Question 6: City with most food listings": 6,
        "Question 7: Most popular food items": 7,
        "Question 8: Food items with most claims": 8,
        "Question 9: Provider with most completed claims": 9,
        "Question 10: Distribution of claim statuses": 10,
        "Question 11: Average claimed quantity per receiver": 11,
        "Question 12: Meal type with most claims": 12,
        "Question 13: Total quantity by provider (ordered)": 13,
        "Question 14: City with highest total claimed quantity": 14,
        "Question 15: Food items claimed by the most receivers": 15,
        "Question 16: Completed claims percentage split by meal type": 16,
        "Question 17: Receiver claim success rate": 17,
        "Question 18: Food types mostly pending": 18,
        "Question 19: City with highest number of providers": 19
    }
    
    selected_question = st.selectbox("Select a question to analyze:", list(question_options.keys()))
    question_num = question_options[selected_question]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if question_num == 1:
            st.subheader("1️⃣ How many food providers and receivers are there in each city?")
            query1 = """
            SELECT
            COALESCE(p.City, r.City) AS City,
            COUNT(DISTINCT p.provider_id) AS provider_count,
            COUNT(DISTINCT r.receiver_id) AS receiver_count
            FROM providers p
            FULL OUTER JOIN receivers r
                ON p.City = r.City
            GROUP BY COALESCE(p.City, r.City)
            ORDER BY City;
            """
            cursor.execute(query1)
            result1 = cursor.fetchall()
            df1 = pd.DataFrame(result1, columns=["City", "provider_count", "receiver_count"])
            
            # Display with custom styling
            display_results(df1, "City-wise Provider and Receiver Counts")
            
            # Add visualization
            if not df1.empty:
                st.subheader("📊 Visualization")
                chart_data = df1.set_index('City')[['provider_count', 'receiver_count']]
                st.bar_chart(chart_data)
        
        elif question_num == 2:
            st.subheader("2️⃣ Which provider type has the highest total quantity?")
            query2 = """
            SELECT 
            provider_type,
            SUM(quantity) AS total_quantity
            FROM food_listings
            GROUP BY provider_type order by total_quantity DESC LIMIT 1;
            """
            cursor.execute(query2)
            result2 = cursor.fetchall()
            df2 = pd.DataFrame(result2, columns=["Provider_Type", "total_quantity"])
            
            # Display with custom styling
            display_results(df2, "Provider Type with Highest Quantity")
            
            # Add visualization
            if not df2.empty:
                st.subheader("📊 Visualization")
                chart_data = df2.set_index('Provider_Type')['total_quantity']
                st.bar_chart(chart_data)
        
        elif question_num == 3:
            st.subheader("3️⃣ What are the contact details of providers in New Jessica?")
            query3 = """
            SELECT City, Contact from providers where City == "New Jessica"
            """
            cursor.execute(query3)
            result3 = cursor.fetchall()
            df3 = pd.DataFrame(result3, columns=["City", "Contact"])
            display_results(df3, "Contact Details in New Jessica")
        
        elif question_num == 4:
            st.subheader("4️⃣ Which receiver has the most claims?")
            query4 = """
            WITH claim_counts AS (
                SELECT 
                    r.Receiver_ID,
                    r.Name,
                    COUNT(c.Claim_ID) AS claim_count
                FROM 
                    receivers r
                LEFT JOIN 
                    claims c
                ON 
                    r.Receiver_ID = c.Receiver_ID
                GROUP BY 
                    r.Receiver_ID, r.Name
            )
            SELECT *
            FROM claim_counts
            WHERE claim_count = (
                SELECT MAX(claim_count) FROM claim_counts
            );
            """
            cursor.execute(query4)
            result4 = cursor.fetchall()
            df4 = pd.DataFrame(result4, columns=["Receiver_ID", "Name", "claim_count"])
            display_results(df4, "Receiver with Most Claims")
        
        elif question_num == 5:
            st.subheader("5️⃣ What is the total quantity provided by each provider?")
            query5 = """
            SELECT 
                f.provider_id,
                p.Name,
                SUM(f.quantity) AS total_quantity
            FROM 
                food_listings f
            JOIN 
                providers p
            ON 
                f.provider_id = p.provider_id
            GROUP BY 
                f.provider_id, p.Name;
            """
            cursor.execute(query5)
            result5 = cursor.fetchall()
            df5 = pd.DataFrame(result5, columns=["Provider_ID", "Name", "total_quantity"])
            display_results(df5, "Total Quantity by Provider")
            
            # Add visualization
            if not df5.empty:
                st.subheader("📊 Visualization")
                chart_data = df5.set_index('Name')['total_quantity']
                st.bar_chart(chart_data)
        
        elif question_num == 6:
            st.subheader("6️⃣ Which city has the most food listings?")
            query6 = """
            WITH location_counts AS (
                SELECT 
                    Location as city,
                    COUNT(*) AS listing_count
                FROM 
                    food_listings
                GROUP BY 
                    Location
            )
            SELECT *
            FROM location_counts
            WHERE listing_count = (
                SELECT MAX(listing_count) 
                FROM location_counts
            );
            """
            cursor.execute(query6)
            result6 = cursor.fetchall()
            df6 = pd.DataFrame(result6, columns=["city", "listing_count"])
            display_results(df6, "City with Most Food Listings")
        
        elif question_num == 7:
            st.subheader("7️⃣ What are the most popular food items by listing count?")
            query7 = """
            SELECT 
                Food_Name,
                COUNT(*) AS listing_count,
                SUM(Quantity) AS total_quantity
            FROM 
                food_listings
            GROUP BY 
                Food_Name
            ORDER BY 
                listing_count DESC;
            """
            cursor.execute(query7)
            result7 = cursor.fetchall()
            df7 = pd.DataFrame(result7, columns=["Food_Name", "listing_count", "total_quantity"])
            display_results(df7, "Most Popular Food Items")
            
            # Add visualization
            if not df7.empty:
                st.subheader("📊 Visualization")
                chart_data = df7.set_index('Food_Name')['listing_count']
                st.bar_chart(chart_data)
        
        elif question_num == 8:
            st.subheader("8️⃣ Which food items have the most claims?")
            query8 = """
            SELECT 
                f.Food_Name,
                COUNT(*) AS claim_count
            FROM 
                claims c
            JOIN 
                food_listings f
            ON 
                c.Food_ID = f.Food_ID
            GROUP BY 
                f.Food_Name;
            """
            cursor.execute(query8)
            result8 = cursor.fetchall()
            df8 = pd.DataFrame(result8, columns=["Food_Name", "claim_count"])
            display_results(df8, "Food Items with Most Claims")
            
            # Add visualization
            if not df8.empty:
                st.subheader("📊 Visualization")
                chart_data = df8.set_index('Food_Name')['claim_count']
                st.bar_chart(chart_data)
        
        elif question_num == 9:
            st.subheader("9️⃣ Which provider has the most completed claims?")
            query9 = """
            WITH completed_counts AS (
                SELECT 
                    f.Provider_ID,
                    COUNT(*) AS completed_claims
                FROM 
                    food_listings f
                JOIN 
                    claims c
                    ON f.Food_ID = c.Food_ID
                WHERE 
                    c.Status = 'Completed'
                GROUP BY 
                    f.Provider_ID
            )
            SELECT 
                p.Provider_ID,
                p.Name,
                cc.completed_claims
            FROM 
                completed_counts cc
            JOIN 
                providers p
                ON cc.Provider_ID = p.Provider_ID
            WHERE 
                cc.completed_claims = (
                    SELECT MAX(completed_claims) FROM completed_counts
                );
            """
            cursor.execute(query9)
            result9 = cursor.fetchall()
            df9 = pd.DataFrame(result9, columns=["Provider_ID", "Name", "completed_claims"])
            display_results(df9, "Provider with Most Completed Claims")
        
        elif question_num == 10:
            st.subheader("🔟 What is the distribution of claim statuses?")
            query10 = """
            SELECT 
                Status,
                COUNT(*) AS claim_count,
                ROUND( (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims)), 2 ) AS percentage
            FROM 
                claims
            GROUP BY 
                Status;
            """
            cursor.execute(query10)
            result10 = cursor.fetchall()
            df10 = pd.DataFrame(result10, columns=["Status", "claim_count", "percentage"])
            display_results(df10, "Claim Status Distribution")
            
            # Add visualization
            if not df10.empty:
                st.subheader("📊 Visualization")
                chart_data = df10.set_index('Status')['claim_count']
                st.bar_chart(chart_data)
        
        elif question_num == 11:
            st.subheader("1️⃣1️⃣ What is the average claimed quantity per receiver?")
            query11 = """
            SELECT 
                r.Receiver_ID,
                r.Name,
                ROUND(AVG(f.Quantity), 2) AS avg_claimed_quantity
            FROM 
                claims c
            JOIN 
                food_listings f
                ON c.Food_ID = f.Food_ID
            JOIN 
                receivers r
                ON c.Receiver_ID = r.Receiver_ID
            GROUP BY 
                r.Receiver_ID, r.Name;
            """
            cursor.execute(query11)
            result11 = cursor.fetchall()
            df11 = pd.DataFrame(result11, columns=["Receiver_ID", "Name", "avg_claimed_quantity"])
            display_results(df11, "Average Claimed Quantity per Receiver")
            
            # Add visualization
            if not df11.empty:
                st.subheader("📊 Visualization")
                chart_data = df11.set_index('Name')['avg_claimed_quantity']
                st.bar_chart(chart_data)
        
        elif question_num == 12:
            st.subheader("1️⃣2️⃣ Which meal type has the most claims?")
            query12 = """
            SELECT 
                f.Meal_Type,
                COUNT(c.Claim_ID) AS claim_count
            FROM 
                claims c
            JOIN 
                food_listings f
                ON c.Food_ID = f.Food_ID
            GROUP BY 
                f.Meal_Type
            ORDER BY 
                claim_count DESC
            LIMIT 1;
            """
            cursor.execute(query12)
            result12 = cursor.fetchall()
            df12 = pd.DataFrame(result12, columns=["Meal_Type", "claim_count"])
            display_results(df12, "Meal Type with Most Claims")
        
        elif question_num == 13:
            st.subheader("1️⃣3️⃣ What is the total quantity provided by each provider (ordered by provider ID)?")
            query13 = """
            SELECT 
                f.Provider_ID,
                p.Name,
                SUM(f.Quantity) AS total_quantity
            FROM 
                food_listings f
            JOIN 
                providers p
                ON f.Provider_ID = p.Provider_ID
            GROUP BY 
                f.Provider_ID, p.Name
            ORDER BY 
                p.Provider_ID;
            """
            cursor.execute(query13)
            result13 = cursor.fetchall()
            df13 = pd.DataFrame(result13, columns=["Provider_ID", "Name", "total_quantity"])
            display_results(df13, "Total Quantity by Provider (Ordered)")
            
            # Add visualization
            if not df13.empty:
                st.subheader("📊 Visualization")
                chart_data = df13.set_index('Name')['total_quantity']
                st.bar_chart(chart_data)
        
        elif question_num == 14:
            st.subheader("1️⃣4️⃣ Which city has received the highest total quantity of claimed food?")
            query14 = """
            SELECT 
                r.City,
                SUM(f.Quantity) AS total_claimed_quantity
            FROM 
                claims c
            JOIN 
                receivers r
                ON c.Receiver_ID = r.Receiver_ID
            JOIN 
                food_listings f
                ON c.Food_ID = f.Food_ID
            GROUP BY 
                r.City
            ORDER BY 
                total_claimed_quantity DESC
            LIMIT 1;
            """
            cursor.execute(query14)
            result14 = cursor.fetchall()
            df14 = pd.DataFrame(result14, columns=["City","total_claimed_quantity"])
            display_results(df14, "City with Highest Total Claimed Quantity")
        
        elif question_num == 15:
            st.subheader("1️⃣5️⃣ Which food items have been claimed by the most receivers?")
            query15 = """
            SELECT 
                f.Food_Name,
                COUNT(DISTINCT c.Receiver_ID) AS unique_receivers
            FROM 
                claims c
            JOIN 
                food_listings f
                ON c.Food_ID = f.Food_ID
            GROUP BY 
                f.Food_Name
            ORDER BY 
                unique_receivers DESC;
            """
            cursor.execute(query15)
            result15 = cursor.fetchall()
            df15 = pd.DataFrame(result15, columns=["Food_Name","unique_receivers"])
            display_results(df15, "Food Items Claimed by the Most Receivers")
            
            if not df15.empty:
                st.subheader("📊 Visualization")
                chart_data = df15.set_index('Food_Name')['unique_receivers']
                st.bar_chart(chart_data)
        
        elif question_num == 16:
            st.subheader("1️⃣6️⃣ For completed claims — percentage split by meal type")
            query16 = """
            WITH completed AS (
              SELECT c.Claim_ID, f.Meal_Type
              FROM claims c
              JOIN food_listings f ON c.Food_ID = f.Food_ID
              WHERE c.Status = 'Completed'
            )
            SELECT
              Meal_Type,
              COUNT(*) AS count_completed,
              ROUND( (COUNT(*) * 100.0) / (SELECT COUNT(*) FROM completed), 2) AS percentage_of_completed
            FROM completed
            GROUP BY Meal_Type
            ORDER BY count_completed DESC;
            """
            cursor.execute(query16)
            result16 = cursor.fetchall()
            df16 = pd.DataFrame(result16, columns=["Meal_Type","count_completed","percentage_of_completed"])
            display_results(df16, "Completed Claims Percentage by Meal Type")
            
            if not df16.empty:
                st.subheader("📊 Visualization")
                chart_data = df16.set_index('Meal_Type')['count_completed']
                st.bar_chart(chart_data)
        
        elif question_num == 17:
            st.subheader("1️⃣7️⃣ Receiver claim success rate")
            query17 = """
            SELECT 
                r.Receiver_ID,
                r.Name,
                ROUND(
                    (SUM(CASE WHEN c.Status = 'Completed' THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 
                    2
                ) AS success_rate_percent
            FROM 
                claims c
            JOIN 
                receivers r
                ON c.Receiver_ID = r.Receiver_ID
            GROUP BY 
                r.Receiver_ID, r.Name;
            """
            cursor.execute(query17)
            result17 = cursor.fetchall()
            df17 = pd.DataFrame(result17, columns=["Receiver_ID","Name","success_rate_percent"])
            display_results(df17, "Receiver Claim Success Rate")
            
            if not df17.empty:
                st.subheader("📊 Visualization")
                chart_data = df17.set_index('Name')['success_rate_percent']
                st.bar_chart(chart_data)
        
        elif question_num == 18:
            st.subheader("1️⃣8️⃣ Food types that are mostly pending")
            query18 = """
            SELECT 
                f.Food_Type,
                COUNT(*) AS pending_count
            FROM claims c
            JOIN food_listings f ON c.Food_ID = f.Food_ID
            WHERE c.Status = 'Pending'
            GROUP BY f.Food_Type
            ORDER BY pending_count DESC;
            """
            cursor.execute(query18)
            result18 = cursor.fetchall()
            df18 = pd.DataFrame(result18, columns=["Food_Type","pending_count"])
            display_results(df18, "Food Types Mostly Pending")
            
            if not df18.empty:
                st.subheader("📊 Visualization")
                chart_data = df18.set_index('Food_Type')['pending_count']
                st.bar_chart(chart_data)
        
        elif question_num == 19:
            st.subheader("1️⃣9️⃣ City with the highest number of providers")
            query19 = """
                SELECT City, COUNT(*) AS Provider_Count
                FROM providers
                GROUP BY City
                ORDER BY Provider_Count DESC
                LIMIT 1;
            """
            cursor.execute(query19)
            result19 = cursor.fetchall()
            df19 = pd.DataFrame(result19, columns=["City", "Provider_Count"])
            display_results(df19, "City with Highest Number of Providers")
        
        conn.close()
        
    except Exception as e:
        st.error(f"Error accessing database: {str(e)}")
        st.info("Make sure the 'food_wastage.db' file exists in the same directory as this app.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>♻️ Local Waste Management System | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
