import os
import streamlit as st
import duckdb

st.set_page_config(page_title="ROIC Intelligence Platform", layout="wide")

# Determine base execution directory setups cleanly
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "lakehouse.db")

def verify_and_get_connection():
    if 'duckdb_conn' not in st.session_state:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        st.session_state.duckdb_conn = duckdb.connect(database=DB_PATH)
        
        # SYSTEM FIX: Drop the old limited table design to force a clean multi-column rebuild
        st.session_state.duckdb_conn.execute("DROP TABLE IF EXISTS gold_roic_ledger")
        
        # Re-initialize Core Gold ledger tracking schemas with company tracking column extensions built in
        st.session_state.duckdb_conn.execute("""
            CREATE TABLE IF NOT EXISTS gold_roic_ledger (
                scenario_name VARCHAR,
                capex_billion DOUBLE,
                roic_percent DOUBLE,
                msft_roic DOUBLE,
                gcp_roic DOUBLE,
                aws_roic DOUBLE,
                meta_roic DOUBLE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Seed baseline entry direct with separate corporate values matching historical vectors
        st.session_state.duckdb_conn.execute("""
            INSERT INTO gold_roic_ledger (scenario_name, capex_billion, roic_percent, msft_roic, gcp_roic, aws_roic, meta_roic) 
            VALUES ('Morgan Stanley Baseline', 357.5, 29.7, 32.4, 28.1, 31.0, 24.5)
        """)
    return st.session_state.duckdb_conn

# Initialize connection immediately on primary boot
conn = verify_and_get_connection()

# Clear multi-page page routing structure mappings
pages = {
    "ROIC Intelligence": [
        st.Page("pages/executive_story.py", title="📖 Executive Story", default=True),
        st.Page("pages/company_lens.py", title="🏢 Company Lens"),
        st.Page("pages/what_if_lab.py", title="🧪 What-If Lab"),
    ]
}

pg = st.navigation(pages)
pg.run()
