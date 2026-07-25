"""
FinSight AI — Classical NLP Complaint Classifier.
Uses robust keyword/lexicon pattern matching without requiring external LLM API calls.
"""
import re
import logging

logger = logging.getLogger("finsight.classifier")

CATEGORIES = [
    "Billing", "Fraud", "Card Declined", "Rewards",
    "Customer Service", "Service Delay", "Credit Reporting", "Collections"
]

CATEGORY_PATTERNS = {
    "Billing": [r"\b(?:fee|fees|interest|rate|charge|charged|payment|billing|balance|overcharge|apr)\b"],
    "Fraud": [r"\b(?:fraud|unauthorized|scam|stolen|identity theft|hacked|fake|suspicious)\b"],
    "Card Declined": [r"\b(?:declined|block|blocked|card declined|limit|transaction failed|freeze)\b"],
    "Rewards": [r"\b(?:reward|points|bonus|cashback|membership rewards|miles|offer|promotion)\b"],
    "Customer Service": [r"\b(?:agent|service|representative|rep|rude|phone|support|call center|attitude)\b"],
    "Service Delay": [r"\b(?:delay|delayed|waiting|weeks|months|timeframe|slow|response time)\b"],
    "Credit Reporting": [r"\b(?:credit report|bureau|score|reporting|equifax|experian|transunion|inquiry)\b"],
    "Collections": [r"\b(?:collection|collector|debt|harassment|late fee|past due|default)\b"],
}

def classify_complaint(narrative: str) -> str:
    """Classify complaint using classical NLP keyword & pattern scoring. Fallback: 'Customer Service'."""
    if not narrative or not isinstance(narrative, str):
        return "Customer Service"
    
    text_lower = narrative.lower()
    scores = {cat: 0 for cat in CATEGORIES}
    
    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            scores[category] += len(matches)
            
    best_cat = max(scores, key=scores.get)
    if scores[best_cat] > 0:
        return best_cat
        
    return "Customer Service"
