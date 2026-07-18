# Executive Dashboard Specification

## Purpose
C-suite overview of portfolio health across all analytics modules.

## KPIs
| Metric | Source | Format |
|--------|--------|--------|
| Total Customers | Unified Profile | Count |
| Churn Rate | Churn Predictions | Percentage |
| Active Rate | Inactivity Scores | Percentage |
| High Risk Clients | KYC Scores | Count |
| Avg Credit Limit | Customer Data | Currency |

## Visualizations
1. Cross-module KPI cards (gradient animated)
2. Segment × Churn Risk heatmap (Plotly)
3. Future churn breakdown by segment (bar chart)
4. Portfolio health trend (line chart)

## Data Refresh
- Cache TTL: 5 minutes
- Source: All `/api/customers/*` endpoints aggregated
