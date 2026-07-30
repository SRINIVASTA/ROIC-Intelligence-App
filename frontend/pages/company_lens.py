import os
import sys
# Force Python path context alignment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import pandas as pd
import numpy as np
# Import the matrix generation function directly from gold pipeline
from data_pipeline.transform_gold import get_company_registry_matrix

st.cache_data.clear()

st.title("🏢 Comprehensive Corporate Lens Analyzer")
st.caption("Granular segment breakdowns mapping the full credit stack from primary registries.")
st.divider()

if "duckdb_conn" not in st.session_state:
    st.error("🔌 Database engine connection offline. Initialize application from core landing page.")
else:
    conn = st.session_state.duckdb_conn
    
    try:
        latest_sim_df = conn.execute("SELECT * FROM gold_roic_ledger ORDER BY timestamp DESC LIMIT 1").df()
        active_capex = float(latest_sim_df.at[0, "capex_billion"])
        active_roic = float(latest_sim_df.at[0, "roic_percent"])
        active_scenario = str(latest_sim_df.at[0, "scenario_name"])
        
        r_msft = float(latest_sim_df.at[0, "msft_roic"]) if "msft_roic" in latest_sim_df.columns else round(active_roic + 2.7, 1)
        r_gcp = float(latest_sim_df.at[0, "gcp_roic"]) if "gcp_roic" in latest_sim_df.columns else round(active_roic - 1.6, 1)
        r_aws = float(latest_sim_df.at[0, "aws_roic"]) if "aws_roic" in latest_sim_df.columns else round(active_roic + 1.3, 1)
        r_meta = float(latest_sim_df.at[0, "meta_roic"]) if "meta_roic" in latest_sim_df.columns else round(active_roic - 5.2, 1)
    except Exception:
        active_capex, active_roic, active_scenario = 357.5, 29.7, "Default Baseline"
        r_msft, r_gcp, r_aws, r_meta = 32.4, 28.1, 31.0, 24.5

    st.info(f"Active Pipeline Context: **{active_scenario}** (Capex: ${active_capex}B, Baseline ROIC: {active_roic}%)")

    # FIX: Generating dataframe via one single line method invocation call!
    master_registry_df = get_company_registry_matrix(active_capex, r_msft, r_gcp, r_aws, r_meta, active_roic)

    st.sidebar.header("🎯 Target Hurdle Parameters")
    target_hurdle = st.sidebar.slider("Minimum Acceptable Safety Return Threshold (%)", min_value=10.0, max_value=40.0, value=25.0, step=0.5)

    st.subheader("🔍 Isolate Ecosystem Players")
    all_entities = master_registry_df["Company / Cluster Entity"].tolist()
    default_selections = ["Microsoft (Azure)", "Alphabet (GCP)", "Amazon (AWS)", "Meta Infrastructure"]
    
    selected_entities = st.multiselect(
        "Select specific enterprise tracking components to populate the financial matrix:",
        options=all_entities,
        default=default_selections
    )

    isolate_failing = st.toggle("⚠️ Isolate Deficit Entities Only", value=False)

    if not selected_entities:
        st.warning("Please choose at least one enterprise entity to calculate data summaries.")
    else:
        filtered_df = master_registry_df[master_registry_df["Company / Cluster Entity"].isin(selected_entities)].copy()
        failing_entities_df = filtered_df[filtered_df["Isolated Operating Return (%)"] < target_hurdle]
        
        display_df = failing_entities_df.copy() if isolate_failing else filtered_df.copy()
            
        if not display_df.empty:
            display_df = display_df.sort_values(by="Allocated Capex Intensity ($B)", ascending=False)
            st.dataframe(display_df, hide_index=True, width="stretch")
        else:
            st.info("🎉 Operational Integrity Verified: No active deficit entities match this hurdle profile!")
        
        st.subheader("📈 Runway Forecast and Convergence Metrics")
        projection_records = []
        for idx, row in filtered_df.iterrows():
            current_return = row["Isolated Operating Return (%)"]
            growth_rate = row["Historical Return Growth (pp/yr)"]
            years_needed = 0 if current_return >= target_hurdle else (float('inf') if growth_rate <= 0 else (target_hurdle - current_return) / growth_rate)
                
            projection_records.append({
                "Ecosystem Entity": row["Company / Cluster Entity"],
                "Classification": row["Segment Classification"],
                "Allocated Capex ($B)": row["Allocated Capex Intensity ($B)"],
                "Current Return (%)": current_return,
                "Target Hurdle (%)": target_hurdle,
                "Estimated Runway (Years)": round(years_needed, 1) if years_needed != float('inf') else "Non-convergent",
                "Hurdle Status": "Passing" if years_needed == 0 else "Immediate Attention"
            })
        
        projection_df = pd.DataFrame(projection_records)
        if isolate_failing:
            projection_df = projection_df[projection_df["Hurdle Status"] == "Immediate Attention"]
            
        if not projection_df.empty:
            projection_df = projection_df.sort_values(by="Allocated Capex ($B)", ascending=False)
            st.dataframe(projection_df, hide_index=True, width="stretch")
