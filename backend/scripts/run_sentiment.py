"""
FinSight AI — VADER Sentiment Analysis Pipeline.

Business Context:
    Understanding complaint sentiment helps CX teams prioritize
    tickets and identify systemic product issues driving negativity.
    VADER is used because it's fast, deterministic, and works well
    for short-to-medium consumer complaint text without needing
    GPU infrastructure or API keys.

Pipeline:
    complaints table → VADER scoring → complaint_sentiment table
"""

import logging
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database.engine import get_engine

logger = logging.getLogger(__name__)


def _get_vader():
    """Initialize VADER SentimentIntensityAnalyzer with NLTK data download."""
    import nltk
    nltk.download("vader_lexicon", quiet=True)
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    return SentimentIntensityAnalyzer()


def classify_sentiment(compound: float) -> str:
    """Map VADER compound score to a label.

    Thresholds follow VADER documentation:
        compound >= 0.05  → Positive
        compound <= -0.05 → Negative
        else              → Neutral
    """
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    return "Neutral"


def run_sentiment_pipeline(batch_size: int = 5000):
    """Score all complaints with VADER and store in complaint_sentiment table.

    Reads narratives from the complaints table, computes VADER scores,
    and writes results to complaint_sentiment. Only scores complaints
    that have a non-empty narrative.

    Args:
        batch_size: Number of rows to process at a time for memory efficiency.
    """
    engine = get_engine()
    sia = _get_vader()

    logger.info("=" * 60)
    logger.info("VADER Sentiment Analysis Pipeline")
    logger.info("=" * 60)

    # Read complaints with narratives
    query = """
        SELECT complaint_id, narrative
        FROM complaints
        WHERE narrative IS NOT NULL AND narrative != ''
    """
    df = pd.read_sql(query, engine)
    logger.info("Complaints with narratives: %d", len(df))

    if df.empty:
        logger.warning("No complaints with narratives found. Skipping.")
        return

    # Score in batches
    results = []
    total = len(df)
    for i in range(0, total, batch_size):
        batch = df.iloc[i:i + batch_size]
        for _, row in batch.iterrows():
            scores = sia.polarity_scores(str(row["narrative"]))
            results.append({
                "complaint_id": row["complaint_id"],
                "compound_score": round(scores["compound"], 4),
                "positive_score": round(scores["pos"], 4),
                "neutral_score": round(scores["neu"], 4),
                "negative_score": round(scores["neg"], 4),
                "sentiment_label": classify_sentiment(scores["compound"]),
            })
        logger.info("  Processed %d / %d complaints", min(i + batch_size, total), total)

    # Write to PostgreSQL
    result_df = pd.DataFrame(results)
    logger.info("Writing %d sentiment scores to complaint_sentiment...", len(result_df))
    result_df.to_sql("complaint_sentiment", engine, if_exists="append", index=False, method="multi", chunksize=5000)
    logger.info("✓ Sentiment pipeline complete")

    # Log distribution
    dist = result_df["sentiment_label"].value_counts()
    for label, count in dist.items():
        logger.info("  %s: %d (%.1f%%)", label, count, 100 * count / len(result_df))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    run_sentiment_pipeline()
