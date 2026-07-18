import streamlit as st, pandas as pd, plotly.express as px, requests, os
from utils.styles import inject_css, section_header

st.set_page_config(layout="wide", page_title="Executive Dashboard", page_icon="📈")
inject_css()

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("📈 Executive Dashboard")

@st.cache_data(ttl=300)
def load_kpis():
    try:
        return requests.get(f"{BACKEND}/api/customers/kpis").json()
    except:
        return {"total_customers": 0, "churn_rate": 0,
                "high_risk_count": 0, "active_rate": 0, "avg_credit_limit": 0}

@st.cache_data(ttl=300)
def load_churn_data():
    return pd.read_csv("data/processed/churn_predictions.csv")

@st.cache_data(ttl=300)
def load_segments():
    return pd.read_csv("data/processed/unified_customer_profile.csv")

@st.cache_data(ttl=300)
def load_kyc():
    return pd.read_parquet("data/feature_store/kyc_features.parquet")

@st.cache_data(ttl=300)
def load_activity():
    return pd.read_csv("data/processed/inactivity_scores.csv")

@st.cache_data(ttl=300)
def load_unified():
    return pd.read_csv("data/processed/unified_customer_profile.csv")

@st.cache_data(ttl=300)
def load_inactivity():
    return pd.read_csv("data/processed/inactivity_scores.csv")

kpis = load_kpis()
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Customers",    f"{kpis.get('total_customers', 0):,}")
col2.metric("⚠️ Churn Rate",          f"{kpis.get('churn_rate', 0)}%")
col3.metric("🛡️ High Risk Count",     f"{kpis.get('high_risk_count', 0):,}")
col4.metric("✅ Active Customers",    f"{kpis.get('active_rate', 0)}%")

st.markdown("---")
c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

with c1:
    try:
        df = load_churn_data()
        if 'churn_probability' in df.columns:
            fig = px.histogram(df, x='churn_probability', nbins=40,
                               title="Churn Probability Distribution",
                               color_discrete_sequence=["#E74C3C"],
                               template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load churn data: {e}")

with c2:
    try:
        df = load_segments()
        if 'segment_name' in df.columns:
            seg = df['segment_name'].value_counts().reset_index()
            seg.columns = ['segment', 'count']
            fig = px.pie(seg, values='count', names='segment',
                         title="Customer Segments", hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set2,
                         template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load segment data: {e}")

with c3:
    try:
        df = load_kyc()
        if 'risk_level' in df.columns:
            risk = df['risk_level'].value_counts().reset_index()
            risk.columns = ['level', 'count']
            fig = px.bar(risk, x='level', y='count',
                         title="KYC Compliance Risk Distribution",
                         color='level', template="plotly_white",
                         color_discrete_map={
                             "Critical": "#E74C3C", "High Risk": "#F39C12",
                             "Medium Risk": "#3498DB", "Low Risk": "#27AE60"
                         })
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load KYC data: {e}")

with c4:
    try:
        df = load_activity()
        if 'activity_category' in df.columns:
            act = df['activity_category'].value_counts().reset_index()
            act.columns = ['category', 'count']
            fig = px.pie(act, values='count', names='category',
                         title="Customer Activity Distribution", hole=0.4,
                         color_discrete_sequence=["#27AE60","#3498DB","#F39C12","#E74C3C"],
                         template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load activity data: {e}")

# ── Cross-Module Insights ─────────────────────────────────
section_header("🔗 Cross-Module Risk Intelligence")

# Load all data
unified = load_unified()
kyc     = load_kyc()
inact   = load_inactivity()

col_a, col_b = st.columns(2)

with col_a:
    # Segment × Risk Matrix (heatmap)
    if 'segment_name' in unified.columns and 'churn_risk_label' in unified.columns:
        pivot = unified.groupby(['segment_name','churn_risk_label']).size().unstack(fill_value=0)
        fig = px.imshow(pivot,
            title="Customer Segment × Churn Risk Matrix",
            color_continuous_scale='RdYlGn_r',
            template="plotly_white",
            text_auto=True)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

with col_b:
    # Future churn candidate donut
    if 'future_churn_candidate' in inact.columns:
        counts = inact['future_churn_candidate'].value_counts()
        labels = ['Future Churn Risk', 'Stable']
        fig = px.pie(values=counts.values, names=labels,
            title="Future Churn Candidate Breakdown",
            hole=0.55, color_discrete_sequence=['#E74C3C','#27AE60'],
            template="plotly_white")
        # Add center annotation
        fig.add_annotation(text=f"{int(inact['future_churn_candidate'].sum())}<br>At Risk",
            x=0.5, y=0.5, font_size=16, showarrow=False,
            font_color='#E74C3C', font=dict(weight=700))
        st.plotly_chart(fig, use_container_width=True)

# ── Platform Summary Stats Row ────────────────────────────
section_header("📊 Platform Data Coverage")
s1,s2,s3,s4 = st.columns(4)
s1.metric("📓 Notebooks Executed", "13")
s2.metric("🤖 ML Models Trained",  "9")
s3.metric("🔌 API Endpoints",      "15")
s4.metric("📂 Datasets Integrated","7")
