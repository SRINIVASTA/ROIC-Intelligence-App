import streamlit as st
import pandas as pd

st.title("🏢 Company Lens Decomposition")
st.caption("Granular breakdowns extracted from source registries.")
st.divider()

company_data = pd.DataFrame({
    "Hyperscaler Entity": ["Company Alpha", "Company Beta", "Company Gamma", "Company Delta"],
    "Allocated AI Capex ($B)": [120.5, 95.0, 82.0, 60.0],
    "Isolated Operating Return (%)": [32.4, 28.1, 31.0, 24.5],
    "Data Confidence Status": ["Verified (10-K)", "Verified (10-K)", "Calculated Estimate", "Alternative Data Source"]
})

st.dataframe(company_data, hide_index=True, use_container_width=True)
