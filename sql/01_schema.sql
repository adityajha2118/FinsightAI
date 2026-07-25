-- ============================================================
-- FinSight AI — PostgreSQL Schema Definition
-- ============================================================
-- Run this script to create all tables from scratch.
-- This is the canonical DDL; the SQLAlchemy models mirror it.
-- ============================================================

-- Drop existing tables (reverse dependency order)
DROP TABLE IF EXISTS complaint_sentiment CASCADE;
DROP TABLE IF EXISTS customer_predictions CASCADE;
DROP TABLE IF EXISTS customer_segments CASCADE;
DROP TABLE IF EXISTS ab_tests CASCADE;
DROP TABLE IF EXISTS kyc_profiles CASCADE;
DROP TABLE IF EXISTS campaigns CASCADE;
DROP TABLE IF EXISTS complaints CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- ── 1. customers ─────────────────────────────────────────────
-- Source: BankChurners.csv (credit card customer demographics)
-- Business: Core table for churn, segmentation, and health scoring
CREATE TABLE customers (
    client_id           BIGINT PRIMARY KEY,
    attrition_flag      VARCHAR(30) NOT NULL,
    customer_age        INTEGER,
    gender              VARCHAR(1),
    dependent_count     INTEGER,
    education_level     VARCHAR(30),
    marital_status      VARCHAR(20),
    income_category     VARCHAR(30),
    card_category       VARCHAR(20),
    months_on_book      INTEGER,
    total_relationship_count INTEGER,
    months_inactive_12_mon   INTEGER,
    contacts_count_12_mon    INTEGER,
    credit_limit        NUMERIC(12,2),
    total_revolving_bal  NUMERIC(12,2),
    avg_open_to_buy     NUMERIC(12,2),
    total_amt_chng_q4_q1 NUMERIC(8,4),
    total_trans_amt     NUMERIC(12,2),
    total_trans_ct      INTEGER,
    total_ct_chng_q4_q1 NUMERIC(8,4),
    avg_utilization_ratio NUMERIC(6,4)
);

-- ── 2. transactions ──────────────────────────────────────────
-- Source: credit_card_transactions.csv
-- Business: Transaction-level analysis, spending patterns
CREATE TABLE transactions (
    transaction_id      BIGSERIAL PRIMARY KEY,
    client_id           BIGINT,
    transaction_date    TIMESTAMP,
    amount              NUMERIC(12,2),
    category            VARCHAR(150),
    merchant            VARCHAR(100),
    city                VARCHAR(100),
    state               VARCHAR(5),
    job                 VARCHAR(150),
    is_fraud            BOOLEAN DEFAULT FALSE
);
CREATE INDEX ix_transactions_client ON transactions(client_id);
CREATE INDEX ix_transactions_date ON transactions(transaction_date);

-- ── 3. complaints ────────────────────────────────────────────
-- Source: CFPB complaints dataset
-- Business: Complaint tracking, trend analysis, regulatory exposure
CREATE TABLE complaints (
    complaint_id        BIGINT PRIMARY KEY,
    date_received       DATE,
    product             VARCHAR(100),
    sub_product         VARCHAR(100),
    issue               VARCHAR(200),
    sub_issue           VARCHAR(200),
    narrative           TEXT,
    company_response    VARCHAR(100),
    company             VARCHAR(200),
    state               VARCHAR(5),
    zip_code            VARCHAR(10),
    submitted_via       VARCHAR(30),
    date_sent_to_company DATE,
    timely_response     VARCHAR(5),
    tags                VARCHAR(50)
);
CREATE INDEX ix_complaints_product ON complaints(product);
CREATE INDEX ix_complaints_date ON complaints(date_received);
CREATE INDEX ix_complaints_state ON complaints(state);

