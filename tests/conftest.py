"""Shared pytest fixtures for FinSight AI tests."""

import pytest
import pandas as pd
from pathlib import Path


@pytest.fixture
def sample_customer_data():
    """Create sample customer DataFrame for testing."""
    return pd.DataFrame({
        "CLIENTNUM": [1001, 1002, 1003],
        "Customer_Age": [45, 30, 55],
        "Gender": ["M", "F", "M"],
        "Credit_Limit": [12000, 5000, 25000],
        "Total_Trans_Amt": [5000, 1200, 15000],
        "Total_Trans_Ct": [60, 15, 90],
        "Avg_Utilization_Ratio": [0.3, 0.8, 0.1],
        "Total_Revolving_Bal": [2000, 4000, 500],
        "Months_Inactive_12_mon": [1, 4, 0],
        "Attrition_Flag": ["Existing Customer", "Attrited Customer", "Existing Customer"],
    })


@pytest.fixture
def sample_complaint_narrative():
    """Sample complaint text for agent testing."""
    return (
        "I have been trying to dispute a fraudulent charge on my credit card "
        "for the past three months. Every time I call, I am put on hold for "
        "over an hour and then disconnected. This is unacceptable and I am "
        "considering filing a complaint with the CFPB."
    )


@pytest.fixture
def project_root():
    """Return the project root path."""
    return Path(__file__).parent.parent
