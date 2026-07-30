# Placeholder module matching the architecture layout
def optimize_v_order_delta():
    print("Simulating V-Order storage cluster optimization optimizations.")

def calculate_lens_metrics(value: float, placeholder: float) -> float:
    """Clean math helper for company_lens.py."""
    return round(value, 1)

def simulate_lab_delta(base_val: float, delta_pct: float) -> float:
    """Clean simulation helper for what_if_lab.py."""
    return round(base_val * (1 + (delta_pct / 100)), 2)

def run_monte_carlo_math(active_baseline_roic: float, market_volatility: float, target_hurdle_rate: float):
    """Offloaded heavy mathematical logic for what_if_lab.py Monte Carlo simulation."""
    import numpy as np
    
    np.random.seed(42)
    simulated_returns = np.random.normal(loc=active_baseline_roic, scale=market_volatility, size=1000)
    
    failing_trials = simulated_returns[simulated_returns < target_hurdle_rate]
    bubble_risk_probability = (len(failing_trials) / 1000.0) * 100.0
    avg_sim_return = np.mean(simulated_returns)
    worst_case_scenario = np.percentile(simulated_returns, 5)
    
    return avg_sim_return, bubble_risk_probability, worst_case_scenario

def get_company_registry_matrix(active_capex, r_msft, r_gcp, r_aws, r_meta, active_roic):
    """Offloaded corporate registry dictionary to drop frontend character footprint."""
    import pandas as pd
    return pd.DataFrame({
        "Company / Cluster Entity": [
            "Microsoft (Azure)", "Alphabet (GCP)", "Amazon (AWS)", "Meta Infrastructure", "Oracle Cloud", "Alibaba Group",
            "CoreWeave AI", "Lambda Labs", "Crusoe Energy", "NVIDIA Corporation", "FluidStack", "Nebius", "Nscale", 
            "OpenAI Compute Node", "Anthropic Cluster"
        ],
        "Segment Classification": [
            "Hyperscaler Core", "Hyperscaler Core", "Hyperscaler Core", "Hyperscaler Core", "Hyperscaler Core", "Hyperscaler Core",
            "Specialized Neocloud", "Specialized Neocloud", "Specialized Neocloud", "Hardware Silicon Designer", "Specialized Neocloud", "Specialized Neocloud", "Specialized Neocloud",
            "Frontier Model Dev", "Frontier Model Dev"
        ],
        "Allocated Capex Intensity ($B)": [
            round(active_capex * 0.28, 1), round(active_capex * 0.22, 1), round(active_capex * 0.20, 1), 
            round(active_capex * 0.14, 1), round(active_capex * 0.06, 1), round(active_capex * 0.03, 1),
            round(active_capex * 0.02, 1), round(active_capex * 0.01, 1), round(active_capex * 0.01, 1),
            round(active_capex * 0.01, 1), round(active_capex * 0.005, 1), round(active_capex * 0.005, 1), 
            round(active_capex * 0.005, 1), round(active_capex * 0.003, 1), round(active_capex * 0.002, 1)
        ],
        "Isolated Operating Return (%)": [
            round(r_msft, 1), round(r_gcp, 1), round(r_aws, 1), round(r_meta, 1), 
            round(active_roic - 1.2, 1), round(active_roic - 3.4, 1), round(active_roic - 6.2, 1), 
            round(active_roic - 5.8, 1), round(active_roic - 4.1, 1), round(active_roic + 14.8, 1), 
            round(active_roic - 7.3, 1), round(active_roic - 6.5, 1), round(active_roic - 7.0, 1), 
            round(active_roic - 8.4, 1), round(active_roic - 9.1, 1)
        ],
        "Historical Return Growth (pp/yr)": [
            1.5, 0.8, 1.2, 2.1, 1.7, 0.5, 3.6, 3.2, 2.4, 5.8, 1.8, 2.0, 1.5, 4.2, 3.9
        ],
        "Credit Risk Profile (S&P)": [
            "AAA (Excellent)", "AA- (High Quality)", "AA (High Quality)", "AA- (High Quality)", "BBB (Investment Grade)", "A+ (Strong)",
            "B+ (Speculative/High Yield)", "Private (Unrated)", "Private (Unrated)", "AAA (Excellent Equivalent)", "Private (Unrated)", "Unrated", 
            "Private (Unrated)", "Borrowing MSFT Credit", "Borrowing AMZN Credit"
        ]
    })
