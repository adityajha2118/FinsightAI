"""Complaint Agent — Available Tools.

These tools are callable by the LangGraph agent nodes during complaint processing.
"""

from src.complaints.summarizer import summarize_complaint
from src.complaints.classifier import classify_complaint
from src.complaints.emotion_detector import detect_emotion
from src.complaints.escalation_model import predict_escalation, encode_for_escalation


TOOLS = {
    "summarize": summarize_complaint,
    "classify": classify_complaint,
    "detect_emotion": detect_emotion,
    "predict_escalation": predict_escalation,
    "encode_for_escalation": encode_for_escalation,
}
