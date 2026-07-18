# Project Plan

## Overview

FinSight AI was developed in 7 sprints following an Agile methodology. Each sprint delivered a functional increment of the platform.

---

## Sprint Timeline

```mermaid
gantt
    title FinSight AI Development Timeline
    dateFormat  YYYY-MM-DD
    axisFormat  %b %d

    section Data Foundation
    Data Collection & Ingestion       :done, s1a, 2025-01-06, 3d
    EDA Notebooks (01-05)             :done, s1b, after s1a, 5d
    Data Cleaning Pipeline            :done, s1c, after s1b, 3d

    section ML Development
    Customer Segmentation (NB 06)     :done, s2a, after s1c, 3d
    Inactivity Detection (NB 07)      :done, s2b, after s2a, 2d
    Churn Prediction (NB 08)          :done, s2c, after s2b, 3d
    Campaign Prediction (NB 09)       :done, s3a, after s2c, 2d
    KYC Risk Scoring (NB 10)          :done, s3b, after s3a, 3d

    section NLP & GenAI
    Complaint Sentiment (NB 11)       :done, s4a, after s3b, 3d
    Escalation Prediction (NB 12)     :done, s4b, after s4a, 2d
    Unified Customer Profile (NB 13)  :done, s4c, after s4b, 2d

    section Backend
    FastAPI Architecture              :done, s5a, after s4c, 3d
    API Endpoints                     :done, s5b, after s5a, 3d
    LangGraph Agent                   :done, s5c, after s5b, 4d

    section Frontend
    Streamlit Dashboard               :done, s6a, after s5c, 5d
    Dashboard Polish & UX             :done, s6b, after s6a, 3d

    section Documentation
    Repository Architecture           :done, s7a, after s6b, 3d
    Documentation & README            :done, s7b, after s7a, 2d
```

---

## Sprint Deliverables

### Sprint 1: Data Foundation
- **Goal**: Ingest and clean all 7 datasets
- **Deliverables**: 5 EDA notebooks, 5 cleaned CSV files
- **Key Metrics**: 1.4M+ records processed

### Sprint 2: Customer ML
- **Goal**: Build customer intelligence models
- **Deliverables**: K-Means segmentation, inactivity scoring, churn prediction
- **Key Metrics**: XGBoost churn ROC-AUC achieved

### Sprint 3: Domain ML
- **Goal**: Campaign and compliance models
- **Deliverables**: Campaign conversion predictor (SMOTE), KYC risk scorer
- **Key Metrics**: Multi-model ensemble for KYC risk

### Sprint 4: NLP & Profile Unification
- **Goal**: Process complaints with LLMs, build unified profile
- **Deliverables**: Sentiment analysis, escalation prediction, 360° customer view
- **Key Metrics**: 24,665 complaints processed through NLP pipeline

### Sprint 5: Backend
- **Goal**: Production API layer
- **Deliverables**: FastAPI with 15+ endpoints, LangGraph complaint agent
- **Key Metrics**: Sub-second response times on cached data

### Sprint 6: Frontend
- **Goal**: Interactive analytics dashboard
- **Deliverables**: 5-page Streamlit application with Plotly visualizations
- **Key Metrics**: All 6 analytics domains visualized

### Sprint 7: Documentation
- **Goal**: Enterprise-grade repository structure
- **Deliverables**: Full documentation suite, architecture diagrams, deployment configs
