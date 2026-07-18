# Model Documentation

## Overview

Model cards for all trained ML models in FinSight AI following the Google Model Cards framework.

---

## Model Registry

| Model | Type | Artifact Path | Task |
|-------|------|--------------|------|
| Churn (XGBoost) | Classification | `models/churn/xgboost_model.pkl` | Predict account closure |
| Churn (RF) | Classification | `models/churn/random_forest.pkl` | Benchmark classifier |
| Churn (LR) | Classification | `models/churn/logistic_regression.pkl` | Baseline classifier |
| Segmentation | Clustering | `models/segmentation/kmeans_model.pkl` | Customer personas (k=5) |
| Scaler | Preprocessing | `models/segmentation/scaler.pkl` | StandardScaler for segmentation |
| Inactivity | Scoring | `models/inactivity/activity_scorer.pkl` | Activity score (0-1) |
| Campaign | Classification | `models/campaign/xgboost_campaign.pkl` | Conversion prediction (SMOTE) |
| KYC (XGBoost) | Classification | `models/kyc/xgboost_kyc.pkl` | Risk tier assignment |
| KYC (RF) | Classification | `models/kyc/random_forest_kyc.pkl` | Ensemble member |
| Escalation | Classification | `models/escalation/xgboost_escalation.pkl` | Complaint escalation probability |

---

## Churn Predictor

- **Algorithm**: XGBoost (n_estimators=200, max_depth=6, lr=0.1)
- **Target**: `Attrition_Flag` (binary)
- **Top Features**: Total_Trans_Ct, Total_Trans_Amt, Total_Revolving_Bal
- **Use**: Retention teams trigger offers when probability > 0.70
- **Limitation**: Static snapshot, no time-series dynamics

## Customer Segmentation

- **Algorithm**: K-Means (k=5)
- **Features**: Credit_Limit, Total_Trans_Amt, Total_Trans_Ct, Avg_Utilization_Ratio, Total_Revolving_Bal, Months_Inactive_12_mon
- **Segments**: Premium, Daily Spenders, Deal Hunters, At-Risk, Silent Users
- **Limitation**: Assumes spherical clusters; requires saved scaler

## Inactivity Scorer

- **Algorithm**: Rule-based weighted composite + MinMaxScaler
- **Output**: Activity Score (0.0–1.0)
- **Threshold**: Score < 0.3 flagged for re-engagement
- **Limitation**: Manually tuned weights, no seasonal adjustment

## Campaign Conversion

- **Algorithm**: XGBoost + SMOTE oversampling
- **Dataset**: 100 records (small — SMOTE-expanded)
- **Key Predictors**: poutcome, euribor3m, nr_employed, pdays
- **Limitation**: Small dataset; macroeconomic features are period-specific

## KYC Risk Scorer

- **Algorithm**: XGBoost + Random Forest ensemble
- **Risk Tiers**: Critical (>0.75), High (0.50-0.75), Medium (0.25-0.50), Low (<0.25)
- **Features**: 12 transaction + entity risk flags
- **Limitation**: Synthetic KYC data; not validated against real regulatory outcomes

## Escalation Predictor

- **Algorithm**: XGBoost on LLM-enriched features
- **Features**: Encoded category, emotion, word_count
- **Use**: LangGraph agent routing node for priority assignment
- **Limitation**: Dependent on LLM classification accuracy
