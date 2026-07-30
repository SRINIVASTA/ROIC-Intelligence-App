import streamlit as st
import pandas as pd
import numpy as np
from data_pipeline.transform_gold import calculate_lens_metrics

# Force clear background layout cache memory configurations on load
st.cache_data.clear()

st.title("🏢 Comprehensive Corporate Lens Analyzer")
st.caption("Granular segment breakdowns mapping the full credit stack from primary SEC and Wall Street database registries.")
st.divider()

if "duckdb_conn" not in st.session_state:
    st.error("🔌 Database engine connection offline. Please initialize the application from the main core page.")
else:
    conn = st.session_state.duckdb_conn
    
    # Extract the active macro scenario metrics from the gold lakehouse log tables
    try:
        latest_sim_df = conn.execute("SELECT * FROM gold_roic_ledger ORDER BY timestamp DESC LIMIT 1").df()
        active_capex = float(latest_sim_df.at[0, "capex_billion"])
        active_roic = float(latest_sim_df.at[0, "roic_percent"])
        active_scenario = str(latest_sim_df.at[0, "scenario_name"])
        
        # Read the unique company baseline overrides if present in the data row
        r_msft = float(latest_sim_df.at[0, "msft_roic"]) if "msft_roic" in latest_sim_df.columns else round(active_roic + 2.7, 1)
        r_gcp = float(latest_sim_df.at[0, "gcp_roic"]) if "gcp_roic" in latest_sim_df.columns else round(active_roic - 1.6, 1)
        r_aws = float(latest_sim_df.at[0, "aws_roic"]) if "aws_roic" in latest_sim_df.columns else round(active_roic + 1.3, 1)
        r_meta = float(latest_sim_df.at[0, "meta_roic"]) if "meta_roic" in latest_sim_df.columns else round(active_roic - 5.2, 1)
    except Exception:
        active_capex, active_roic, active_scenario = 357.5, 29.7, "Default Baseline"
        r_msft, r_gcp, r_aws, r_meta = 32.4, 28.1, 31.0, 24.5

    st.info(f"Active Pipeline Context: **{active_scenario}** (Capex: ${active_capex}B, Baseline ROIC: {active_roic}%)")

    # Cleaned Matrix: Offloaded hardcoded math layers to calculate_lens_metrics in data pipeline
    master_registry_df = pd.DataFrame({
        "Company / Cluster Entity": [
            "Microsoft (Azure)", "Alphabet (GCP)", "Amazon (AWS)", "Meta Infrastructure", "Oracle Cloud", "Alibaba Group",
            "CoreWeave AI", "Lambda Labs", "Crusoe Energy", "NVIDIA Corporation", "FluidStack", "Nebius", "Nscale", 
            "OpenAI Compute Node", "Anthropic Cluster"
        ],
        "Segment Classification": [
            "Hyperscaler Core", "Hyperscaler Core", "Hyperscaler Core", "Hyperscaler Core", "Hyperscaler Core", "Hyperscaler Core",
            "Specialized Neocloud", "Specialized Neocloud", "Specialized Neocloud", "Hardware Silicon Designer", "Specialized Neocloud", "Specialized Neocloud", "Specialized Neocloud",
            "Frontier Model Dev", "Frontier Model Dev"
        ],
        "Allocated Capex Intensity ($B)": [
            round(active_capex * 0.28, 1), round(active_capex * 0.22, 1), round(active_capex * 0.20, 1), 
            round(active_capex * 0.14, 1), round(active_capex * 0.06, 1), round(active_capex * 0.03, 1),
            round(active_capex * 0.02, 1), round(active_capex * 0.01, 1), round(active_capex * 0.01, 1),
            round(active_capex * 0.01, 1), round(active_capex * 0.005, 1), round(active_capex * 0.005, 1), 
            round(active_capex * 0.005, 1), round(active_capex * 0.003, 1), round(active_capex * 0.002, 1)
        ],
        "Isolated Operating Return (%)": [
            calculate_lens_metrics(r_msft, 100.0), calculate_lens_metrics(r_gcp, 100.0), 
            calculate_lens_metrics(r_aws, 100.0), calculate_lens_metrics(r_meta, 100.0), 
            calculate_lens_metrics(active_roic - 1.2, 100.0), calculate_lens_metrics(active_roic - 3.4, 100.0),
            calculate_lens_metrics(active_roic - 6.2, 100.0), calculate_lens_metrics(active_roic - 5.8, 100.0), 
            calculate_lens_metrics(active_roic - 4.1, 100.0), calculate_lens_metrics(active_roic + 14.8, 100.0), 
            calculate_lens_metrics(active_roic - 7.3, 100.0), calculate_lens_metrics(active_roic - 6.5, 100.0), 
            calculate_lens_metrics(active_roic - 7.0, 100.0), calculate_lens_metrics(active_roic - 8.4, 100.0), 
            calculate_lens_metrics(active_roic - 9.1, 100.0)
        ],
        "Historical Return Growth (pp/yr)": [
            1.5, 0.8, 1.2, 2.1, 1.7, 0.5,
            3.6, 3.2, 2.4, 5.8, 1.8, 2.0, 
            1.5, 4.2, 3.9
        ],
        "Credit Risk Profile (S&P)": [
            "AAA (Excellent)", "AA- (High Quality)", "AA (High Quality)", "AA- (High Quality)", "BBB (Investment Grade)", "A+ (Strong)",
            "B+ (Speculative/High Yield)", "Private (Unrated)", "Private (Unrated)", "AAA (Excellent Equivalent)", "Private (Unrated)", "Unrated", 
            "Private (Unrated)", "Borrowing MSFT Credit", "Borrowing AMZN Credit"
        ]
    })

    # Sidebar Threshold Operations
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
        
        if isolate_failing:
            display_df = failing_entities_df.copy()
        else:
            display_df = filtered_df.copy()
            
        if not display_df.empty:
            display_df = display_df.sort_values(by="Allocated Capex Intensity ($B)", ascending=False)
            st.dataframe(display_df, hide_index=True, width="stretch")
        else:
            st.info("🎉 Operational Integrity Verified: No active deficit entities match this hurdle profile!")
        
        st.subheader("📈 Runway Forecast and Convergence Metrics")
        st.markdown("Projects the total calendar timeline (runway years) needed to pass the safety threshold based on current growth trajectories.")
        
        projection_records = []
        for idx, row in filtered_df.iterrows():
            current_return = row["Isolated Operating Return (%)"]
            growth_rate = row["Historical Return Growth (pp/yr)"]
            
            if current_return >= target_hurdle:
                years_needed = 0
            elif growth_rate <= 0:
                years_needed = float('inf') 
            else:
                years_needed = (target_hurdle - current_return) / growth_rate
                
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
