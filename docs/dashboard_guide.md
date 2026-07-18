# Dashboard User Guide

## Accessing the Dashboard

```bash
cd frontend
streamlit run dashboard.py
# Opens at http://localhost:8501
```

> **Prerequisite**: The FastAPI backend must be running on port 8000.

---

## Home Page

The landing page provides:
- **Live KPI Strip**: Total customers, churn rate, high-risk clients, active rate, avg credit limit
- **Module Cards**: Quick navigation to all 5 analytics domains
- **Tech Stack**: Visual display of technologies used
- **Dataset Summary**: Table of all 7 datasets powering the platform

---

## Page 1: Customer Intelligence

### Segment Distribution
Interactive pie/bar chart showing the 5 K-Means customer segments and their relative sizes.

### Churn Analysis
- Churn probability distribution histogram
- Top customers ranked by churn risk
- XGBoost feature importance chart showing which factors drive churn

### Future Churn Watchlist
Sortable table of customers flagged by the inactivity model, with risk badges (Critical, High, Standard).

---

## Page 2: Campaign Analytics

### Campaign Performance
Overview metrics: success rate, total contacts, conversion breakdown by channel.

### Conversion Predictor
Interactive form where you input customer demographic and campaign features. The XGBoost model returns a real-time conversion probability.

---

## Page 3: Compliance Analytics

### Risk Distribution
Pie chart of KYC risk tiers (Critical, High, Medium, Low) across all entities.

### High-Risk Entities
Table of flagged entities with PEP/sanctions indicators and risk scores.

### KYC Predictor
Interactive form to input risk flags and get an immediate risk tier assessment.

---

## Page 4: Complaint Intelligence

### NLP Analysis
Visualizations of LLM-generated analysis: emotion distribution, category breakdown, escalation probabilities.

### Live AI Agent
Text input where you paste a raw customer complaint. The LangGraph agent processes it in real-time through 6 nodes:
1. Summarize → 2. Classify → 3. Detect Emotion → 4. Score Escalation → 5. Route → 6. Generate Response

The output shows the complete agent state: summary, category, emotion, escalation probability, priority level, assigned team, and drafted response.

---

## Page 5: Executive Dashboard

### Platform KPIs
High-level metrics aggregated across all modules.

### Cross-Module Risk Intelligence
- Segment × Churn Risk heatmap
- Future churn breakdown by segment
- Portfolio health indicators

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API Offline" warning | Start the backend: `python main.py` |
| Empty charts | Ensure notebooks have been executed and processed data exists |
| Agent returns fallback response | Check LLM API key in `.env` |
