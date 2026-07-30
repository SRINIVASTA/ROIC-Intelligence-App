import os
import streamlit as st
import pdfplumber
import re
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("🧪 Scenario Analytics Lab")
st.caption("Perform modifications, scenario commits, or load unstructured PDF updates.")
st.divider()

if "duckdb_conn" not in st.session_state:
    st.error("🔌 Database engine connection offline.")
else:
    conn = st.session_state.duckdb_conn
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
            st.success("Variables parsed successfully!")
        except Exception as e:
            st.error(f"Parsing exception: {e}")

    with st.form("scenario_form"):
        label = st.text_input("New Scenario Operation Name", value="Simulation Run Pro")
        multiplier = st.slider("Scale Multiplier Factor (Capex)", 0.5, 2.5, 1.0, 0.1)
        shift = st.slider("Hurdle Shift (ROIC Percentage Points)", -10.0, 15.0, 0.0, 0.5)
        
        final_capex = round(base_capex * multiplier, 1)
        final_roic = round(base_roic + shift, 1)
        
        if st.form_submit_button("Commit Transaction to Lakehouse"):
            conn.execute(
                "INSERT INTO gold_roic_ledger (scenario_name, capex_billion, roic_percent) VALUES (?, ?, ?)", 
                (label, final_capex, final_roic)
            )
            st.success(f"Committed: '{label}' successfully!")

    st.subheader("📋 Historic Audit Trail")
    try:
        log_df = conn.execute('SELECT scenario_name AS "Scenario Name", capex_billion AS "Capex ($B)", roic_percent AS "ROIC (%)", timestamp AS "Committed Timestamp" FROM gold_roic_ledger ORDER BY timestamp DESC').df()
    except Exception:
        log_df = pd.DataFrame()

    st.dataframe(log_df, hide_index=True)

    # DYNAMIC EXPORT REPAIR: If logs exist, create a downloadable image slide card
    if not log_df.empty:
        st.write("---")
        st.subheader("🖼️ Executive Presentation Export Hub")
        st.markdown("Generate and download a stylized visual snapshot summary card of the most recent modeling metrics for slide decks.")
        
        # Pull the absolute freshest row committed to the database
        latest_scenario = log_df.iloc[0]["Scenario Name"]
        latest_capex = log_df.iloc[0]["Capex ($B)"]
        latest_roic = log_df.iloc[0]["ROIC (%)"]
        
        # Build a programmatic clean image card using matplotlib
        fig, ax = plt.subplots(figsize=(7, 4.5))
        fig.patch.set_facecolor('#0d231d') # Deep green brand color matching Executive Story
        ax.set_facecolor('#0d231d')
        
        # Hide standard chart axes boundaries to keep the card design crisp
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        
        # Write clean layout presentation strings onto the image canvas
        ax.text(0.05, 0.85, "ROIC INTELLIGENCE PLATFORM", color='#2e7d32', fontsize=11, fontweight='bold', alpha=0.9)
        ax.text(0.05, 0.73, f"SCENARIO: {latest_scenario.upper()}", color='#ffffff', fontsize=18, fontweight='bold')
        
        ax.text(0.05, 0.50, "HYPERSCALE CASH CAPEX", color='#ffffff', fontsize=9, alpha=0.7, fontweight='bold')
        ax.text(0.05, 0.36, f"${latest_capex:,.1f}B", color='#ffffff', fontsize=32, fontweight='bold')
        
        ax.text(0.55, 0.50, "AVG ADJUSTED ROIC PROFILE", color='#ffffff', fontsize=9, alpha=0.7, fontweight='bold')
        ax.text(0.55, 0.36, f"{latest_roic:.1f}%", color='#ffffff', fontsize=32, fontweight='bold')
        
        ax.text(0.05, 0.12, "Generated securely via the data warehouse lakehouse pipeline framework.", color='#ffffff', fontsize=8, alpha=0.5, fontstyle='italic')
        
        # Save out the plot canvas memory map cleanly to an internal binary byte buffer stream
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
        buf.seek(0)
        plt.close(fig) # Shut down background figure handlers to prevent cloud memory leaks
        
        # Stream the image file downstream to a user actionable click trigger
        st.download_button(
            label="📥 Download Executive Presentation Summary Card (.PNG)",
            data=buf,
            file_name=f"roic_summary_{latest_scenario.lower().replace(' ', '_')}.png",
            mime="image/png"
        )
