"""FinSight AI — Complaint Prompt Templates."""

SUMMARIZE_PROMPT = """Summarize the following customer complaint in 1-2 concise sentences.
Focus on the core issue and any urgency indicators.

Complaint:
{narrative}

Summary:"""

CLASSIFY_PROMPT = """Classify the following customer complaint into exactly ONE of these categories:
- Billing
- Fraud
- Account Management
- Credit Reporting
- Debt Collection
- Mortgage
- Other

Complaint:
{narrative}

Category:"""

EMOTION_PROMPT = """Detect the primary emotional state of the customer in this complaint.
Choose exactly ONE:
- Frustration
- Anger
- Distress
- Legal Threat
- Neutral

Complaint:
{narrative}

Emotion:"""

RESPONSE_PROMPT = """Write a professional, empathetic 2-3 sentence response to a bank customer
whose complaint is about {category},
emotional state is {emotion},
and priority level is {priority_level}.
Be concise, solution-focused, and avoid making specific promises about timelines.

Response:"""
