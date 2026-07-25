"""
FinSight AI — Data Ingestion Pipeline.

Pipeline: CSV → Python Cleaning → PostgreSQL

This script reads raw CSV files, cleans them, and loads them into
PostgreSQL tables. It is designed to be run once during setup,
or re-run to refresh data.

Usage:
    cd FinSight-AI/backend
    python -m scripts.seed_data

    Or to seed specific tables:
    python -m scripts.seed_data --tables customers,complaints
"""

import argparse
import logging
import sys
import os
from pathlib import Path

import pandas as pd
import numpy as np
from sqlalchemy import text

# ── Path setup (run from backend/) ───────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database.engine import get_engine, Base
from src.database.models import (
    Customer, Transaction, Complaint, Campaign,
    KYCProfile, ABTest, CustomerSegment, CustomerPrediction,
    ComplaintSentiment,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Default raw data directory ────────────────────────────────
# CSV files are in the parent project root
RAW_DATA_DIR = Path(os.getenv(
    "DATA_RAW_DIR",
    str(Path(__file__).resolve().parent.parent.parent.parent)
))


# ═════════════════════════════════════════════════════════════
# CLEANING FUNCTIONS
# ═════════════════════════════════════════════════════════════

def clean_customers(raw_dir: Path) -> pd.DataFrame:
    """Clean the BankChurners/customer_data CSV.

    Steps:
        1. Drop the two Naive_Bayes classifier columns (data leakage)
        2. Standardize column names
        3. Handle missing education/income values
    """
    filepath = raw_dir / "customer_data.csv"
    logger.info("Reading customers from %s", filepath)
    df = pd.read_csv(filepath)
    logger.info("  Raw shape: %s", df.shape)

    # Drop Naive Bayes columns (they start with "Naive_Bayes")
    nb_cols = [c for c in df.columns if c.startswith("Naive_Bayes")]
    df = df.drop(columns=nb_cols, errors="ignore")

    # Standardize 'Unknown' values
    for col in ["Education_Level", "Marital_Status", "Income_Category"]:
        if col in df.columns:
            df[col] = df[col].replace("Unknown", "Unknown")

    # Rename to match our schema
    rename_map = {
        "CLIENTNUM": "client_id",
        "Attrition_Flag": "attrition_flag",
        "Customer_Age": "customer_age",
        "Gender": "gender",
        "Dependent_count": "dependent_count",
        "Education_Level": "education_level",
        "Marital_Status": "marital_status",
        "Income_Category": "income_category",
        "Card_Category": "card_category",
        "Months_on_book": "months_on_book",
        "Total_Relationship_Count": "total_relationship_count",
        "Months_Inactive_12_mon": "months_inactive_12_mon",
        "Contacts_Count_12_mon": "contacts_count_12_mon",
        "Credit_Limit": "credit_limit",
        "Total_Revolving_Bal": "total_revolving_bal",
        "Avg_Open_To_Buy": "avg_open_to_buy",
        "Total_Amt_Chng_Q4_Q1": "total_amt_chng_q4_q1",
        "Total_Trans_Amt": "total_trans_amt",
        "Total_Trans_Ct": "total_trans_ct",
        "Total_Ct_Chng_Q4_Q1": "total_ct_chng_q4_q1",
        "Avg_Utilization_Ratio": "avg_utilization_ratio",
    }
    df = df.rename(columns=rename_map)

    # Keep only columns that exist in our schema
    schema_cols = list(rename_map.values())
    df = df[[c for c in schema_cols if c in df.columns]]

    logger.info("  Clean shape: %s", df.shape)
    return df


def clean_transactions(raw_dir: Path, max_rows: int = 100_000) -> pd.DataFrame:
    """Clean credit card transactions. Sample to max_rows for manageability.

    Args:
        raw_dir: Directory containing the CSV
        max_rows: Maximum number of rows to load (default: 100,000)
    """
    # Try multiple possible filenames
    candidates = [
        raw_dir / "FinSight-AI" / "data" / "processed" / "transaction_clean.csv",
        raw_dir / "credit_card_transactions.csv",
    ]
    filepath = None
    for p in candidates:
        if p.exists():
            filepath = p
            break

    if filepath is None:
        logger.warning("No transaction CSV found. Skipping transactions.")
        return pd.DataFrame()

    logger.info("Reading transactions from %s (max %d rows)", filepath, max_rows)

    # Read only max_rows to keep PostgreSQL size manageable
    df = pd.read_csv(filepath, nrows=max_rows)
    logger.info("  Raw shape: %s", df.shape)

    # Standardize column names
    col_map = {}
    for col in df.columns:
        lower = col.lower().strip()
        if lower in ("trans_date_trans_time", "transaction_date", "date"):
            col_map[col] = "transaction_date"
        elif lower in ("amt", "amount"):
            col_map[col] = "amount"
        elif lower == "category":
            col_map[col] = "category"
        elif lower == "merchant":
            col_map[col] = "merchant"
        elif lower == "city":
            col_map[col] = "city"
        elif lower == "state":
            col_map[col] = "state"
        elif lower == "job":
            col_map[col] = "job"
        elif lower == "is_fraud":
            col_map[col] = "is_fraud"

    df = df.rename(columns=col_map)

    # Parse transaction date
    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    # Convert is_fraud to boolean
    if "is_fraud" in df.columns:
        df["is_fraud"] = df["is_fraud"].astype(bool)

    # Keep only schema columns
    keep_cols = ["transaction_date", "amount", "category", "merchant",
                 "city", "state", "job", "is_fraud"]
    df = df[[c for c in keep_cols if c in df.columns]]

    # Add client_id placeholder (not in raw transaction data)
    if "client_id" not in df.columns:
        df["client_id"] = None

    logger.info("  Clean shape: %s", df.shape)
    return df


def clean_complaints(raw_dir: Path) -> pd.DataFrame:
    """Clean CFPB complaint data.

    Steps:
        1. Parse dates
        2. Standardize column names
        3. Handle null narratives
    """
    filepath = raw_dir / "cfpb_complaints.csv"
    logger.info("Reading complaints from %s", filepath)
    df = pd.read_csv(filepath, low_memory=False)
    logger.info("  Raw shape: %s", df.shape)

    # Rename to match schema
    rename_map = {
        "Complaint ID": "complaint_id",
        "Date received": "date_received",
        "Product": "product",
        "Sub-product": "sub_product",
        "Issue": "issue",
        "Sub-issue": "sub_issue",
        "Consumer complaint narrative": "narrative",
        "Company": "company",
        "State": "state",
        "ZIP code": "zip_code",
        "Submitted via": "submitted_via",
        "Date sent to company": "date_sent_to_company",
        "Company response to consumer": "company_response",
        "Timely response?": "timely_response",
        "Tags": "tags",
    }
    df = df.rename(columns=rename_map)

    # Parse dates
    for date_col in ["date_received", "date_sent_to_company"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce").dt.date

    # Drop duplicates on complaint_id
    if "complaint_id" in df.columns:
        df = df.drop_duplicates(subset=["complaint_id"])

    # Handle null narratives
    df["narrative"] = df["narrative"].fillna("")

    # Standardize state codes (trim whitespace, uppercase)
    if "state" in df.columns:
        df["state"] = df["state"].str.strip().str.upper()

    # Keep schema columns
    schema_cols = [
        "complaint_id", "date_received", "product", "sub_product",
        "issue", "sub_issue", "narrative", "company_response", "company",
        "state", "zip_code", "submitted_via", "date_sent_to_company",
        "timely_response", "tags",
    ]
    df = df[[c for c in schema_cols if c in df.columns]]

    logger.info("  Clean shape: %s", df.shape)
    return df


def clean_campaigns(raw_dir: Path) -> pd.DataFrame:
    """Clean bank marketing campaign data.

    Steps:
        1. Rename dot-separated columns
        2. Map target variable
        3. Drop index column if present
    """
    filepath = raw_dir / "bank_campaign.csv"
    logger.info("Reading campaigns from %s", filepath)
    df = pd.read_csv(filepath)
    logger.info("  Raw shape: %s", df.shape)

    # Drop index column
    if "index" in df.columns:
        df = df.drop(columns=["index"])

    # Rename columns to match schema
    rename_map = {
        "default": "default_credit",
        "campaign": "campaign_count",
        "y": "subscribed",
        "emp.var.rate": "emp_var_rate",
        "cons.price.idx": "cons_price_idx",
        "cons.conf.idx": "cons_conf_idx",
        "nr.employed": "nr_employed",
    }
    df = df.rename(columns=rename_map)

    logger.info("  Clean shape: %s", df.shape)
    return df


def clean_kyc(raw_dir: Path) -> pd.DataFrame:
    """Clean and merge KYC Part 1 (transactions) + Part 2 (entity profiles).

    Steps:
        1. Aggregate Part 1 transaction flags per client_id
        2. Merge with Part 2 entity profiles
        3. Fill missing flags with 0
    """
    path1 = raw_dir / "kyc_part1.csv"
    path2 = raw_dir / "kyc_part2.csv"

    logger.info("Reading KYC Part 1 from %s", path1)
    df1 = pd.read_csv(path1)
    logger.info("  Part 1 shape: %s", df1.shape)

    logger.info("Reading KYC Part 2 from %s", path2)
    df2 = pd.read_csv(path2)
    logger.info("  Part 2 shape: %s", df2.shape)

    # Aggregate Part 1: sum risk flags per client, count transactions
    flag_cols = [
        "ofac_match_flag", "fatf_country_flag", "structuring_pattern_flag",
        "rapid_movement_flag", "trade_mispricing_flag",
    ]
    agg_dict = {col: "sum" for col in flag_cols if col in df1.columns}
    agg_dict["transaction_id"] = "count"
    if "amount" in df1.columns:
        agg_dict["amount"] = "sum"

    txn_agg = df1.groupby("client_id").agg(agg_dict).reset_index()
    txn_agg = txn_agg.rename(columns={
        "transaction_id": "transaction_count",
        "amount": "total_transaction_amount",
        "fatf_country_flag": "fatf_txn_flag",
    })

    # Merge with Part 2
    merged = df2.merge(txn_agg, on="client_id", how="left")

    # Fill missing values
    int_cols = [
        "pep_flag", "sanctions_flag", "fatf_country_flag",
        "ofac_country_flag", "sectoral_sanctions_flag",
        "ofac_match_flag", "fatf_txn_flag", "structuring_pattern_flag",
        "rapid_movement_flag", "trade_mispricing_flag", "transaction_count",
    ]
    for col in int_cols:
        if col in merged.columns:
            merged[col] = merged[col].fillna(0).astype(int)
    if "total_transaction_amount" in merged.columns:
        merged["total_transaction_amount"] = merged["total_transaction_amount"].fillna(0)
    if "ownership_opacity_score" in merged.columns:
        merged["ownership_opacity_score"] = merged["ownership_opacity_score"].fillna(0)

    logger.info("  Merged KYC shape: %s", merged.shape)
    return merged


def generate_ab_test_data() -> pd.DataFrame:
    """Generate a realistic A/B testing dataset.

    Simulates a website conversion experiment:
    - Control: existing checkout page
    - Treatment: redesigned checkout page with simplified flow

    This is a synthetic but statistically valid dataset with
    a real treatment effect baked in (~3% lift in conversion).
    """
    logger.info("Generating A/B testing dataset")
    np.random.seed(42)
    n_users = 10_000

    # Control group: 12% base conversion rate
    n_control = n_users // 2
    control = pd.DataFrame({
        "user_id": [f"user_{i}" for i in range(n_control)],
        "experiment_group": "control",
        "converted": np.random.binomial(1, 0.12, n_control).astype(bool),
        "sessions": np.random.poisson(3, n_control),
        "pages_viewed": np.random.poisson(5, n_control),
        "time_spent": np.round(np.random.exponential(4.5, n_control), 2),
        "experiment_name": "checkout_redesign_q4_2024",
    })

    # Treatment group: 15% conversion rate (~3% absolute lift)
    n_treatment = n_users - n_control
    treatment = pd.DataFrame({
        "user_id": [f"user_{i}" for i in range(n_control, n_users)],
        "experiment_group": "treatment",
        "converted": np.random.binomial(1, 0.15, n_treatment).astype(bool),
        "sessions": np.random.poisson(3.2, n_treatment),
        "pages_viewed": np.random.poisson(5.5, n_treatment),
        "time_spent": np.round(np.random.exponential(5.0, n_treatment), 2),
        "experiment_name": "checkout_redesign_q4_2024",
    })

    # Revenue: $0 if not converted, else lognormal distribution
    for group_df in [control, treatment]:
        group_df["revenue"] = np.where(
            group_df["converted"],
            np.round(np.random.lognormal(3.5, 0.8, len(group_df)), 2),
            0.0,
        )

    df = pd.concat([control, treatment], ignore_index=True)

    # Add timestamps spanning 2 weeks
    base_date = pd.Timestamp("2024-10-01")
    df["timestamp"] = base_date + pd.to_timedelta(
        np.random.uniform(0, 14 * 24 * 60, len(df)), unit="min"
    )

    logger.info("  A/B test shape: %s", df.shape)
    return df


# ═════════════════════════════════════════════════════════════
# LOADING FUNCTIONS
# ═════════════════════════════════════════════════════════════

def load_to_postgres(df: pd.DataFrame, table_name: str, engine, if_exists: str = "append"):
    """Load a DataFrame into a PostgreSQL table.

    Args:
        df: Cleaned DataFrame
        table_name: Target table name
        engine: SQLAlchemy engine
        if_exists: 'replace' drops & recreates, 'append' adds rows
    """
    if df.empty:
        logger.warning("  Empty DataFrame, skipping %s", table_name)
        return

    logger.info("  Loading %d rows into '%s'...", len(df), table_name)
    df.to_sql(
        table_name,
        engine,
        if_exists=if_exists,
        index=False,
        method="multi",
        chunksize=5000,
    )
    logger.info("  ✓ '%s' loaded successfully", table_name)


# ═════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═════════════════════════════════════════════════════════════

AVAILABLE_TABLES = [
    "customers", "transactions", "complaints", "campaigns",
    "kyc_profiles", "ab_tests",
]


def run_pipeline(tables: list[str] | None = None, raw_dir: Path | None = None):
    """Execute the full data ingestion pipeline.

    Args:
        tables: Specific tables to seed (None = all)
        raw_dir: Override raw data directory
    """
    if raw_dir is None:
        raw_dir = RAW_DATA_DIR

    logger.info("=" * 60)
    logger.info("FinSight AI — Data Ingestion Pipeline")
    logger.info("Raw data directory: %s", raw_dir)
    logger.info("=" * 60)

    engine = get_engine()

    # Create all tables from ORM models
    logger.info("Creating database tables from ORM models...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("✓ Tables created")

    targets = tables or AVAILABLE_TABLES

    if "customers" in targets:
        df = clean_customers(raw_dir)
        load_to_postgres(df, "customers", engine)

    if "transactions" in targets:
        df = clean_transactions(raw_dir, max_rows=100_000)
        load_to_postgres(df, "transactions", engine)

    if "complaints" in targets:
        df = clean_complaints(raw_dir)
        load_to_postgres(df, "complaints", engine)

    if "campaigns" in targets:
        df = clean_campaigns(raw_dir)
        load_to_postgres(df, "campaigns", engine)

    if "kyc_profiles" in targets:
        df = clean_kyc(raw_dir)
        load_to_postgres(df, "kyc_profiles", engine)

    if "ab_tests" in targets:
        df = generate_ab_test_data()
        load_to_postgres(df, "ab_tests", engine)

    # Create SQL views
    logger.info("Creating SQL views...")
    views_path = Path(__file__).resolve().parent.parent.parent / "sql" / "02_views.sql"
    if views_path.exists():
        sql_content = views_path.read_text(encoding="utf-8")
        # Split on semicolons and execute each statement in its own transaction
        statements = sql_content.split(";")
        for stmt in statements:
            stmt = stmt.strip()
            if stmt and ("CREATE" in stmt.upper() or "DROP" in stmt.upper()):
                try:
                    with engine.connect() as conn:
                        conn.execute(text(stmt))
                        conn.commit()
                except Exception as e:
                    logger.warning("View creation warning: %s", e)
        logger.info("✓ SQL views created")
    else:
        logger.warning("Views file not found at %s", views_path)

    logger.info("=" * 60)
    logger.info("✓ Data ingestion pipeline complete!")
    logger.info("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FinSight AI Data Ingestion")
    parser.add_argument(
        "--tables",
        type=str,
        default=None,
        help="Comma-separated list of tables to seed (default: all)",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Path to raw CSV files directory",
    )
    args = parser.parse_args()

    target_tables = args.tables.split(",") if args.tables else None
    data_dir = Path(args.data_dir) if args.data_dir else None

    run_pipeline(tables=target_tables, raw_dir=data_dir)
