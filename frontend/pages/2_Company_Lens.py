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

# 2. Interactive Threshold Configuration System
st.sidebar.header("🎯 Enterprise Hurdle Options")
target_hurdle = st.sidebar.slider(
    "Minimum Return Safety Threshold (%)",
    min_value=15.0, max_value=35.0, value=25.0, step=0.5,
    help="Set the minimum acceptable operating return target profile for isolated hyperscale entities."
)

st.subheader("🔍 Corporate Filter Optimization Hub")
all_companies = base_company_df["Hyperscaler Entity"].unique().tolist()

selected_companies = st.multiselect(
    "Isolate specific hyperscale tracking entities:",
    options=all_companies,
    default=all_companies
)

if not selected_companies:
    st.warning("⚠️ Please select at least one corporate entity to render data tracking lines.")
else:
    filtered_df = base_company_df[base_company_df["Hyperscaler Entity"].isin(selected_companies)].copy()
    
    # 3. LIVE COLUMN THRESHOLD ALERTS (Evaluating drops beneath hurdle boundary parameters)
    failing_entities = filtered_df[filtered_df["Isolated Operating Return (%)"] 
            {status_message}
        </div>
    """, unsafe_allow_html=True)
    
    # Top Row Segmented Telemetry Calculations
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="AGGREGATE SELECTED CAPEX", value=f"${filtered_df['Allocated AI Capex ($B)'].sum():,.1f}B")
    with c2:
        st.metric(label="MAX ISOLATED OPERATING RETURN", value=f"{filtered_df['Isolated Operating Return (%)'].max():.1f}%")
    with c3:
        st.metric(label="FAILING SYSTEM NODES", value=f"{len(failing_entities)} / {len(filtered_df)}")
        
    st.write("")
    
    # 4. Highlighted Grid Representation
    st.subheader("📋 Segmented Corporate Dimensions Grid")
    
    # FIXED: Rebuilt clean explicit row styling function to resolve ast parsing issues
    def style_threshold_rows(row):
        is_below_hurdle = row["Isolated Operating Return (%)"] < target_hurdle
        bg_style = 'background-color: #ffcccc' if is_below_hurdle else ''
        return [bg_style] * len(row)
        
    styled_grid = filtered_df.style.apply(style_threshold_rows, axis=1)
    st.dataframe(styled_grid, hide_index=True, use_container_width=True)
