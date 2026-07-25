"""
FinSight AI — Experimentation Analytics Service Layer.

Business Context:
    Business decisions must be backed by statistical evidence.
    This module performs rigorous A/B test analysis including
    T-Test, Chi-Square, confidence intervals, and effect size
    so stakeholders can make informed go/no-go decisions.
"""

import logging
import math
from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats
from sqlalchemy import text

from src.database.engine import get_engine

logger = logging.getLogger(__name__)


def get_experiment_summary(experiment_name: Optional[str] = None) -> dict:
    """Complete A/B test analysis with statistical rigor.

    Returns:
        - Group-level metrics (conversion rate, avg revenue, etc.)
        - Chi-Square test for conversion proportions
        - T-Test for continuous metrics (revenue, time_spent)
        - Confidence intervals
        - Effect size (Cohen's h for proportions, Cohen's d for means)
        - Statistical recommendation
    """
    engine = get_engine()

    # Fetch data
    if experiment_name:
        query = text("SELECT * FROM ab_tests WHERE experiment_name = :name")
        df = pd.read_sql(query, engine, params={"name": experiment_name})
    else:
        df = pd.read_sql("SELECT * FROM ab_tests", engine)

    if df.empty:
        return {"error": "No experiment data found"}

    control = df[df["experiment_group"] == "control"]
    treatment = df[df["experiment_group"] == "treatment"]

    # ── Group Metrics ─────────────────────────────────────────
    control_conversions = control["converted"].sum()
    treatment_conversions = treatment["converted"].sum()
    control_rate = control["converted"].mean()
    treatment_rate = treatment["converted"].mean()

    lift = ((treatment_rate - control_rate) / control_rate * 100) if control_rate > 0 else 0

    group_metrics = {
        "control": {
            "sample_size": len(control),
            "conversions": int(control_conversions),
            "conversion_rate": round(float(control_rate), 4),
            "avg_revenue": round(float(control["revenue"].mean()), 2),
            "avg_sessions": round(float(control["sessions"].mean()), 2),
            "avg_pages_viewed": round(float(control["pages_viewed"].mean()), 2),
            "avg_time_spent": round(float(control["time_spent"].mean()), 2),
        },
        "treatment": {
            "sample_size": len(treatment),
            "conversions": int(treatment_conversions),
            "conversion_rate": round(float(treatment_rate), 4),
            "avg_revenue": round(float(treatment["revenue"].mean()), 2),
            "avg_sessions": round(float(treatment["sessions"].mean()), 2),
            "avg_pages_viewed": round(float(treatment["pages_viewed"].mean()), 2),
            "avg_time_spent": round(float(treatment["time_spent"].mean()), 2),
        },
    }

    # ── Chi-Square Test (Conversion Proportions) ──────────────
    contingency_table = np.array([
        [control_conversions, len(control) - control_conversions],
        [treatment_conversions, len(treatment) - treatment_conversions],
    ])
    chi2, chi2_p, chi2_dof, _ = stats.chi2_contingency(contingency_table)

    # ── T-Test (Revenue) ──────────────────────────────────────
    t_stat, t_p = stats.ttest_ind(
        treatment["revenue"].dropna(),
        control["revenue"].dropna(),
        equal_var=False,  # Welch's t-test
    )

    # ── Confidence Interval (Conversion Rate Difference) ──────
    p1, p2 = control_rate, treatment_rate
    n1, n2 = len(control), len(treatment)
    diff = p2 - p1
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z = 1.96  # 95% CI
    ci_lower = round(diff - z * se, 4)
    ci_upper = round(diff + z * se, 4)

    # ── Effect Size ───────────────────────────────────────────
    # Cohen's h for proportions
    cohens_h = 2 * (math.asin(math.sqrt(p2)) - math.asin(math.sqrt(p1)))

    # Cohen's d for revenue
    pooled_std = math.sqrt(
        (control["revenue"].std() ** 2 + treatment["revenue"].std() ** 2) / 2
    )
    cohens_d = (treatment["revenue"].mean() - control["revenue"].mean()) / pooled_std if pooled_std > 0 else 0

    def interpret_effect(d: float) -> str:
        d = abs(d)
        if d < 0.2:
            return "Negligible"
        elif d < 0.5:
            return "Small"
        elif d < 0.8:
            return "Medium"
        return "Large"

    # ── Statistical Power (optional) ──────────────────────────
    try:
        from statsmodels.stats.power import NormalIndPower
        power_analysis = NormalIndPower()
        power = power_analysis.solve_power(
            effect_size=abs(cohens_h),
            nobs1=n1,
            ratio=n2 / n1,
            alpha=0.05,
        )
    except Exception:
        power = None

    # ── Recommendation ────────────────────────────────────────
    alpha = 0.05
    if chi2_p < alpha and lift > 0:
        recommendation = (
            f"Statistically significant improvement detected. "
            f"The treatment group shows a {lift:.1f}% lift in conversion rate "
            f"(p={chi2_p:.4f}). Recommend rolling out the treatment."
        )
        recommendation_status = "positive"
    elif chi2_p < alpha and lift < 0:
        recommendation = (
            f"Statistically significant decline detected. "
            f"The treatment group shows a {lift:.1f}% drop in conversion rate "
            f"(p={chi2_p:.4f}). Do NOT roll out the treatment."
        )
        recommendation_status = "negative"
    else:
        recommendation = (
            f"No statistically significant difference detected "
            f"(p={chi2_p:.4f}, α=0.05). The observed {lift:.1f}% lift "
            f"could be due to random chance. Consider extending the experiment."
        )
        recommendation_status = "neutral"

    return {
        "experiment_name": experiment_name or df["experiment_name"].iloc[0],
        "total_participants": len(df),
        "lift_pct": round(lift, 2),
        "group_metrics": group_metrics,
        "chi_square_test": {
            "statistic": round(float(chi2), 4),
            "p_value": round(float(chi2_p), 6),
            "degrees_of_freedom": int(chi2_dof),
            "significant": bool(chi2_p < alpha),
        },
        "t_test_revenue": {
            "statistic": round(float(t_stat), 4),
            "p_value": round(float(t_p), 6),
            "significant": bool(t_p < alpha),
        },
        "confidence_interval": {
            "difference": round(diff, 4),
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "confidence_level": 0.95,
        },
        "effect_size": {
            "cohens_h": round(cohens_h, 4),
            "cohens_h_interpretation": interpret_effect(cohens_h),
            "cohens_d_revenue": round(float(cohens_d), 4),
            "cohens_d_interpretation": interpret_effect(cohens_d),
        },
        "statistical_power": round(float(power), 4) if power is not None else None,
        "recommendation": recommendation,
        "recommendation_status": recommendation_status,
    }


def get_experiment_list() -> list[dict]:
    """List available experiments."""
    engine = get_engine()
    query = text("""
        SELECT
            experiment_name,
            COUNT(*) AS participants,
            SUM(CASE WHEN converted THEN 1 ELSE 0 END) AS total_conversions,
            MIN(timestamp) AS start_date,
            MAX(timestamp) AS end_date
        FROM ab_tests
        GROUP BY experiment_name
        ORDER BY experiment_name
    """)
    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
        return [dict(r) for r in rows]
