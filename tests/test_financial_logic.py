import pytest
# FIXED: Target function imported from the correct bronze ingestion module path
from data_pipeline.ingestion_bronze import parse_metrics

def test_accurate_string_metric_parsing():
    """Verify regular expressions cleanly parse financial targets."""
    sample_text = "The hyperscalers invested $357.5B in cash capex while sustaining an average 29.7% adjusted ROIC."
    extracted_data = parse_metrics(sample_text)
    
    assert extracted_data["capex"] == 357.5
    assert extracted_data["roic"] == 29.7

def test_parsing_fallback_tolerance():
    """Verify system defaults operate correctly if patterns aren't identified."""
    empty_unrelated_text = "Plain text containing no quantitative analyst indicators."
    fallback_data = parse_metrics(empty_unrelated_text)
    
    assert fallback_data["capex"] == 357.5
    assert fallback_data["roic"] == 29.7

def test_edge_case_formatting():
    """Ensure parser regex handles varying spaces, lowercase text, and spelling changes."""
    tricky_text = "projected capex is 120.5b while expected roic sits near 18.5%"
    extracted_data = parse_metrics(tricky_text)
    
    assert extracted_data["capex"] == 120.5
    assert extracted_data["roic"] == 18.5
