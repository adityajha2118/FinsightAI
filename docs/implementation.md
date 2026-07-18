# Implementation Journal

## Overview

This document captures the key design decisions, trade-offs, and lessons learned during the development of FinSight AI.

---

## Design Decisions

### 1. CSV over Database for Initial Implementation

**Decision**: Use CSV/Parquet files instead of a live database for data storage.

**Rationale**: The primary goal is demonstrating ML/AI capabilities, not database administration. CSV files allow:
- Zero infrastructure setup for reviewers
- Full data visibility (files are human-readable)
- Portable — the entire project runs on any machine

**Trade-off**: No concurrent write support, no ACID transactions. The `database_schema.md` in `architecture/` documents the production migration path.

### 2. Monolithic FastAPI over Microservices

**Decision**: Single FastAPI application serving all domains.

**Rationale**: For a portfolio project, the overhead of managing multiple services, service discovery, and inter-service communication adds complexity without proportional value. The code is organized by domain module, making future microservice extraction straightforward.

### 3. LangGraph over Raw LangChain Chains

**Decision**: Use LangGraph's StateGraph instead of sequential LangChain chains for the complaint agent.

**Rationale**: LangGraph provides:
- Explicit state management (TypedDict)
- Visual graph representation
- Built-in support for conditional routing
- Foundation for future multi-agent expansion

### 4. XGBoost as Primary Classifier

**Decision**: XGBoost for churn, campaign, KYC, and escalation prediction.

**Rationale**: Consistently outperformed Logistic Regression and Random Forest on ROC-AUC across all datasets. Handles tabular data with missing values natively.

### 5. SMOTE for Campaign Dataset

**Decision**: Apply Synthetic Minority Over-sampling to the campaign dataset.

**Rationale**: The marketing campaign dataset has severe class imbalance (~88% negative, ~12% positive). Without SMOTE, the model achieves high accuracy by predicting the majority class but fails on recall for the minority class.

---

## Lessons Learned

1. **Feature Store Pays Off**: Pre-computing Parquet features reduced API response times from ~2s to ~200ms for customer profile lookups.

2. **LLM Fallbacks Are Essential**: During development, LLM API rate limits caused frequent failures. Adding hardcoded fallback responses in the complaint agent ensures the system never returns an empty response.

3. **Notebook ≠ Production Code**: The biggest refactoring effort was extracting ML inference logic from notebooks into `src/` modules. Notebooks should prototype; production code lives in packages.

4. **Unified Customer Profile**: The most impactful feature was joining segmentation, churn, inactivity, and KYC data into a single customer view. This enabled the Executive Dashboard's cross-module analytics.
