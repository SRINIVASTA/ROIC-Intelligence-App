import os
import streamlit as st
import pdfplumber
import re

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "lakehouse.db"))

st.title("🧪 Scenario Analytics Lab")
st.caption("Perform modifications, scenario commits, or load unstructured PDF updates.")
st.divider()

uploaded_file = st.file_uploader("Upload analyst document inputs", type="pdf")

# Standard base parameters (Fallbacks)
base_capex = 357.5
base_roic = 29.7

if uploaded_file is not None:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            txt = "\n".join([p.extract_text() or "" for p in pdf.pages])
            
            # 1. Look for specialized Morgan Stanley case study anchors (e.g., NOPAT of $70 billion)
            nopat_match = re.search(r'NOPAT\s*(?:of|is)?\s*\$?(\d+(?:\.\d+)?)\s*B(?:illion)?', txt, re.IGNORECASE)
            ebit_match = re.search(r'EBITA\s*(?:of|is)?\s*\$?(\d+(?:\.\d+)?)\s*B(?:illion)?', txt, re.IGNORECASE)
            
            # 2. Look for ROIC patterns in text blocks or tables
            roic_match = re.search(r'ROIC\s*(?:was|is)?\s*(\d+(?:\.\d+)?)\s*%\s*', txt, re.IGNORECASE)
            
            # Update baseline variables if explicit matches are parsed
            if nopat_match:
                # Map parsed NOPAT directly into our core analytical scale baseline
                base_capex = float(nopat_match.group(1))
                st.info(f"📈 Found Report Case-Study NOPAT Asset Anchor: ${base_capex}B")
            elif ebit_match:
                base_capex = float(ebit_match.group(1))
                st.info(f"📈 Found Report Case-Study EBITA Asset Anchor: ${base_capex}B")
                
            if roic_match:
                base_roic = float(roic_match.group(1))
                st.info(f"📊 Found Report Target Efficiency Metric: {base_roic}%")
                
            st.success("Variables parsed from document input successfully!")
            
    except Exception as e:
        st.error(f"Error reading structure from file mapping: {e}")

with st.form("scenario_form"):
    label = st.text_input("New Scenario Operation Name", value="Morgan Stanley Case Analysis")
    multiplier = st.slider("Scale Multiplier Factor (Capex / NOPAT Anchor)", 0.5, 2.5, 1.0, 0.1)
    shift = st.slider("Hurdle Shift (ROIC Percentage Points)", -10.0, 15.0, 0.0, 0.5)
    
    if st.form_submit_button("Commit Transaction to Lakehouse"):
        final_c = base_capex * multiplier
        final_r = base_roic + shift
        
        st.session_state.duckdb_conn.execute(
            "INSERT INTO gold_roic_ledger (scenario_name, capex_billion, roic_percent) VALUES (?, ?, ?)", 
            (label, round(final_c, 1), round(final_r, 1))
        )
        st.success(f"Committed scenario layout variant: '{label}' to Gold warehouse table!")

st.subheader("📋 Historic Audit Trail")
log_df = st.session_state.duckdb_conn.execute("SELECT scenario_name, capex_billion, roic_percent, timestamp FROM gold_roic_ledger ORDER BY timestamp DESC").df()
st.dataframe(log_df, use_container_width=True, hide_index=True)
