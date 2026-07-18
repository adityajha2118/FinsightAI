# Business Requirements Document (BRD)

## 1. Executive Summary

FinSight AI addresses the critical challenge facing modern financial institutions: **fragmented data systems that prevent unified customer intelligence**. The platform consolidates customer lifecycle management, retention analytics, compliance monitoring, and complaint intelligence into a single decision-support system.

---

## 2. Business Problems

### BP-001: Customer Churn
- **Impact**: Acquiring new customers costs 5–25x more than retention
- **Current State**: Reactive — churn detected only after account closure
- **Desired State**: Predictive — flag at-risk customers 90 days in advance
- **Success Metric**: Churn prediction ROC-AUC > 0.85

### BP-002: Silent Attrition
- **Impact**: Dead capital in unused credit lines, zero swipe revenue
- **Current State**: No systematic inactivity monitoring
- **Desired State**: Automated activity scoring with re-engagement triggers
- **Success Metric**: Identify 80% of future churners via inactivity flags

### BP-003: Campaign Inefficiency
- **Impact**: Wasted marketing spend, customer fatigue
- **Current State**: Blanket campaigns with low single-digit conversion
- **Desired State**: ML-targeted campaigns based on predicted conversion
- **Success Metric**: Conversion prediction accuracy sufficient for targeting

### BP-004: Compliance Risk
- **Impact**: Regulatory fines (potentially hundreds of millions), reputational damage
- **Current State**: Manual review of KYC flags
- **Desired State**: Automated risk tiering with real-time alerts
- **Success Metric**: Zero false negatives on Critical risk entities

### BP-005: Complaint Escalation
- **Impact**: Legal fees, CFPB regulatory action, brand damage
- **Current State**: Manual complaint triage, inconsistent prioritization
- **Desired State**: AI-driven classification, emotion detection, and autonomous routing
- **Success Metric**: Autonomous agent processes complaints end-to-end

### BP-006: Lack of Customer Segmentation
- **Impact**: Inefficient resource allocation across customer base
- **Current State**: Treating all customers identically
- **Desired State**: Data-driven personas enabling tailored product offerings
- **Success Metric**: 5 distinct, interpretable customer segments

---

## 3. Stakeholder Matrix

| Stakeholder | Interest | Key Dashboard |
|-------------|----------|---------------|
| Chief Risk Officer | AML/KYC compliance | Compliance Analytics |
| VP Customer Success | Churn prevention | Customer Intelligence |
| CMO | Campaign ROI | Campaign Analytics |
| Head of Support | Complaint resolution | Complaint Intelligence |
| CEO / Board | Portfolio health | Executive Dashboard |

---

## 4. Requirements Traceability

| Requirement ID | Business Problem | Module | Notebook | API Endpoint |
|---------------|-----------------|--------|----------|-------------|
| REQ-001 | BP-001 | Churn Prediction | NB 08 | `/api/customers/churn/*` |
| REQ-002 | BP-002 | Inactivity Detection | NB 07 | `/api/customers/watchlist` |
| REQ-003 | BP-003 | Campaign Prediction | NB 09 | `/api/campaign/predict` |
| REQ-004 | BP-004 | KYC Risk Scoring | NB 10 | `/api/compliance/risk/*` |
| REQ-005 | BP-005 | Complaint Agent | NB 11-12 | `/api/complaints/process` |
| REQ-006 | BP-006 | Customer Segmentation | NB 06 | `/api/customers/segments` |

---

## 5. Non-Functional Requirements

| Category | Requirement |
|----------|------------|
| Performance | API response time < 500ms for cached data |
| Scalability | Support horizontal scaling via stateless API design |
| Security | No hardcoded credentials; all secrets via environment variables |
| Reliability | LLM fallback responses on API failure |
| Maintainability | Domain-driven modular architecture |
| Portability | Docker containerization for any environment |
