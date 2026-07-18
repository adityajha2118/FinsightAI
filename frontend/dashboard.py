import streamlit as st, requests, os
from utils.styles import inject_css, module_card, section_header

st.set_page_config(
    page_title="FinSight AI — Enterprise Fintech Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
inject_css()

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 📊 FinSight AI")
    st.markdown("**Enterprise Fintech Analytics**")
    st.markdown("---")
    st.markdown("""
    **🔗 Navigate**
    - 📈 [Executive Dashboard](/5_executive_dashboard)
    - 👥 [Customer Intelligence](/1_customer_intelligence)
    - 📣 [Campaign Analytics](/2_campaign_analytics)
    - 🛡️ [Compliance & KYC](/3_compliance_analytics)
    - 📋 [Complaint Intelligence](/4_complaint_intelligence)
    """)
    st.markdown("---")
    st.markdown("**⚙️ System Status**")
    try:
        health = requests.get(f"{BACKEND}/api/health", timeout=3).json()
        st.success(f"✅ API Online — v{health.get('version','1.0.0')}")
    except:
        st.error("❌ API Offline")
    st.markdown("---")
    st.caption("FinSight AI v1.0 | Built with FastAPI + LangGraph + Streamlit")

# ── Hero Section ──────────────────────────────────────────
col_hero, col_badge = st.columns([3, 1])
with col_hero:
    st.markdown("# 📊 FinSight AI")
    st.markdown("### Enterprise-Grade Fintech Analytics & AI Platform")
    st.markdown("""
    A production-ready analytics platform combining **Machine Learning**, 
    **LLM-powered AI agents**, and **real-time dashboards** to deliver 
    360° customer intelligence across 6 financial analytics domains.
    """)

with col_badge:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:linear-gradient(135deg,#635BFF,#3498DB);
                border-radius:12px;padding:1rem;text-align:center;color:white;'>
      <div style='font-size:1.8rem;font-weight:700;'>6</div>
      <div style='font-size:0.75rem;opacity:0.9;'>Analytics Modules</div>
    </div>
    """, unsafe_allow_html=True)

# ── Live KPI Strip from API ───────────────────────────────
st.markdown("---")
section_header("📈 Live Platform Metrics", "Pulled from live FastAPI backend")

try:
    kpis = requests.get(f"{BACKEND}/api/customers/kpis", timeout=5).json()
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("👥 Total Customers",    f"{kpis.get('total_customers',0):,}")
    k2.metric("⚠️ Churn Rate",          f"{kpis.get('churn_rate',0):.1f}%")
    k3.metric("🛡️ High Risk Clients",   f"{kpis.get('high_risk_count',0):,}")
    k4.metric("✅ Active Customers",    f"{kpis.get('active_rate',0):.1f}%")
    k5.metric("💳 Avg Credit Limit",   f"${kpis.get('avg_credit_limit',0):,.0f}")
except:
    st.warning("⚠️ Backend not reachable — start FastAPI with: `python main.py`")

# ── Module Cards Grid ─────────────────────────────────────
st.markdown("---")
section_header("🚀 Platform Modules", "Click any card to navigate")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(module_card("👥", "Customer Intelligence",
        "Churn prediction · K-Means segmentation · Activity scoring · Unified profiles"),
        unsafe_allow_html=True)
with c2:
    st.markdown(module_card("📣", "Campaign Analytics",
        "Conversion prediction · Channel analysis · SMOTE-augmented ML · Fatigue modeling"),
        unsafe_allow_html=True)
with c3:
    st.markdown(module_card("🛡️", "KYC / Compliance",
        "AML risk scoring · PEP/OFAC flags · Structuring detection · Regulatory alerts"),
        unsafe_allow_html=True)

c4, c5, c6 = st.columns(3)
with c4:
    st.markdown(module_card("📋", "Complaint Intelligence",
        "LangGraph AI agent · NLP classification · Emotion detection · Live escalation"),
        unsafe_allow_html=True)
with c5:
    st.markdown(module_card("💳", "Fraud Analytics",
        "1.3M+ transaction EDA · Fraud pattern detection · Category risk analysis"),
        unsafe_allow_html=True)
with c6:
    st.markdown(module_card("📈", "Executive Dashboard",
        "Real-time KPIs · Cross-module insights · Risk heatmaps · Portfolio overview"),
        unsafe_allow_html=True)

# ── Tech Stack Strip ──────────────────────────────────────
st.markdown("---")
section_header("🛠️ Technology Stack")

t1,t2,t3,t4,t5,t6,t7 = st.columns(7)
tech = [("🐍","Python 3.11"),("⚡","FastAPI"),("🤖","LangGraph"),
        ("🧠","XGBoost"),("📊","Streamlit"),("🌐","Gemini/GPT"),("📦","scikit-learn")]
for col, (icon, name) in zip([t1,t2,t3,t4,t5,t6,t7], tech):
    col.markdown(f"""
    <div style='text-align:center;background:#1a1a2e;border:1px solid #635BFF33;
                border-radius:8px;padding:0.6rem;'>
        <div style='font-size:1.4rem;'>{icon}</div>
        <div style='color:#CBD5E1;font-size:0.7rem;margin-top:4px;'>{name}</div>
    </div>""", unsafe_allow_html=True)

# ── Dataset Summary ───────────────────────────────────────
st.markdown("---")
section_header("📂 Datasets Powering This Platform")

datasets = [
    ("bank_churners.csv",             "10,127",  "23", "Churn · Segmentation · Inactivity"),
    ("credit_card_transactions.csv",  "1,296,675","24", "Fraud Detection · Spend Analytics"),
    ("bank_transactions.csv",         "2,512",   "16", "Account Inactivity · Balance EDA"),
    ("bank_marketing.csv",            "100",     "22", "Campaign Conversion (SMOTE)"),
    ("kyc_part1.csv",                 "50,000",  "12", "AML Transaction Flags"),
    ("kyc_part2.csv",                 "2,000",   "12", "Entity Risk · PEP · Sanctions"),
    ("cfpb_complaints.csv",           "24,665",  "16", "NLP · Escalation · AI Agent"),
]
df_display = __import__('pandas').DataFrame(datasets,
    columns=["Dataset", "Rows", "Columns", "Used For"])
st.dataframe(df_display, use_container_width=True, hide_index=True)
