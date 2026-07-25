"""
FinSight AI — Classical Emotion & Sentiment Detector.
Uses VADER sentiment analysis and classical NLP rules without excessive AI.
"""
import re
import logging
from nltk.sentiment.vader import SentimentIntensityAnalyzer

logger = logging.getLogger("finsight.emotion")

_sia = None

def _get_sia():
    global _sia
    if _sia is None:
        try:
            _sia = SentimentIntensityAnalyzer()
        except Exception:
            import nltk
            try:
                nltk.download("vader_lexicon", quiet=True)
                _sia = SentimentIntensityAnalyzer()
            except Exception:
                pass
    return _sia

def detect_emotion(narrative: str) -> str:
    """Detect emotion using VADER compound score & classical NLP rules: Anger, Frustration, Neutral, Legal Threat, Distress."""
    if not narrative or not isinstance(narrative, str):
        return "Neutral"
        
    text_lower = narrative.lower()
    
    # 1. Check for Legal Threat
    if any(w in text_lower for w in ["attorney", "lawyer", "sue", "legal", "cfpb", "court", "violation", "litigation", "lawsuit"]):
        return "Legal Threat"
        
    # 2. Check for Distress
    if any(w in text_lower for w in ["devastated", "ruined", "desperate", "crying", "help me", "hopeless", "severe financial distress", "homeless"]):
        return "Distress"
        
    # 3. VADER Polarity Scoring
    sia = _get_sia()
    if sia:
        scores = sia.polarity_scores(narrative)
        compound = scores.get("compound", 0.0)
        if compound <= -0.55:
            return "Anger"
        elif compound <= -0.15:
            return "Frustration"
        else:
            return "Neutral"
            
    # Fallback if sia unavailable
    if any(w in text_lower for w in ["scam", "furious", "unacceptable", "terrible", "worst", "disgusting"]):
        return "Anger"
    elif any(w in text_lower for w in ["annoyed", "frustrated", "delay", "issue", "problem"]):
        return "Frustration"
        
    return "Neutral"