-- ── 4. campaigns ─────────────────────────────────────────────
-- Source: Bank Marketing Dataset (UCI)
-- Business: Campaign conversion prediction, channel optimization
CREATE TABLE campaigns (
    campaign_id         SERIAL PRIMARY KEY,
    age                 INTEGER,
    job                 VARCHAR(30),
    marital             VARCHAR(20),
    education           VARCHAR(30),
    default_credit      VARCHAR(10),
    housing             VARCHAR(5),
    loan                VARCHAR(5),
    contact             VARCHAR(20),
    month               VARCHAR(5),
    day_of_week         VARCHAR(5),
    duration            INTEGER,
    campaign_count      INTEGER,
    pdays               INTEGER,
    previous            INTEGER,
    poutcome            VARCHAR(20),
    emp_var_rate        NUMERIC(6,2),
    cons_price_idx      NUMERIC(8,4),
    cons_conf_idx       NUMERIC(8,2),
    euribor3m           NUMERIC(6,4),
    nr_employed         NUMERIC(8,2),
    subscribed          VARCHAR(5)
);

-- ── 5. kyc_profiles ──────────────────────────────────────────
-- Source: KYC Part 1 (transactions) + Part 2 (entity profiles)
-- Business: AML/KYC risk assessment and regulatory compliance
CREATE TABLE kyc_profiles (
    profile_id          SERIAL PRIMARY KEY,
    client_id           VARCHAR(50),
    client_name         VARCHAR(100),
    client_type         VARCHAR(30),
    sector              VARCHAR(50),
    sector_risk         VARCHAR(20),
    country             VARCHAR(80),
    pep_flag            INTEGER DEFAULT 0,
    sanctions_flag      INTEGER DEFAULT 0,
    fatf_country_flag   INTEGER DEFAULT 0,
    ofac_country_flag   INTEGER DEFAULT 0,
    sectoral_sanctions_flag INTEGER DEFAULT 0,
    ownership_opacity_score NUMERIC(4,3),
    -- Aggregated transaction risk flags
    ofac_match_flag     INTEGER DEFAULT 0,
    fatf_txn_flag       INTEGER DEFAULT 0,
    structuring_pattern_flag INTEGER DEFAULT 0,
    rapid_movement_flag INTEGER DEFAULT 0,
    trade_mispricing_flag INTEGER DEFAULT 0,
    transaction_count   INTEGER DEFAULT 0,
    total_transaction_amount NUMERIC(14,2) DEFAULT 0
);
CREATE INDEX ix_kyc_client ON kyc_profiles(client_id);
CREATE INDEX ix_kyc_country ON kyc_profiles(country);
CREATE INDEX ix_kyc_sector ON kyc_profiles(sector);

-- ── 6. ab_tests ──────────────────────────────────────────────
-- Source: A/B testing dataset
-- Business: Statistical experimentation for business decisions
CREATE TABLE ab_tests (
    record_id           SERIAL PRIMARY KEY,
    user_id             VARCHAR(50),
    experiment_group    VARCHAR(20),
    converted           BOOLEAN,
    revenue             NUMERIC(10,2),
    sessions            INTEGER,
    pages_viewed        INTEGER,
    time_spent          NUMERIC(8,2),
    experiment_name     VARCHAR(100) DEFAULT 'default_experiment',
    timestamp           TIMESTAMP
);
CREATE INDEX ix_ab_tests_group ON ab_tests(experiment_group);

-- ── 7. customer_segments (ML output) ─────────────────────────
-- Populated by: K-Means clustering pipeline
CREATE TABLE customer_segments (
    client_id           BIGINT PRIMARY KEY,
    cluster_id          INTEGER,
    segment_name        VARCHAR(50)
);

-- ── 8. customer_predictions (ML output) ──────────────────────
-- Populated by: XGBoost churn model + health scoring pipeline
CREATE TABLE customer_predictions (
    client_id           BIGINT PRIMARY KEY,
    churn_probability   NUMERIC(6,4),
    risk_label          VARCHAR(20),
    health_score        NUMERIC(6,2),
    activity_score      NUMERIC(6,4)
);

-- ── 9. complaint_sentiment (VADER output) ────────────────────
-- Populated by: VADER sentiment analysis pipeline
CREATE TABLE complaint_sentiment (
    complaint_id        BIGINT PRIMARY KEY,
    compound_score      NUMERIC(6,4),
    positive_score      NUMERIC(6,4),
    neutral_score       NUMERIC(6,4),
    negative_score      NUMERIC(6,4),
    sentiment_label     VARCHAR(20)
);
