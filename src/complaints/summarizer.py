"""
FinSight AI — Classical Extractive Complaint Summarizer.
Uses sentence boundary detection & importance weighting without excessive AI.
"""
import re
import logging

logger = logging.getLogger("finsight.summarizer")

def summarize_complaint(narrative: str) -> str:
    """Extractive summarization using classical sentence splitting & length/position weighting."""
    if not narrative or not isinstance(narrative, str):
        return "Summary unavailable"
        
    # Split sentences cleanly
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', narrative) if len(s.strip()) > 15]
    
    if not sentences:
        return narrative[:180] + ("..." if len(narrative) > 180 else "")
        
    if len(sentences) <= 2:
        return " ".join(sentences)
        
    # Score sentences based on position and key terms
    keywords = {"fee", "charge", "unauthorized", "scam", "fraud", "declined", "error", "delay", "failed", "closed", "limit", "points", "reward"}
    scores = []
    for idx, sent in enumerate(sentences):
        score = 0
        if idx == 0:
            score += 3  # Lead sentence is usually high informative value
        sent_lower = sent.lower()
        words = set(re.findall(r'\w+', sent_lower))
        score += len(words.intersection(keywords)) * 2
        if 30 <= len(sent) <= 180:
            score += 1
        scores.append((score, idx, sent))
        
    # Sort by score descending, then pick top 2 sorted by original order
    top_sentences = sorted(sorted(scores, key=lambda x: x[0], reverse=True)[:2], key=lambda x: x[1])
    return " ".join([s[2] for s in top_sentences])
