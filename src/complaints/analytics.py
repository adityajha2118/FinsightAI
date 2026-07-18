from pathlib import Path
import pandas as pd

COMPLAINTS_PATH = Path("data/processed/complaints_with_escalation.csv")

def get_complaint_stats() -> dict:
    """Return aggregated complaint statistics for the dashboard."""
    if not COMPLAINTS_PATH.exists():
        return {
            "total_complaints": 0,
            "high_escalation_count": 0,
            "critical_count": 0,
            "category_distribution": {},
            "emotion_distribution": {},
            "top_escalations": []
        }
    
    df = pd.read_csv(COMPLAINTS_PATH)
    total_complaints = len(df)
    
    # Use fallback if column is missing
    escalation_col = 'escalation_probability' if 'escalation_probability' in df.columns else 'escalation_score' if 'escalation_score' in df.columns else None
    
    high_escalation_count = 0
    critical_count = 0
    top_escalations = []
    
    if escalation_col:
        high_escalation_count = int((df[escalation_col] > 0.8).sum())
        
        # Sort for top escalations
        top_df = df.sort_values(escalation_col, ascending=False).head(10)
        
        for _, row in top_df.iterrows():
            prob = row[escalation_col]
            if prob > 0.9:
                priority = "Critical"
                team = "Legal & Compliance" if row.get('emotion') == "Legal Threat" else "Escalation Team"
            elif prob > 0.8:
                priority = "High"
                team = "Priority Support"
            else:
                priority = "Standard"
                team = "General Support"
                
            if priority == "Critical":
                critical_count += 1
                
            top_escalations.append({
                "complaint_id": row.get('complaint_id', 'Unknown'),
                "category": row.get('category', 'Unknown'),
                "emotion": row.get('emotion', 'Neutral'),
                "escalation_probability": round(prob, 4),
                "priority": priority,
                "team": team
            })
            
    # Category Distribution
    category_distribution = {}
    if 'category' in df.columns:
        category_distribution = df['category'].value_counts().to_dict()
        
    # Emotion Distribution
    emotion_distribution = {}
    if 'emotion' in df.columns:
        emotion_distribution = df['emotion'].value_counts().to_dict()
        
    return {
        "total_complaints": total_complaints,
        "high_escalation_count": high_escalation_count,
        "critical_count": critical_count,
        "category_distribution": category_distribution,
        "emotion_distribution": emotion_distribution,
        "top_escalations": top_escalations
    }
