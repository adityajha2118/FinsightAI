# Customer Agent

## Purpose
Retrieves unified customer profiles, segments, and risk scores for customer intelligence queries.

## Capabilities
- Look up customer by CLIENTNUM
- Retrieve segment assignment and behavioral scores
- Access churn probability and inactivity flags
- Cross-reference KYC risk tier

## Implementation
- Profile Builder: `src/customer_intelligence/profile_builder.py`
- Segmentation: `src/customer_intelligence/segmentation.py`
- API Endpoints: `GET /api/customers/*`

## Status
Placeholder for future LangGraph agent implementation.
