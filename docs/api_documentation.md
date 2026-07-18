# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently open (no authentication). Production deployment should add OAuth2/JWT.

---

## Health Check

### `GET /api/health`
Returns API status and version.

**Response:**
```json
{"status": "ok", "version": "1.0.0"}
```

---

## Customer Intelligence

### `GET /api/customers/kpis`
Executive KPI summary across all customers.

**Response:**
```json
{
  "total_customers": 10127,
  "churn_rate": 16.1,
  "high_risk_count": 245,
  "active_rate": 83.9,
  "avg_credit_limit": 8631.95
}
```

### `GET /api/customers/segments`
Segment distribution counts.

### `GET /api/customers/segment-profiles`
Mean feature values per segment for comparison tables.

### `GET /api/customers/churn/top?n=50`
Top N customers by churn probability.

### `GET /api/customers/churn/distribution`
Churn probability distribution histogram data.

### `GET /api/customers/watchlist?n=100`
Future churn watchlist — high-inactivity customers.

### `GET /api/customers/activity`
Activity score distribution data.

### `GET /api/customers/profile/{client_id}`
Unified 360° profile for a specific customer.

**Path Parameters:** `client_id` (string)

---

## Campaign Analytics

### `GET /api/campaign/stats`
Full campaign statistics including success rates and channel breakdowns.

### `POST /api/campaign/predict`
Predict campaign conversion probability.

**Request Body:**
```json
{
  "age": 35.0,
  "job": 1,
  "marital": 0,
  "education": 2,
  "default": 0,
  "housing": 1,
  "loan": 0,
  "contact": 1,
  "month": 5,
  "campaign": 2.0,
  "pdays": 999.0,
  "previous": 0.0,
  "poutcome": 0,
  "emp_var_rate": 1.1,
  "cons_price_idx": 93.994,
  "cons_conf_idx": -36.4,
  "euribor3m": 4.857,
  "nr_employed": 5191.0,
  "contacted_before": 0,
  "campaign_intensity": 1.0
}
```

---

## Compliance

### `GET /api/compliance/risk/distribution`
KYC risk tier distribution.

### `GET /api/compliance/risk/high?n=50`
Top N high-risk entities.

### `POST /api/compliance/risk/predict`
Predict KYC risk tier for given features.

**Request Body:**
```json
{
  "ofac_match_flag": 0,
  "fatf_txn_flag": 1,
  "structuring_pattern_flag": 0,
  "rapid_movement_flag": 1,
  "pep_flag": 0,
  "sanctions_flag": 0,
  "ownership_opacity_score": 0.65,
  "sector_risk": "High"
}
```

---

## Complaint Intelligence

### `POST /api/complaints/process`
Process a complaint through the full LangGraph AI agent pipeline.

**Request Body:**
```json
{
  "narrative": "I have been trying to dispute a charge on my credit card for three months. Nobody responds to my calls. I am considering legal action."
}
```

**Response:**
```json
{
  "narrative": "I have been trying to dispute...",
  "summary": "Customer unable to dispute charge for 3 months, considering legal action.",
  "category": "Billing",
  "emotion": "Legal Threat",
  "escalation_probability": 0.87,
  "priority_level": "CRITICAL",
  "assigned_team": "Legal Compliance",
  "recommended_action": "Escalate to compliance immediately",
  "suggested_response": "We sincerely apologize for the delay..."
}
```

**Validation:** Narrative must be at least 20 characters.
