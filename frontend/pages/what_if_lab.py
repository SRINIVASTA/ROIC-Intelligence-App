import os
import streamlit as st
import pdfplumber
import re
import duckdb
import pandas as pd

# Standardise path to the data storage file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "lakehouse.db")

st.title("🧪 Scenario Analytics Lab")
st.caption("Perform modifications, scenario commits, or load unstructured PDF updates.")
st.divider()

# FAIL-SAFE REPAIR: If the database connection drops from state, reconnect on the fly
if "duckdb_conn" not in st.session_state:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    st.session_state.duckdb_conn = duckdb.connect(database=DB_PATH)

conn = st.session_state.duckdb_conn

# Ensure tables are initialized safely
conn.execute("""
    CREATE TABLE IF NOT EXISTS gold_roic_ledger (
        scenario_name VARCHAR,
        capex_billion DOUBLE,
        roic_percent DOUBLE,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

uploaded_file = st.file_uploader("Upload analyst document inputs", type="pdf")
base_capex, base_roic = 357.5, 29.7

if uploaded_file is not None:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            txt = "\n".join([p.extract_text() or "" for p in pdf.pages])
            c_match = re.search(r'\$?(\d+(?:\.\d+)?)\s*B\s+capex', txt, re.IGNORECASE)
            r_match = re.search(r'(\d+(?:\.\d+)?)\s*%\s*ROIC', txt, re.IGNORECASE)
            if c_match: base_capex = float(c_match.group(1))
            if r_match: base_roic = float(r_match.group(1))
        st.success("Variables parsed from document input successfully!")
    except Exception as e:
        st.error(f"Data pipeline file parsing exception: {e}")

with st.form("scenario_form"):
    label = st.text_input("New Scenario Operation Name", value="Simulation Run Pro")
    multiplier = st.slider("Scale Multiplier Factor (Capex)", 0.5, 2.5, 1.0, 0.1)
    shift = st.slider("Hurdle Shift (ROIC Percentage Points)", -10.0, 15.0, 0.0, 0.5)
    
    if st.form_submit_button("Commit Transaction to Lakehouse"):
        conn.execute(
            "INSERT INTO gold_roic_ledger (scenario_name, capex_billion, roic_percent) VALUES (?, ?, ?)", 
            (label, round(base_capex * multiplier, 1), round(base_roic + shift, 1))
        )
        st.success(f"Committed: '{label}' to Gold warehouse table!")

st.subheader("📋 Historic Audit Trail")

# Safely extract historical rows
try:
    log_df = conn.execute("""
        SELECT scenario_name AS "Scenario Name", 
               capex_billion AS "Capex ($B)", 
               roic_percent AS "ROIC (%)", 
               timestamp AS "Committed Timestamp" 
        FROM gold_roic_ledger 
        ORDER BY timestamp DESC
    """).df()
except Exception:
    log_df = pd.DataFrame(columns=["Scenario Name", "Capex ($B)", "ROIC (%)", "Committed Timestamp"])

st.dataframe(log_df, hide_index=True, width="stretch")

if not log_df.empty:
    csv_data = log_df.to_csv(index=False).encode('utf-8')
    st.write("")
    st.download_button(
        label="📥 Download Audit Ledger Spreadsheet (.CSV)", 
        data=csv_data, 
        file_name="roic_ledger.csv", 
        mime="text/csv", 
        width="stretch"
    )
