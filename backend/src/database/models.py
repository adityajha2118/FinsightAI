"""
FinSight AI — SQLAlchemy ORM Models.

Defines all 9 PostgreSQL tables as Python classes.
These mirror the SQL DDL in sql/01_schema.sql.

Tables:
    customers           — Core customer demographics & behavior
    transactions        — Transaction-level records
    complaints          — CFPB consumer complaint records
    campaigns           — Bank marketing campaign records
    kyc_profiles        — KYC entity risk profiles
    ab_tests            — A/B testing experiment records
    customer_segments   — ML output: segment assignments
    customer_predictions — ML output: churn & health scores
    complaint_sentiment — VADER sentiment scores per complaint
"""

from datetime import date, datetime
from sqlalchemy import (
    Column, Integer, BigInteger, String, Float, Boolean, Date, DateTime,
    Text, ForeignKey, Index,
)
from src.database.engine import Base


# ── Core Business Tables ──────────────────────────────────────

class Customer(Base):
    """Credit card customer demographics and behavioral metrics."""
    __tablename__ = "customers"

    client_id = Column(BigInteger, primary_key=True, comment="Unique customer identifier")
    attrition_flag = Column(Text, nullable=False, comment="Existing Customer / Attrited Customer")
    customer_age = Column(Integer, comment="Customer age in years")
    gender = Column(Text, comment="M or F")
    dependent_count = Column(Integer)
    education_level = Column(Text)
    marital_status = Column(Text)
    income_category = Column(Text)
    card_category = Column(Text)
    months_on_book = Column(Integer, comment="Tenure in months")
    total_relationship_count = Column(Integer)
    months_inactive_12_mon = Column(Integer, comment="Months inactive in last 12")
    contacts_count_12_mon = Column(Integer)
    credit_limit = Column(Float)
    total_revolving_bal = Column(Float)
    avg_open_to_buy = Column(Float)
    total_amt_chng_q4_q1 = Column(Float, comment="Change in transaction amount Q4 vs Q1")
    total_trans_amt = Column(Float, comment="Total transaction amount (12 months)")
    total_trans_ct = Column(Integer, comment="Total transaction count (12 months)")
    total_ct_chng_q4_q1 = Column(Float, comment="Change in transaction count Q4 vs Q1")
    avg_utilization_ratio = Column(Float)


class Transaction(Base):
    """Individual credit card transactions."""
    __tablename__ = "transactions"

    transaction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    client_id = Column(BigInteger, index=True, comment="Links to customers table")
    transaction_date = Column(DateTime)
    amount = Column(Float)
    category = Column(Text)
    merchant = Column(Text)
    city = Column(Text)
    state = Column(Text)
    job = Column(Text)
    is_fraud = Column(Boolean, default=False)

    __table_args__ = (
        Index("ix_transactions_date", "transaction_date"),
    )


class Complaint(Base):
    """CFPB consumer complaint records."""
    __tablename__ = "complaints"

    complaint_id = Column(BigInteger, primary_key=True)
    date_received = Column(Date)
    product = Column(Text)
    sub_product = Column(Text)
    issue = Column(Text)
    sub_issue = Column(Text)
    narrative = Column(Text, comment="Consumer complaint narrative text")
    company_response = Column(Text)
    company = Column(Text)
    state = Column(Text)
    zip_code = Column(Text)
    submitted_via = Column(Text)
    date_sent_to_company = Column(Date)
    timely_response = Column(Text, comment="Yes or No")
    tags = Column(Text)

    __table_args__ = (
        Index("ix_complaints_product", "product"),
        Index("ix_complaints_date", "date_received"),
        Index("ix_complaints_state", "state"),
    )


