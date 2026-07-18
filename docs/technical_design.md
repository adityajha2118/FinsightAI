# Technical Design Document

## 1. Introduction

This document provides technical specifications for all ML models, algorithms, and AI systems in FinSight AI.

---

## 2. Customer Segmentation

### Algorithm: K-Means Clustering
- **k**: 5 (determined via Elbow Method + Silhouette Score)
- **Features**: `Credit_Limit`, `Total_Trans_Amt`, `Total_Trans_Ct`, `Avg_Utilization_Ratio`, `Total_Revolving_Bal`, `Months_Inactive_12_mon`
- **Preprocessing**: StandardScaler normalization
- **Cluster Interpretation**:

| Cluster | Label | Characteristics |
|---------|-------|----------------|
| 0 | Premium Customers | High credit limit, high spend |
| 1 | Daily Spenders | High transaction frequency, low avg ticket |
| 2 | Deal Hunters | Low revolving balance, moderate activity |
| 3 | At-Risk Customers | High inactivity, declining engagement |
| 4 | Silent Users | Lowest engagement across all metrics |

---

## 3. Churn Prediction

### Models Evaluated

| Model | ROC-AUC | Precision | Recall | F1 |
|-------|---------|-----------|--------|----|
| Logistic Regression | Baseline | Baseline | Baseline | Baseline |
| Random Forest | Above baseline | Good | Moderate | Moderate |
| **XGBoost** | **Best** | **Best** | **Best** | **Best** |

### XGBoost Configuration
```python
{
    "n_estimators": 200,
    "max_depth": 6,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "scale_pos_weight": "auto (class ratio)",
    "eval_metric": "auc"
}
```

### Feature Importance (Top 5)
1. `Total_Trans_Ct` — Transaction frequency
2. `Total_Trans_Amt` — Total spend
3. `Total_Revolving_Bal` — Revolving balance
4. `Avg_Utilization_Ratio` — Credit utilization
5. `Months_Inactive_12_mon` — Inactivity months

---

## 4. Inactivity Scoring

### Methodology: Weighted Rule-Based + MinMaxScaler
- **Input Features**: Days since last transaction, transaction frequency, utilization ratio
- **Output**: Activity Score (0.0 = completely inactive, 1.0 = highly active)
- **Thresholds**:
  - Activity Score < 0.3 → Flagged for re-engagement
  - Months Inactive > 3 + Utilization < 15% → Future Churn Watchlist

---

## 5. Campaign Conversion Prediction

### Data Challenge: Severe Class Imbalance
- **Positive class**: ~12% (subscribed)
- **Negative class**: ~88% (did not subscribe)

### Solution: SMOTE + XGBoost
- **SMOTE**: Synthetic Minority Over-sampling Technique applied to training set only
- **Validation**: Stratified K-Fold cross-validation to prevent data leakage

### Key Predictive Features
1. `poutcome` (previous campaign outcome)
2. `euribor3m` (3-month Euribor rate — macroeconomic indicator)
3. `nr_employed` (number of employees — economic context)
4. `pdays` (days since last contact)
5. `campaign` (contact frequency — fatigue indicator)

---

## 6. KYC Risk Scoring

### Composite Risk Model
Ensembles transaction-level flags with entity-level risk indicators:

**Transaction Flags**: `ofac_match_flag`, `fatf_txn_flag`, `structuring_pattern_flag`, `rapid_movement_flag`, `trade_mispricing_flag`

**Entity Flags**: `pep_flag`, `sanctions_flag`, `fatf_entity_flag`, `ofac_country_flag`, `ownership_opacity_score`, `sector_risk`

### Risk Tiers
| Tier | Score Range | Action |
|------|------------|--------|
| Critical | > 0.75 | Immediate freeze + compliance review |
| High | 0.50 – 0.75 | Enhanced Due Diligence |
| Medium | 0.25 – 0.50 | 30-day periodic review |
| Low | < 0.25 | Standard monitoring |

---

## 7. Escalation Prediction

### Training Data
- **Source**: CFPB complaints enriched with LLM-generated features
- **Features**: Complaint category (encoded), emotion label (encoded), narrative word count
- **Target**: Binary escalation flag

### Model: XGBoost Classifier
- Trained on NLP-enriched features
- Outputs calibrated probability for business rule integration

---

## 8. NLP Pipeline (LLM-Powered)

### Provider: Google Gemini (gemini-1.5-flash) / OpenAI (gpt-4o-mini)

| Task | Prompt Strategy | Output |
|------|----------------|--------|
| Summarization | "Summarize in 1-2 sentences" | Concise complaint summary |
| Classification | "Classify into: Billing, Fraud, Account..." | Category label |
| Emotion Detection | "Detect: Frustration, Anger, Distress, Legal Threat..." | Emotion label |
| Response Generation | Context-aware with priority level | Draft customer response |
