"""FinSight AI — Risk Badge Component."""

import streamlit as st


RISK_COLORS = {
    "CRITICAL": ("#E74C3C", "#FADBD8"),
    "HIGH": ("#E67E22", "#FDEBD0"),
    "MEDIUM": ("#F39C12", "#FEF9E7"),
    "STANDARD": ("#2ECC71", "#D5F5E3"),
    "LOW": ("#2ECC71", "#D5F5E3"),
}


def render_risk_badge(level: str) -> str:
    """Generate HTML for a color-coded risk badge.

    Args:
        level: Risk level string (CRITICAL, HIGH, MEDIUM, STANDARD, LOW).

    Returns:
        HTML string for the badge.
    """
    level = level.upper()
    fg, bg = RISK_COLORS.get(level, ("#95A5A6", "#EAECEE"))

    return (
        f'<span style="background:{bg};color:{fg};padding:2px 8px;'
        f'border-radius:4px;font-size:0.75rem;font-weight:600;">'
        f'{level}</span>'
    )
