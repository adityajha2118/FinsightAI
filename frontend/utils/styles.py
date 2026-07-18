CUSTOM_CSS = """
<style>
  /* ── Global resets ─────────────────────────── */
  .block-container { padding-top: 1.5rem !important; }
  
  /* ── KPI metric cards ───────────────────────── */
  [data-testid="metric-container"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #635BFF33;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0 4px 15px rgba(99,91,255,0.15);
    transition: transform 0.2s ease;
  }
  [data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99,91,255,0.25);
  }
  [data-testid="stMetricLabel"] { color: #9CA3AF !important; font-size: 0.8rem !important; }
  [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.6rem !important; font-weight: 700 !important; }
  
  /* ── Section headers ────────────────────────── */
  .section-header {
    background: linear-gradient(90deg, #635BFF, #3498DB);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 1.5rem 0 0.5rem 0;
  }
  
  /* ── Module cards on homepage ───────────────── */
  .module-card {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    border: 1px solid rgba(99,91,255,0.3);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    height: 160px;
  }
  .module-card:hover {
    border-color: #635BFF;
    box-shadow: 0 0 30px rgba(99,91,255,0.3);
    transform: translateY(-4px);
  }
  .module-card .icon { font-size: 2rem; margin-bottom: 0.5rem; }
  .module-card .title { color: #E2E8F0; font-size: 1rem; font-weight: 600; }
  .module-card .desc  { color: #94A3B8; font-size: 0.75rem; margin-top: 0.3rem; }
  
  /* ── Badge pills ────────────────────────────── */
  .badge-critical { background:#E74C3C22; color:#E74C3C; border:1px solid #E74C3C44; 
                    border-radius:20px; padding:2px 10px; font-size:0.75rem; font-weight:600; }
  .badge-high     { background:#F39C1222; color:#F39C12; border:1px solid #F39C1244;
                    border-radius:20px; padding:2px 10px; font-size:0.75rem; font-weight:600; }
  .badge-medium   { background:#3498DB22; color:#3498DB; border:1px solid #3498DB44;
                    border-radius:20px; padding:2px 10px; font-size:0.75rem; font-weight:600; }
  .badge-safe     { background:#27AE6022; color:#27AE60; border:1px solid #27AE6044;
                    border-radius:20px; padding:2px 10px; font-size:0.75rem; font-weight:600; }

  /* ── Info banners ───────────────────────────── */
  .info-banner {
    background: linear-gradient(90deg, #635BFF11, #3498DB11);
    border-left: 3px solid #635BFF;
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    color: #CBD5E1;
    font-size: 0.85rem;
  }
  
  /* ── Sidebar styling ────────────────────────── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    border-right: 1px solid #635BFF33;
  }
  [data-testid="stSidebar"] .stMarkdown { color: #CBD5E1; }
  
  /* ── Tab styling ─────────────────────────────── */
  .stTabs [data-baseweb="tab-list"] {
    background-color: #0f0f1a;
    border-bottom: 2px solid #635BFF33;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 8px 20px;
    color: #9CA3AF;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #635BFF22, #3498DB22);
    color: #635BFF !important;
    border-bottom: 2px solid #635BFF;
  }
  
  /* ── Divider ─────────────────────────────────── */
  hr { border-color: #635BFF22 !important; }
</style>
"""

def inject_css():
    """Inject global FinSight AI CSS into the current Streamlit page."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def section_header(title: str, subtitle: str = ""):
    """Render a styled gradient section header."""
    import streamlit as st
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)

def module_card(icon: str, title: str, desc: str) -> str:
    """Return HTML for a module card."""
    return f"""
    <div class="module-card">
      <div class="icon">{icon}</div>
      <div class="title">{title}</div>
      <div class="desc">{desc}</div>
    </div>"""

def badge(level: str) -> str:
    """Return HTML badge for a risk/priority level."""
    mapping = {
        'CRITICAL': 'badge-critical', 'Critical': 'badge-critical',
        'HIGH': 'badge-high', 'High Risk': 'badge-high',
        'MEDIUM': 'badge-medium', 'Medium Risk': 'badge-medium',
        'LOW': 'badge-safe', 'Low Risk': 'badge-safe',
        'Loyal': 'badge-safe', 'Active': 'badge-safe',
        'High Risk': 'badge-critical'
    }
    css_class = mapping.get(level, 'badge-medium')
    return f'<span class="{css_class}">{level}</span>'

def info_banner(text: str):
    """Render a styled info banner."""
    import streamlit as st
    st.markdown(f'<div class="info-banner">ℹ️ {text}</div>', unsafe_allow_html=True)
