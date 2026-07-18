from pathlib import Path
import pandas as pd
from dotenv import load_dotenv; load_dotenv()

CAMPAIGN_PATH = Path("data/processed/campaign_clean.csv")

def _load_data():
    df = pd.read_csv(CAMPAIGN_PATH)
    if 'y_binary' not in df.columns:
        df['y_binary'] = (df['y'] == 'yes').astype(int)
    return df

def get_campaign_success_rate() -> dict:
    """Return overall conversion rate and total record count."""
    df = _load_data()
    return {"success_rate": round(df['y_binary'].mean() * 100, 2), "total_records": len(df)}

def get_conversion_by_job() -> dict:
    """Return {job: conversion_rate} rounded to 4 decimal places."""
    df = _load_data()
    return df.groupby('job')['y_binary'].mean().round(4).to_dict()

def get_conversion_by_contact() -> dict:
    """Return {contact_method: conversion_rate} rounded to 4 decimal places."""
    df = _load_data()
    return df.groupby('contact')['y_binary'].mean().round(4).to_dict()

def get_conversion_by_month() -> dict:
    """Return {month: conversion_rate} rounded to 4 decimal places."""
    df = _load_data()
    return df.groupby('month')['y_binary'].mean().round(4).to_dict()

def get_full_campaign_stats() -> dict:
    """Return combined dict with success_rate, by_job, by_contact, by_month."""
    return {
        "success_rate": get_campaign_success_rate(),
        "by_job": get_conversion_by_job(),
        "by_contact": get_conversion_by_contact(),
        "by_month": get_conversion_by_month()
    }
