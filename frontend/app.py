import os
import streamlit as st
import duckdb

# --- FORCE STREAMLIT TO HIDE CHROME, HEADERS, AND FOOTERS ---
st.markdown("""
    <style>
    /* 1. Hide the entire top header toolbar (Deploy, Share, Options menu) */
    [data-testid="stHeader"], header {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 2. Hide the running status loading elements */
    [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 3. Hide GitHub connection buttons or fork badges */
    .viewerBadge_container__17w1a, #GithubIcon, .styles_viewerBadge__1yB5_ {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 4. Hide the native main menu hamburger icon */
    #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }

    /* 5. Hide the default Streamlit footer */
    footer {
        visibility: hidden !important;
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="ROIC Intelligence Platform", layout="wide")

# Determine base execution directory setups cleanly
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "lakehouse.db")

def verify_and_get_connection():
    if 'duckdb_conn' not in st.session_state:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        st.session_state.duckdb_conn = duckdb.connect(database=DB_PATH)
        
        # SYSTEM FIX: Drop the old limited table design to force a clean multi-column rebuild
        st.session_state.duckdb_conn.execute("DROP TABLE IF EXISTS gold_roic_ledger")
        
        # Re-initialize Core Gold ledger tracking schemas with company tracking column extensions built in
        st.session_state.duckdb_conn.execute("""
            CREATE TABLE IF NOT EXISTS gold_roic_ledger (
                scenario_name VARCHAR,
                capex_billion DOUBLE,
                roic_percent DOUBLE,
                msft_roic DOUBLE,
                gcp_roic DOUBLE,
                aws_roic DOUBLE,
                meta_roic DOUBLE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Seed baseline entry direct with separate corporate values matching historical vectors
        st.session_state.duckdb_conn.execute("""
            INSERT INTO gold_roic_ledger (scenario_name, capex_billion, roic_percent, msft_roic, gcp_roic, aws_roic, meta_roic) 
            VALUES ('Morgan Stanley Baseline', 357.5, 29.7, 32.4, 28.1, 31.0, 24.5)
        """)
    return st.session_state.duckdb_conn

# Initialize connection immediately on primary boot
conn = verify_and_get_connection()

# Clear multi-page page routing structure mappings
pages = {
    "ROIC Intelligence": [
        st.Page("pages/executive_story.py", title="📖 Executive Story", default=True),
        st.Page("pages/company_lens.py", title="🏢 Company Lens"),
        st.Page("pages/what_if_lab.py", title="🧪 What-If Lab"),
    ]
}

pg = st.navigation(pages)
pg.run()

# High-visibility fixed footer with professional contact links
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #262730; /* Matches your secondary background */
        color: #FAFAFA;            /* Matches your theme text color */
        text-align: center;
        font-size: 13px;
        padding: 12px 0;
        z-index: 999999;           /* Forces footer to stay on top of everything */
        border-top: 1px solid #FF4B4B; /* Adds a thin red line accent */
    }
    .footer a {
        color: #FF4B4B;            /* Uses your primary theme red color for links */
        text-decoration: none;
        margin: 0 10px;
        font-weight: bold;
    }
    .footer a:hover {
        text-decoration: underline;
        color: #FAFAFA;            /* Turns white when hovered */
    }
    .footer-separator {
        color: #666;
        margin: 0 5px;
    }
    /* Adds padding to the bottom of the page container so content isn't blocked */
    .main .block-container {
        padding-bottom: 70px;
    }
    </style>
    <div class="footer">
        <span><strong>© 2026 T A Srinivas.</strong> All Rights Reserved. Strictly for portfolio viewing purposes.</span>
        <span class="footer-separator">|</span>
        <a href="https://www.linkedin.com/in/srinivas-t-a-557637119/" target="_blank">LinkedIn Profile</a>
        <span class="footer-separator">|</span>
        <a href="mailto:tasrinivass@gmail.com">Contact Me</a>
    </div>
    """,
    unsafe_allow_html=True
)
