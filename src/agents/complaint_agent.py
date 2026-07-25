from typing import TypedDict
import logging

from src.complaints.summarizer import summarize_complaint
from src.complaints.classifier import classify_complaint
from src.complaints.emotion_detector import detect_emotion
from src.complaints.escalation_model import predict_escalation, encode_for_escalation

logger = logging.getLogger("finsight.agent")

class ComplaintState(TypedDict):
    narrative: str
    summary: str
    category: str
    emotion: str
    escalation_probability: float
    priority_level: str
    assigned_team: str
    recommended_action: str
    suggested_response: str

def route_priority(prob: float, emo: str) -> dict:
    if prob > 0.90:
        return {"priority_level": "CRITICAL", "assigned_team": "Supervisor", "recommended_action": "Notify supervisor immediately"}
    if prob > 0.80:
        return {"priority_level": "HIGH", "assigned_team": "Priority Support", "recommended_action": "Escalate to senior agent"}
    if emo in ["Legal Threat", "Distress"]:
        return {"priority_level": "CRITICAL", "assigned_team": "Legal Compliance", "recommended_action": "Escalate to compliance"}
    if emo == "Anger" and prob > 0.60:
        return {"priority_level": "HIGH", "assigned_team": "Priority Support", "recommended_action": "Immediate callback required"}
    
    return {"priority_level": "STANDARD", "assigned_team": "General Support", "recommended_action": "Standard resolution process"}

def generate_classical_response(category: str, emotion: str, priority_level: str) -> str:
    """Generate structured, empathetic response template using classical business rules without excessive AI."""
    if priority_level == "CRITICAL" or emotion in ["Legal Threat", "Anger"]:
        return (f"We take your {category} concern very seriously and apologize for your frustration. "
                f"A senior specialist from our {category} escalation team has been assigned to investigate your account immediately and will contact you directly within 24 hours.")
    elif priority_level == "HIGH":
        return (f"Thank you for reaching out regarding your {category} issue. We sincerely apologize for any inconvenience caused. "
                f"Our priority resolution team is actively reviewing your transaction details and will provide an update shortly.")
    else:
        return (f"We appreciate you contacting American Express regarding your {category} inquiry. "
                f"We have documented your request and our customer service team will review your account and process the resolution within standard timeframes.")

def run_complaint_agent(narrative: str) -> dict:
    """Run classical ML/NLP complaint processing pipeline without requiring external LLM API calls."""
    summary = summarize_complaint(narrative)
    category = classify_complaint(narrative)
    emotion = detect_emotion(narrative)
    
    length = len(narrative) if narrative else 0
    encoded = encode_for_escalation(category, emotion, length)
    res = predict_escalation(encoded)
    escalation_prob = res.get("escalation_probability", 0.0)
    
    routing = route_priority(escalation_prob, emotion)
    response = generate_classical_response(category, emotion, routing["priority_level"])
    
    return {
        "narrative": narrative,
        "summary": summary,
        "category": category,
        "emotion": emotion,
        "escalation_probability": escalation_prob,
        "priority_level": routing["priority_level"],
        "assigned_team": routing["assigned_team"],
        "recommended_action": routing["recommended_action"],
        "suggested_response": response
    }
