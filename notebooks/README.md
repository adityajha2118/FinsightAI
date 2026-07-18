# Notebooks

Jupyter notebooks organized by analytical phase. Each phase builds on the outputs of the previous one.

## Execution Order

| Phase | Directory | Notebooks | Purpose |
|-------|-----------|-----------|---------|
| 1 | `01_data_understanding/` | NB 01–05 | EDA, cleaning, and initial profiling |
| 2 | `02_feature_engineering/` | NB 13 | Unified customer profile construction |
| 3 | `03_customer_intelligence/` | NB 06–08 | Segmentation, inactivity, churn models |
| 4 | `04_campaign_analytics/` | NB 09 | Campaign conversion prediction |
| 5 | `05_compliance_intelligence/` | NB 10 | KYC/AML risk scoring |
| 6 | `06_complaint_intelligence/` | NB 11–12 | NLP sentiment + escalation prediction |
| 7 | `07_genai/` | — | GenAI experimentation (future) |
| 8 | `08_agents/` | — | Agent development (future) |
| 9 | `09_dashboard_validation/` | — | Dashboard data validation (future) |

## Working Directory

All notebooks assume the **repository root** (`FinSight-AI/`) as the working directory. Data paths use relative references like `../../data/raw/` or `data/processed/` depending on notebook location.

## Output Artifacts

Notebooks produce two types of output:
1. **Processed data** → `data/processed/`
2. **Trained models** → `models/{domain}/`
