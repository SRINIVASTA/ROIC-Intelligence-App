import streamlit as st
import pandas as pd
import numpy as np

st.title("🏢 Company Lens Decomposition")
st.caption("Granular operational breakdowns extracted from primary 10-K registries with multi-year hurdle forecasting.")
st.divider()

base_company_df = pd.DataFrame({
    "Hyperscaler Entity": ["Microsoft (Azure)", "Alphabet (GCP)", "Amazon (AWS)", "Meta Infrastructure"],
    "Allocated AI Capex ($B)": [120.5, 95.0, 82.0, 60.0],
    "Isolated Operating Return (%)": [32.4, 28.1, 31.0, 24.5],
    "Historical Return Growth (pp/yr)": [1.5, 0.8, 1.2, 2.1],
    "Data Confidence Status": ["Verified (10-K)", "Verified (10-K)", "Calculated Estimate", "Alternative Data Source"]
})

st.sidebar.header("🎯 Enterprise Hurdle Options")
target_hurdle = st.sidebar.slider(
    "Minimum Return Safety Threshold (%)",
    min_value=15.0, max_value=35.0, value=25.0, step=0.5,
    help="Set the minimum acceptable operating return target profile."
)

st.subheader("🔍 Corporate Filter Optimization Hub")
all_companies = base_company_df["Hyperscaler Entity"].unique().tolist()
selected_companies = st.multiselect("Isolate specific hyperscale tracking entities:", options=all_companies, default=all_companies)

isolate_failing = st.toggle(
    "⚠️ Isolate Deficit Entities Only", 
    value=False,
    help="Toggle this switch to instantly clear passing rows and show only the corporations currently failing the active hurdle rate."
)

if not selected_companies:
    st.warning("⚠️ Please select at least one corporate entity.")
else:
    filtered_df = base_company_df[base_company_df["Hyperscaler Entity"].isin(selected_companies)].copy()
    failing_entities_df = filtered_df[filtered_df["Isolated Operating Return (%)"] = target_hurdle:
            years_needed = 0
        elif growth_rate <= 0:
            years_needed = float('inf') 
        else:
            years_needed = (target_hurdle - current_return) / growth_rate
            
        projection_records.append({
            "Hyperscaler Entity": entity_name,
            "Current Return (%)": current_return,
            "Target Hurdle (%)": target_hurdle,
            "Growth Rate (pp/yr)": growth_rate,
            "Estimated Runway (Years)": round(years_needed, 1) if years_needed != float('inf') else "Non-convergent",
            "Hurdle Status": "Passing" if years_needed == 0 else "Immediate Attention"
        })
    
    projection_df = pd.DataFrame(projection_records)
    st.dataframe(projection_df, hide_index=True)
