import streamlit as st
import pandas as pd

st.title("🏢 Company Lens Decomposition")
st.caption("Granular operational breakdowns extracted from primary 10-K registries and alternative data sources.")
st.divider()

# 1. Base Corporate Relational Dataset (Silver Layer Table)
base_company_df = pd.DataFrame({
    "Hyperscaler Entity": ["Microsoft (Azure)", "Alphabet (GCP)", "Amazon (AWS)", "Meta Infrastructure"],
    "Allocated AI Capex ($B)": [120.5, 95.0, 82.0, 60.0],
    "Isolated Operating Return (%)": [32.4, 28.1, 31.0, 24.5],
    "Data Confidence Status": ["Verified (10-K)", "Verified (10-K)", "Calculated Estimate", "Alternative Data Source"]
})

# 2. Interactive Multi-Select Filter Menu
st.subheader("🔍 Corporate Filter Optimization Hub")
all_companies = base_company_df["Hyperscaler Entity"].unique().tolist()

selected_companies = st.multiselect(
    "Isolate specific hyperscale tracking entities:",
    options=all_companies,
    default=all_companies,
    help="Select or remove corporate tracking rows to refine the analytical matrix below."
)

# 3. Dynamic Filter Logic
if not selected_companies:
    st.warning("⚠️ Please select at least one corporate entity to render data tracking lines.")
else:
    filtered_df = base_company_df[base_company_df["Hyperscaler Entity"].isin(selected_companies)]
    
    # 4. Top Row Segmented Telemetry Calculations
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(
            label="AGGREGATE SELECTED CAPEX", 
            value=f"${filtered_df['Allocated AI Capex ($B)'].sum():,.1f}B"
        )
    with c2:
        st.metric(
            label="MAX ISOLATED OPERATING RETURN", 
            value=f"{filtered_df['Isolated Operating Return (%)'].max():.1f}%"
        )
    with c3:
        st.metric(
            label="ACTIVE DATA LINE TRACKERS", 
            value=f"{len(filtered_df)} / {len(all_companies)}"
        )
        
    st.write("")
    
    # 5. Filtered Data Display
    st.subheader("📋 Segmented Corporate Dimensions Grid")
    st.dataframe(
        filtered_df, 
        hide_index=True, 
        use_container_width=True
    )
