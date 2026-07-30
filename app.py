import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Page Configuration & Visual Styling
st.set_page_config(page_title="ROIC Intelligence App", layout="wide")

# Minimalist corporate styling matched to your screenshot palette
st.markdown("""
    <style>
    .metric-box {
        background-color: #0d231d;
        color: #ffffff;
        padding: 24px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .metric-value { font-size: 36px; font-weight: bold; }
    .metric-label { font-size: 14px; opacity: 0.8; }
    </style>
""", unsafe_allow_html=True)

st.title("The returns behind the AI buildout")
st.caption("Illustrative Financial Modeling Application • Powered by Open-Source Python & Streamlit")
st.divider()

# 2. Sidebar Parameters (What-If Scenario Controls)
st.sidebar.header("🔧 What-If Sensitivity Adjustments")

base_capex = 357.5
base_roic = 29.7

# Sliders to simulate scenario testing
capex_multiplier = st.sidebar.slider(
    "Simulated Capex Scaling Factor", 
    min_value=0.5, max_value=2.0, value=1.0, step=0.1,
    help="Adjusts the $357.5B base Hyperscaler cash capex."
)

roic_shift = st.sidebar.slider(
    "Adjusted ROIC Shift (Percentage Points)", 
    min_value=-15.0, max_value=15.0, value=0.0, step=0.5,
    help="Simulates improvements or compressions in returns on invested capital."
)

# 3. Core Semantic Calculation Engine
simulated_capex = base_capex * capex_multiplier
simulated_roic = base_roic + roic_shift

# 4. KPI Layout Presentation
col1, col2 = st.columns(2)  # FIXED: Added the required argument '2'

with col1:
    st.subheader("Hyperscaler Financial Framework")
    st.write(
        f"The hyperscalers invested **${simulated_capex:,.1f}B** in cash capex "
        f"while sustaining an average **{simulated_roic:.1f}%** adjusted ROIC."
    )
    
    # Live Interactive Visualizer Chart
    fig = go.Figure()
    
    # Baseline Marker
    fig.add_trace(go.Scatter(
        x=[base_capex], y=[base_roic],
        mode='markers+text', name='Morgan Stanley Baseline',
        text=["Baseline"], textposition="top center",
        marker=dict(color='#A0A0A0', size=15)
    ))
    
    # Simulated Target Marker
    fig.add_trace(go.Scatter(
        x=[simulated_capex], y=[simulated_roic],
        mode='markers+text', name='Simulated Scenario',
        text=["Current Scenario"], textposition="bottom center",
        marker=dict(color='#0d231d', size=18, symbol='star')
    ))
    
    fig.update_layout(
        title="Capex vs. Adjusted ROIC Efficiency Frontier",
        xaxis_title="Cash Capex ($ Billions)",
        yaxis_title="Adjusted ROIC (%)",
        xaxis=dict(range=[100, 800]), 
        yaxis=dict(range=[0, 50]),
        template="plotly_white", 
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Render UI boxes based on dark theme in screenshot
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">CASH CAPEX</div>
            <div class="metric-value">${simulated_capex:,.1f}B</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">ADJUSTED ROIC</div>
            <div class="metric-value">{simulated_roic:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick-view tabular lookup historical log
    st.subheader("📜 Scenario Version Ledger")
    history_df = pd.DataFrame({
        "Scenario Baseline": ["Report Baseline", "Current Simulation"],
        "Capex ($B)": [base_capex, round(simulated_capex, 1)],
        "ROIC (%)": [base_roic, round(simulated_roic, 1)]
    })
    st.dataframe(history_df, hide_index=True, use_container_width=True)
