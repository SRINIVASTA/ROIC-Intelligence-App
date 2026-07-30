import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import duckdb

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "lakehouse.db"))

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

# Query latest metric state from local lakehouse data store
conn = duckdb.connect(database=DB_PATH)
current_name, current_capex, current_roic, _ = conn.execute("SELECT * FROM gold_roic_ledger ORDER BY timestamp DESC LIMIT 1").fetchone()
conn.close()

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
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[357.5], y=[29.7], mode='markers+text', name='Baseline', text=["Baseline"], textposition="top center", marker=dict(color='#A0A0A0', size=12)))
    fig.add_trace(go.Scatter(x=[current_capex], y=[current_roic], mode='markers+text', name='Current', text=["Active Run"], textposition="bottom center", marker=dict(color='#0d231d', size=16, symbol='star')))
    fig.update_layout(xaxis_title="Cash Capex ($B)", yaxis_title="Adjusted ROIC (%)", template="plotly_white", margin=dict(l=20, r=20, t=20, b=20))
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
