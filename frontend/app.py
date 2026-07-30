import os
import streamlit as st
import duckdb

st.set_page_config(page_title="ROIC Intelligence Platform", layout="wide")

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "lakehouse.db"))

# Initialize a single persistent global connection inside session state
if 'duckdb_conn' not in st.session_state:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # FIXED: DuckDB connect without the sqlite3-specific parameter
    st.session_state.duckdb_conn = duckdb.connect(database=DB_PATH)
    
    # Initialize Schema Tables
    st.session_state.duckdb_conn.execute("""
        CREATE TABLE IF NOT EXISTS gold_roic_ledger (
            scenario_name VARCHAR,
            capex_billion DOUBLE,
            roic_percent DOUBLE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Seed baseline entry if ledger is empty
    count = st.session_state.duckdb_conn.execute("SELECT COUNT(*) FROM gold_roic_ledger").fetchone()[0]
    if count == 0:
        st.session_state.duckdb_conn.execute("""
            INSERT INTO gold_roic_ledger (scenario_name, capex_billion, roic_percent) 
            VALUES ('Morgan Stanley Baseline', 357.5, 29.7)
        """)

# Define Dashboard Navigation Map
pages = {
    "ROIC Intelligence": [
        st.Page("pages/1_📖_Executive_Story.py", title="📖 Executive Story", default=True),
        st.Page("pages/2_🏢_Company_Lens.py", title="🏢 Company Lens"),
        st.Page("pages/3_🧪_What_If_Lab.py", title="🧪 What-If Lab"),
    ]
}

pg = st.navigation(pages)
pg.run()
