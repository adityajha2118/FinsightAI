"""FinSight AI — Reusable KPI Card Component."""

import streamlit as st


def render_kpi_card(icon: str, label: str, value: str, delta: str = None) -> None:
    """Render a styled KPI metric card.

    Args:
        icon: Emoji icon for the card.
        label: Metric label text.
        value: Metric value to display.
        delta: Optional delta/change indicator.
    """
    delta_html = ""
    if delta:
        color = "#2ECC71" if delta.startswith("+") else "#E74C3C"
        delta_html = f'<div style="color:{color};font-size:0.75rem;">{delta}</div>'

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                border:1px solid #635BFF33;border-radius:12px;
                padding:1rem;text-align:center;'>
        <div style='font-size:1.5rem;'>{icon}</div>
        <div style='color:#CBD5E1;font-size:0.75rem;margin:4px 0;'>{label}</div>
        <div style='color:white;font-size:1.3rem;font-weight:700;'>{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)
