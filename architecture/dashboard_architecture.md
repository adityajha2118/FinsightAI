# Dashboard Architecture

## Overview

The FinSight AI frontend is a multi-page Streamlit application serving as the primary user interface for enterprise analytics. It follows a modular page-based architecture where each analytics domain has its own dedicated view.

---

## Component Hierarchy

```mermaid
graph TD
    APP[dashboard.py<br/>Main Entry Point] --> SB[Sidebar Navigation]
    APP --> HERO[Hero Section + KPIs]
    APP --> GRID[Module Cards Grid]

    SB --> P1[1_customer_intelligence.py]
    SB --> P2[2_campaign_analytics.py]
    SB --> P3[3_compliance_analytics.py]
    SB --> P4[4_complaint_intelligence.py]
    SB --> P5[5_executive_dashboard.py]

    P1 --> C_SEG[Segment Distribution]
    P1 --> C_CHR[Churn Analysis]
    P1 --> C_WL[Watchlist Table]
    P1 --> C_FI[Feature Importance]

    P2 --> CA_STATS[Campaign Stats]
    P2 --> CA_PRED[Conversion Predictor Form]

    P3 --> CO_RISK[Risk Distribution]
    P3 --> CO_HIGH[High Risk Table]
    P3 --> CO_PRED[KYC Predictor Form]

    P4 --> CP_NLP[NLP Analysis Viz]
    P4 --> CP_AGT[Live AI Agent Interface]

    P5 --> EX_KPI[Executive KPIs]
    P5 --> EX_HEAT[Risk Heatmap]
    P5 --> EX_CROSS[Cross-Module Insights]

    style APP fill:#635BFF,color:#fff
    style P1 fill:#3498DB,color:#fff
    style P2 fill:#E67E22,color:#fff
    style P3 fill:#E74C3C,color:#fff
    style P4 fill:#9B59B6,color:#fff
    style P5 fill:#2ECC71,color:#fff
```

---

## Page Specifications

### Home Dashboard (`dashboard.py`)
- **Purpose**: Landing page with platform overview and navigation
- **Data Sources**: `/api/customers/kpis`
- **Components**: Hero section, Live KPI strip, Module cards grid, Tech stack, Dataset summary

### Page 1: Customer Intelligence
- **Purpose**: Deep dive into customer behavior, segmentation, and churn risk
- **Data Sources**: `/api/customers/segments`, `/api/customers/churn/*`, `/api/customers/watchlist`
- **Key Visualizations**:
  - K-Means segment distribution (Plotly pie/bar)
  - Churn probability histogram
  - Segment profile comparison table
  - XGBoost feature importance bar chart
  - Future churn watchlist with risk badges

### Page 2: Campaign Analytics
- **Purpose**: Marketing campaign performance and conversion prediction
- **Data Sources**: `/api/campaign/stats`, `/api/campaign/predict`
- **Key Visualizations**:
  - Campaign success rate metrics
  - Channel effectiveness comparison
  - Interactive conversion predictor form

### Page 3: Compliance Analytics
- **Purpose**: KYC/AML risk monitoring and entity risk assessment
- **Data Sources**: `/api/compliance/risk/*`
- **Key Visualizations**:
  - Risk tier distribution (pie chart)
  - High-risk entity table with PEP/sanctions flags
  - Interactive KYC risk predictor form

### Page 4: Complaint Intelligence
- **Purpose**: NLP analysis results and live AI agent interface
- **Data Sources**: `/api/complaints/process`
- **Key Visualizations**:
  - Emotion × Category heatmap
  - Escalation probability distribution
  - Live AI Agent: text input → real-time LangGraph processing → structured output

### Page 5: Executive Dashboard
- **Purpose**: C-suite overview with cross-module risk intelligence
- **Data Sources**: All API endpoints aggregated
- **Key Visualizations**:
  - Platform-wide KPI cards
  - Segment × Churn Risk heatmap
  - Cross-module risk correlation

---

## Data Refresh Pattern

```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant FastAPI
    participant DataLayer

    User->>Streamlit: Navigate to page
    Streamlit->>FastAPI: GET /api/{domain}/data
    FastAPI->>DataLayer: Load CSV/Parquet
    DataLayer-->>FastAPI: DataFrame
    FastAPI-->>Streamlit: JSON response
    Streamlit-->>User: Render Plotly charts

    Note over Streamlit: @st.cache_data(ttl=300)<br/>caches API responses for 5 min
```

---

## Styling Architecture

All pages inject shared CSS via `frontend/utils/styles.py`:

| Component | Style Feature |
|-----------|--------------|
| KPI Cards | Gradient backgrounds, animated borders |
| Risk Badges | Color-coded (Critical=red, High=orange, Standard=green) |
| Section Headers | Gradient text with subtle separators |
| Module Cards | Hover effects, glassmorphism borders |
| Tables | Alternating row colors, sticky headers |
