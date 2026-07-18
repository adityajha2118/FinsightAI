# Database Schema

## Overview

While the current implementation uses CSV/Parquet files for data storage, the system is designed for migration to PostgreSQL. This document defines the production database schema.

---

## Entity Relationship Diagram

```mermaid
erDiagram
    CUSTOMERS ||--o{ TRANSACTIONS : has
    CUSTOMERS ||--o{ COMPLAINTS : files
    CUSTOMERS ||--o| CUSTOMER_RISK_PROFILES : has
    CUSTOMERS ||--o| CUSTOMER_SEGMENTS : belongs_to
    CUSTOMERS ||--o{ CAMPAIGN_CONTACTS : receives
    CAMPAIGNS ||--o{ CAMPAIGN_CONTACTS : includes
    COMPLAINTS ||--o| COMPLAINT_ANALYSIS : analyzed_by

    CUSTOMERS {
        bigint client_id PK
        int customer_age
        varchar gender
        varchar income_category
        varchar card_category
        int months_on_book
        float credit_limit
        float total_revolving_bal
        float avg_utilization_ratio
        int total_trans_ct
        float total_trans_amt
        int months_inactive_12_mon
        varchar attrition_flag
        timestamp created_at
        timestamp updated_at
    }

    TRANSACTIONS {
        bigint transaction_id PK
        bigint client_id FK
        timestamp trans_datetime
        float amount
        varchar merchant
        varchar category
        varchar city
        varchar state
        boolean is_fraud
    }

    CUSTOMER_SEGMENTS {
        bigint client_id PK "FK"
        int cluster_id
        varchar segment_name
        float activity_score
        float churn_probability
        timestamp scored_at
    }

    CUSTOMER_RISK_PROFILES {
        bigint profile_id PK
        bigint client_id FK
        float kyc_risk_score
        varchar risk_tier
        boolean pep_flag
        boolean sanctions_flag
        boolean ofac_match
        float ownership_opacity_score
        timestamp assessed_at
    }

    CAMPAIGNS {
        int campaign_id PK
        varchar campaign_name
        date start_date
        date end_date
        varchar channel
        varchar target_segment
    }

    CAMPAIGN_CONTACTS {
        bigint contact_id PK
        int campaign_id FK
        bigint client_id FK
        int contact_count
        varchar contact_method
        varchar outcome
        timestamp contacted_at
    }

    COMPLAINTS {
        bigint complaint_id PK
        bigint client_id FK
        text narrative
        varchar product
        varchar issue
        varchar sub_issue
        varchar company_response
        boolean timely_response
        timestamp received_date
    }

    COMPLAINT_ANALYSIS {
        bigint analysis_id PK
        bigint complaint_id FK
        text summary
        varchar category
        varchar emotion
        float escalation_probability
        varchar priority_level
        varchar assigned_team
        text suggested_response
        timestamp analyzed_at
    }
```

---

## Table Descriptions

| Table | Purpose | Est. Rows |
|-------|---------|-----------|
| `customers` | Core customer demographics and behavioral metrics | 10,127 |
| `transactions` | Individual transaction records | 1,296,675 |
| `customer_segments` | ML-derived segment labels and scores | 10,127 |
| `customer_risk_profiles` | KYC/AML risk assessments | 52,000 |
| `campaigns` | Marketing campaign definitions | ~50 |
| `campaign_contacts` | Individual customer-campaign interactions | ~100 |
| `complaints` | Raw customer complaint records | 24,665 |
| `complaint_analysis` | AI-generated analysis results | 24,665 |

---

## Indexes

```sql
-- High-frequency lookup patterns
CREATE INDEX idx_customers_attrition ON customers(attrition_flag);
CREATE INDEX idx_segments_name ON customer_segments(segment_name);
CREATE INDEX idx_risk_tier ON customer_risk_profiles(risk_tier);
CREATE INDEX idx_complaints_product ON complaints(product);
CREATE INDEX idx_analysis_priority ON complaint_analysis(priority_level);
CREATE INDEX idx_transactions_client ON transactions(client_id);
CREATE INDEX idx_transactions_fraud ON transactions(is_fraud);
```

---

## Migration Path

The current CSV-based implementation maps directly to this schema:

| CSV File | Target Table |
|----------|-------------|
| `customer_clean.csv` | `customers` |
| `transaction_clean.csv` | `transactions` |
| `customer_with_segments.csv` | `customer_segments` |
| `kyc_clean.csv` | `customer_risk_profiles` |
| `campaign_clean.csv` | `campaigns` + `campaign_contacts` |
| `complaints_clean.csv` | `complaints` |
| `complaints_with_escalation.csv` | `complaint_analysis` |
