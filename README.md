# 🏢 AI Infrastructure ROIC Intelligence Platform

Developed by **Srinivasta** • Built on a programmatic cloud-native Medallion Lakehouse Engine.

An institutional-grade financial analytics suite and "What-If" simulator engineered to evaluate hyper-scale capital deployment, aggregate AI capacity metrics, infrastructure leasing frameworks, and portfolio return profiles.

---
## 🚀 Live Streamlit Application Context [ROIC-Intelligence-App](https://roic-intelligence-app-mprxzj5ss9pcpykoag2jwg.streamlit.app/)

The application interface is fully automated, self-healing, and deployed live to production on Streamlit Cloud. 

### 🕹️ Core Multi-Page Subsystem Matrix:
1. **📖 Executive Story (The Presentation Hub)**: Pulls transactional simulation rows straight from the active Gold warehouse ledger to update aggregate WACC economic profit spreads, project overall industry cash capex vs. a 9.0% hurdle, and emit high-resolution slide deck snapshot presentation cards (.PNG).
2. **🏢 Company Lens (Granular Ecosystem Decomposition)**: Pre-arranges all 15 core ecosystem players (from primary Hyperscalers down to Neoclouds and frontier model nodes) ranked from **Big to Small** by asset spend size. Features dynamic threshold sliders and risk isolation filters (`⚠️ Isolate Deficit Entities Only`).
3. **🧪 What-If Lab (The Data Extraction & Risk Engine)**: Houses both the automated unstructured document parser (`pdfplumber`) and an advanced **1,000-iteration Monte Carlo Volatility Simulator** utilizing statistical normal distribution bell curves to compute portfolio Value-at-Risk (VaR) profiles on the fly.

---

## 🛠️ Unified Medallion Architecture Setup

The platform utilizes a structured backend data catalog structure ensuring a Single Source of Truth across text-parsing and financial visualization components:

```text
roic-intelligence-app/
│
├── .streamlit/
│   └── config.toml            # Deployed runtime configuration flags
│
├── data_pipeline/             # Backend Medallion Processing Core
│   ├── __init__.py
│   ├── ingestion_bronze.py    # Raw text extraction, hashing, and regex mapping
│   ├── transform_gold.py      # Aggregations and analytical metric calculation layers
│   └── orchestrator.py        # Pipeline execution workflow manager
│
├── database/                  # Invisible Storage Layer (Handled in Cloud Virtual Memory)
│   └── lakehouse.db           # Persistent DuckDB transaction database file
│
├── frontend/                  # Presentation Layer (Streamlit App Layout)
│   ├── app.py                 # Core routing system & bootstrapper file
│   └── pages/                 
│       ├── executive_story.py # Storytelling presentation card metric dashboards
│       ├── company_lens.py    # Size-sorted multi-entity filtration hub
│       └── what_if_lab.py     # Document uploader and Monte Carlo simulation lab
│
├── tests/                     # Automated Quality Control Framework
│   ├── __init__.py            
│   └── test_financial_logic.py# Statistical math and parsing regex assert validation
│
├── .gitignore                 # Exclusion settings blocking local .db caches
├── LICENSE                    # open-source MIT Legal License
└── requirements.txt           # Python application micro-dependency tree
```

---

## 🧠 Advanced Statistical Model Specifications

The **Monte Carlo Risk Engine** uses a programmatic normal distribution model to run multi-variable stress-testing matrices:
$$\text{Simulated ROIC} \sim \mathcal{N}(\mu_{\text{Database Baseline}}, \sigma_{\text{Expected Volatility}})$$

* **Value-at-Risk (VaR)** is isolated at the strict **5th percentile margin boundary**, giving senior C-Suite leaders an absolute lower floor projection under severe silicon supply chain friction or power generation capacity locks.
* **Intelligent Document Parsing** combines standard Cash Capex strings with active capacity checks, translating physical electrical measurements like **Megawatts ($11M per MW real estate footprint)** directly into equivalent billion-dollar asset allocations automatically.

---

## 📦 Local Installation & Test Execution

To duplicate and execute this analytical platform locally on your machine, run these commands inside your terminal terminal environment:

```bash
# 1. Clone the repository framework
git clone https://github.com
cd roic-intelligence-app

# 2. Deploy micro-dependencies listed in requirements.txt
pip install -r requirements.txt

# 3. Boot up the Streamlit page router system locally
streamlit run frontend/app.py

# 4. Trigger the automated mathematical test suite validations
pytest tests/
```

---
*Created with architectural precision and verified execution boundaries by **Srinivasta**.*