class Campaign(Base):
    """Bank marketing campaign records (term deposit subscription)."""
    __tablename__ = "campaigns"

    campaign_id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer)
    job = Column(Text)
    marital = Column(Text)
    education = Column(Text)
    default_credit = Column(Text, comment="Has credit in default?")
    housing = Column(Text)
    loan = Column(Text)
    contact = Column(Text, comment="Contact type: cellular/telephone")
    month = Column(Text)
    day_of_week = Column(Text)
    duration = Column(Integer, comment="Last contact duration in seconds")
    campaign_count = Column(Integer, comment="Number of contacts during this campaign")
    pdays = Column(Integer, comment="Days since last contact from previous campaign")
    previous = Column(Integer, comment="Number of contacts before this campaign")
    poutcome = Column(Text, comment="Outcome of previous campaign")
    emp_var_rate = Column(Float)
    cons_price_idx = Column(Float)
    cons_conf_idx = Column(Float)
    euribor3m = Column(Float)
    nr_employed = Column(Float)
    subscribed = Column(Text, comment="Did the client subscribe? yes/no")


class KYCProfile(Base):
    """Know Your Customer entity risk profiles."""
    __tablename__ = "kyc_profiles"

    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Text, index=True)
    client_name = Column(Text)
    client_type = Column(Text)
    sector = Column(Text)
    sector_risk = Column(Text)
    country = Column(Text)
    pep_flag = Column(Integer, comment="Politically Exposed Person: 0 or 1")
    sanctions_flag = Column(Integer, comment="Sanctions match: 0 or 1")
    fatf_country_flag = Column(Integer)
    ofac_country_flag = Column(Integer)
    sectoral_sanctions_flag = Column(Integer)
    ownership_opacity_score = Column(Float, comment="0.0 to 1.0, higher = more opaque")
    # Transaction-level risk flags (aggregated from KYC Part 1)
    ofac_match_flag = Column(Integer, default=0)
    fatf_txn_flag = Column(Integer, default=0)
    structuring_pattern_flag = Column(Integer, default=0)
    rapid_movement_flag = Column(Integer, default=0)
    trade_mispricing_flag = Column(Integer, default=0)
    transaction_count = Column(Integer, default=0)
    total_transaction_amount = Column(Float, default=0.0)

    __table_args__ = (
        Index("ix_kyc_country", "country"),
        Index("ix_kyc_sector", "sector"),
    )


class ABTest(Base):
    """Synthetic A/B testing data."""
    __tablename__ = "ab_tests"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Text, index=True)
    experiment_group = Column(Text, comment="control or treatment")
    converted = Column(Boolean, comment="Did the user convert?")
    revenue = Column(Float, nullable=True, comment="Revenue generated (if applicable)")
    sessions = Column(Integer, nullable=True, comment="Number of sessions")
    pages_viewed = Column(Integer, nullable=True, comment="Pages viewed per session")
    time_spent = Column(Float, nullable=True, comment="Time spent in minutes")
    experiment_name = Column(Text, default="default_experiment")
    timestamp = Column(DateTime, nullable=True)
# ── ML Output Tables ──────────────────────────────────────────

class CustomerSegment(Base):
    """ML-generated customer segment assignments."""
    __tablename__ = "customer_segments"

    client_id = Column(BigInteger, primary_key=True)
    cluster_id = Column(Integer, comment="K-Means cluster number")
    segment_name = Column(Text, comment="Human-readable segment label")


class CustomerPrediction(Base):
    """ML-generated churn and health predictions."""
    __tablename__ = "customer_predictions"

    client_id = Column(BigInteger, primary_key=True)
    churn_probability = Column(Float, comment="0.0 to 1.0")
    risk_label = Column(Text, comment="High Risk / Medium Risk / Low Risk")
    health_score = Column(Float, comment="Composite health score 0-100")
    activity_score = Column(Float, comment="Activity score 0-1")


class ComplaintSentiment(Base):
    """VADER sentiment analysis results per complaint."""
    __tablename__ = "complaint_sentiment"

    complaint_id = Column(BigInteger, primary_key=True)
    compound_score = Column(Float, comment="VADER compound: -1.0 to 1.0")
    positive_score = Column(Float)
    neutral_score = Column(Float)
    negative_score = Column(Float)
    sentiment_label = Column(Text, comment="Positive / Neutral / Negative")
