import streamlit as st
import pandas as pd
import numpy as np

st.title("🏢 Company Lens Decomposition")
st.caption("Granular operational breakdowns extracted from primary 10-K registries with multi-year hurdle forecasting.")
st.divider()

# 1. Base Corporate Relational Dataset (Silver Layer Table)
base_company_df = pd.DataFrame({
    "Hyperscaler Entity": ["Microsoft (Azure)", "Alphabet (GCP)", "Amazon (AWS)", "Meta Infrastructure"],
    "Allocated AI Capex ($B)": [120.5, 95.0, 82.0, 60.0],
    "Isolated Operating Return (%)": [32.4, 28.1, 31.0, 24.5],
    "Historical Return Growth (pp/yr)": [1.5, 0.8, 1.2, 2.1], # Percentage points improvement per year
    "Data Confidence Status": ["Verified (10-K)", "Verified (10-K)", "Calculated Estimate", "Alternative Data Source"]
})

# 2. Interactive Threshold Configuration System
st.sidebar.header("🎯 Enterprise Hurdle Options")
target_hurdle = st.sidebar.slider(
    "Minimum Return Safety Threshold (%)",
    min_value=15.0, max_value=35.0, value=25.0, step=0.5,
    help="Set the minimum acceptable operating return target profile."
)

st.subheader("🔍 Corporate Filter Optimization Hub")
all_companies = base_company_df["Hyperscaler Entity"].unique().tolist()
selected_companies = st.multiselect("Isolate specific hyperscale tracking entities:", options=all_companies, default=all_companies)

# FEATURE 1: Dynamic line-item filtering toggle switch
isolate_failing = st.toggle(
    "⚠️ Isolate Deficit Entities Only", 
    value=False,
    help="Toggle this switch to instantly clear passing rows and show only the corporations currently failing the active hurdle rate."
)

if not selected_companies:
    st.warning("⚠️ Please select at least one corporate entity.")
else:
    # First filter down to selected entities
    filtered_df = base_company_df[base_company_df["Hyperscaler Entity"].isin(selected_companies)].copy()
    
    # Isolate failing entities for alert metrics
    failing_entities_master = filtered_df[filtered_df["Isolated Operating Return (%)"] < target_hurdle]
    
    # Apply the toggle filter if switched on
    if isolate_failing:
        filtered_df = filtered_df[filtered_df["Isolated Operating Return (%)"] < target_hurdle]

    # Dynamic Layout CSS Generator based on threshold safety status
    if not failing_entities_master.empty:
        alert_bg, alert_border, alert_text = "#fde8e8", "#f8b4b4", "#9b1c1c"
        status_message = f"🚨 ALERT: {len(failing_entities_master)} profiles dropped beneath your active {target_hurdle}% threshold!"
    else:
        alert_bg, alert_border, alert_text = "#edfafa", "#b2f5ea", "#005c53"
        status_message = "✅ STABLE: All isolated enterprise data entities clear active return performance hurdles."

    st.markdown(f'<div style="background-color: {alert_bg}; border: 1px solid {alert_border}; color: {alert_text}; padding: 16px; border-radius: 4px; font-weight: bold; margin-bottom: 20px;">{status_message}</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.metric(label="AGGREGATE SELECTED CAPEX", value=f"${filtered_df['Allocated AI Capex ($B)'].sum():,.1f}B")
    with c2: st.metric(label="MAX ISOLATED OPERATING RETURN", value=f"{filtered_df['Isolated Operating Return (%)'].max():.1f}%" if not filtered_df.empty else "0.0%")
    with c3: st.metric(label="FAILING SYSTEM NODES", value=f"{len(failing_entities_master)} / {len(all_companies)}")
        
    st.write("")
    
    if filtered_df.empty:
        st.info("ℹ️ No entities match the active deficit filter criteria.")
    else:
        st.subheader("📋 Segmented Corporate Dimensions Grid")
        
        # Explicit row highlight function
        def style_threshold_rows(row):
            is_below_hurdle = row["Isolated Operating Return (%)"]  0 else "Immediate"
                })
            
            projection_df = pd.DataFrame(projection_records)
            st.dataframe(projection_df, hide_index=True, use_container_width=True)
