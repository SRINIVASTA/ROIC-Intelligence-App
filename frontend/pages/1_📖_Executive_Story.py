import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.markdown("""
    <style>
    .metric-card-dark { background-color: #0d231d; color: #ffffff; padding: 24px; border-radius: 4px; margin-bottom: 20px; }
    .metric-card-light { background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 20px; border-radius: 4px; }
    .metric-value-large { font-size: 42px; font-weight: bold; line-height: 1.1; }
    .metric-value-sub { font-size: 28px; font-weight: bold; color: #111111; }
    .metric-label-dark { font-size: 11px; opacity: 0.7; letter-spacing: 1px; margin-bottom: 8px; text-transform: uppercase;}
    .metric-label-light { font-size: 11px; color: #6c757d; font-weight: bold; text-transform: uppercase; margin-bottom: 4px; }
    </style>
""", unsafe_allow_html=True)

st.title("The returns behind the AI buildout")
st.caption("A governed view of capital intensity, operating performance, and pathways to economic profit.")
st.divider()

# 1. Fetch complete data table timeline from DuckDB
conn = st.session_state.duckdb_conn
all_scenarios_df = conn.execute("SELECT * FROM gold_roic_ledger ORDER BY timestamp ASC").df()

# Isolate latest row for the main KPI layouts
latest_row = all_scenarios_df.iloc[-1]
current_name = latest_row["scenario_name"]
current_capex = latest_row["capex_billion"]
current_roic = latest_row["roic_percent"]

simulated_revenue = 1602.5 * (current_capex / 357.5)
simulated_spread = current_roic - 9.0

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"""
        <div style="background-color: #fdfdfd; padding: 30px; border: 1px solid #f1f1f1; border-radius: 4px; margin-bottom: 20px;">
            <p style="font-size: 11px; color: #a0a0a0; font-weight: bold; margin-bottom: 5px;">@ ACTIVE VIEW: {current_name.upper()}</p>
            <h2 style="font-family: serif; font-size: 34px; font-weight: normal; color: #111111; line-height: 1.3;">
                The hyperscalers invested <span style="color: #2e7d32; font-weight: bold;">${current_capex:,.1f}B</span> in cash capex while sustaining an average <span style="color: #2e7d32; font-weight: bold;">{current_roic:.1f}%</span> adjusted ROIC.
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. PERSISTENT TIME-SERIES LINE PLOT (Charting consecutive simulation runs)
    fig = go.Figure()
    
    # Add historical sequence tracking trajectory path
    fig.add_trace(go.Scatter(
        x=all_scenarios_df["timestamp"], 
        y=all_scenarios_df["roic_percent"],
        mode='lines+markers',
        name='Simulation Trajectory',
        line=dict(color='#2e7d32', width=3),
        marker=dict(size=8, color='#0d231d'),
        hovertext=all_scenarios_df["scenario_name"]
    ))
    
    # Static Hurdle reference marking threshold boundary line
    fig.add_shape(
        type="line", x0=all_scenarios_df["timestamp"].min(), x1=all_scenarios_df["timestamp"].max(),
        y0=9.0, y1=9.0, line=dict(color="#d32f2f", width=2, dash="dash")
    )
    
    fig.update_layout(
        title="Scenario Iteration Path Over Time vs 9% Hurdle Rate",
        xaxis_title="Commit Timestamp Timeline",
        yaxis_title="Adjusted ROIC (%)",
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown(f"""
        <div class="metric-card-dark">
            <div class="metric-label-dark">FY2025 Combined Revenue</div>
            <div class="metric-value-large">${simulated_revenue:,.1f}B</div>
        </div>
        <div class="metric-card-dark">
            <div class="metric-label-dark">WACC Spread (9% Hurdle)</div>
            <div class="metric-value-large">{simulated_spread:+.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

b1, b2, b3, b4 = st.columns(4)
with b1: st.markdown(f'<div class="metric-card-light"><div class="metric-label-light">Cash Capex</div><div class="metric-value-sub">${current_capex:,.1f}B</div></div>', unsafe_allow_html=True)
with b2: st.markdown(f'<div class="metric-card-light"><div class="metric-label-light">Avg Adjusted ROIC</div><div class="metric-value-sub">{current_roic:.1f}%</div></div>', unsafe_allow_html=True)
with b3:
    color = "#2e7d32" if current_roic >= 9.0 else "#d32f2f"
    st.markdown(f'<div class="metric-card-light"><div class="metric-label-light">Positive Spreads</div><div class="metric-value-sub" style="color:{color};">4 / 4</div></div>', unsafe_allow_html=True)
with b4: st.markdown('<div class="metric-card-light"><div class="metric-label-light">Evidence Classes</div><div class="metric-value-sub">5</div></div>', unsafe_allow_html=True)
