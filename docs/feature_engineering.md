# Feature Engineering Catalog

## Overview

This document catalogs every engineered feature in FinSight AI, including its formula, rationale, source data, and the modules that consume it.

---

## Customer Intelligence Features

### Behavioral Features

| Feature | Formula / Method | Rationale | Source |
|---------|-----------------|-----------|--------|
| `Total_Trans_Ct` | Count of transactions in 12 months | Primary engagement indicator | `customer_data.csv` |
| `Total_Trans_Amt` | Sum of transaction amounts | Spending power indicator | `customer_data.csv` |
| `Avg_Utilization_Ratio` | Revolving balance / Credit limit | Credit usage intensity | `customer_data.csv` |
| `Total_Revolving_Bal` | Current revolving balance | Debt exposure | `customer_data.csv` |
| `Months_Inactive_12_mon` | Count of inactive months in past year | Silent attrition signal | `customer_data.csv` |
| `Contacts_Count_12_mon` | Customer-initiated contacts | Engagement/frustration proxy | `customer_data.csv` |

### Derived Features

| Feature | Formula / Method | Rationale | Created In |
|---------|-----------------|-----------|-----------|
| `activity_score` | MinMaxScaler(weighted composite of frequency, recency, utilization) | Unified activity metric (0–1) | NB 07 |
| `churn_probability` | XGBoost.predict_proba() | Likelihood of account closure | NB 08 |
| `segment_name` | KMeans.predict() → label mapping | Customer persona assignment | NB 06 |
| `cluster_id` | KMeans.predict() | Raw cluster assignment (0-4) | NB 06 |

---

## Campaign Features

| Feature | Formula / Method | Rationale | Source |
|---------|-----------------|-----------|--------|
| `campaign` | Number of contacts in current campaign | Fatigue indicator | `bank_campaign.csv` |
| `previous` | Number of prior campaign contacts | Historical responsiveness | `bank_campaign.csv` |
| `pdays` | Days since last contact | Recency effect | `bank_campaign.csv` |
| `poutcome` | Outcome of previous campaign (encoded) | Strongest single predictor | `bank_campaign.csv` |
| `contacted_before` | Binary: pdays != 999 | Whether customer was previously contacted | NB 09 (engineered) |
| `campaign_intensity` | campaign / mean(campaign) | Relative contact pressure | NB 09 (engineered) |

### Macroeconomic Context Features

| Feature | Source | Rationale |
|---------|--------|-----------|
| `emp_var_rate` | Employment variation rate | Economic cycle indicator |
| `cons_price_idx` | Consumer price index | Inflation proxy |
| `cons_conf_idx` | Consumer confidence index | Sentiment proxy |
| `euribor3m` | 3-month Euribor rate | Interest rate environment |
| `nr_employed` | Number of employees (quarterly) | Labor market health |

---

## KYC / Compliance Features

### Transaction-Level Flags

| Feature | Type | Description |
|---------|------|-------------|
| `ofac_match_flag` | Binary | Match against OFAC sanctions list |
| `fatf_txn_flag` | Binary | Transaction flagged by FATF criteria |
| `structuring_pattern_flag` | Binary | Smurfing pattern detected |
| `rapid_movement_flag` | Binary | Unusual velocity of fund movement |
| `trade_mispricing_flag` | Binary | Trade-based money laundering indicator |

### Entity-Level Flags

| Feature | Type | Description |
|---------|------|-------------|
| `pep_flag` | Binary | Politically Exposed Person |
| `sanctions_flag` | Binary | Entity on sanctions list |
| `fatf_entity_flag` | Binary | Entity in FATF jurisdiction |
| `ofac_country_flag` | Binary | Domiciled in OFAC-listed country |
| `sectoral_sanctions_flag` | Binary | Industry under sanctions |
| `ownership_opacity_score` | Float [0–1] | Beneficial ownership transparency |
| `sector_risk` | Categorical | Industry risk level (Low/Medium/High) |

---

## NLP-Derived Features (LLM-Generated)

| Feature | Method | Output | Used By |
|---------|--------|--------|---------|
| `summary` | Gemini/GPT summarization | 1-2 sentence summary | Agent UI |
| `category` | Gemini/GPT classification | Complaint category label | Escalation model |
| `emotion` | Gemini/GPT emotion detection | Emotional state label | Routing rules |
| `word_count` | `len(narrative.split())` | Narrative length | Escalation model |

---

## Feature Encoding

### Categorical Encoding (for Escalation Model)

```python
CATEGORY_MAP = {
    "Billing": 0, "Fraud": 1, "Account Management": 2,
    "Credit Reporting": 3, "Debt Collection": 4, "Other": 5
}

EMOTION_MAP = {
    "Frustration": 0, "Anger": 1, "Distress": 2,
    "Legal Threat": 3, "Neutral": 4
}
```

### Scaling

- **StandardScaler**: Applied to segmentation features (zero mean, unit variance)
- **MinMaxScaler**: Applied to activity scoring (bounded 0–1)
- **SMOTE**: Applied to campaign training data (synthetic minority oversampling)
