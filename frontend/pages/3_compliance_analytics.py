import streamlit as st, pandas as pd, plotly.express as px, requests, os

st.set_page_config(layout="wide", page_title="Compliance Analytics", page_icon="🛡️")
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

PRIMARY   = "#635BFF"
RISK      = "#E74C3C"
SAFE      = "#27AE60"
NEUTRAL   = "#3498DB"
WARNING   = "#F39C12"

st.title("🛡️ KYC / Compliance Analytics")

@st.cache_data(ttl=300)
def load_kyc_data():
    return pd.read_parquet("data/feature_store/kyc_features.parquet")

try:
    kyc_df = load_kyc_data()
except Exception as e:
    st.error(f"Error loading KYC data: {e}")
    st.stop()

st.header("Overall Risk Assessment")
c1, c2 = st.columns(2)

with c1:
    risk_dist = kyc_df['risk_level'].value_counts().reset_index()
    risk_dist.columns = ['level', 'count']
    fig = px.pie(risk_dist, values='count', names='level', title="Risk Level Distribution", hole=0.3,
                 color='level', color_discrete_map={"Critical": RISK, "High Risk": WARNING, "Medium Risk": NEUTRAL, "Low Risk": SAFE}, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    if 'sector_risk' in kyc_df.columns:
        sec = kyc_df.groupby(['sector_risk', 'risk_level']).size().reset_index(name='count')
        fig = px.bar(sec, x='sector_risk', y='count', color='risk_level', barmode='group',
                     title="Sector Risk vs KYC Risk Level", template="plotly_white",
                     color_discrete_map={"Critical": RISK, "High Risk": WARNING, "Medium Risk": NEUTRAL, "Low Risk": SAFE})
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("Critical Risk Flags Distribution")
flags = ['pep_flag', 'sanctions_flag', 'ofac_match_flag', 'structuring_pattern_flag']
flag_sums = {f: kyc_df[f].sum() for f in flags if f in kyc_df.columns}
if flag_sums:
    f_df = pd.DataFrame(list(flag_sums.items()), columns=['Flag', 'Count'])
    fig = px.bar(f_df, x='Flag', y='Count', title="Occurrences of Critical Flags", color_discrete_sequence=[RISK], template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.header("Top 50 High-Risk Clients")
top_50 = kyc_df.sort_values('kyc_risk_score', ascending=False).head(50)
cols = ['client_id', 'kyc_risk_score', 'risk_level', 'pep_flag', 'sanctions_flag', 'ofac_match_flag']
avail_cols = [c for c in cols if c in top_50.columns]
st.dataframe(top_50[avail_cols].style.background_gradient(subset=['kyc_risk_score'], cmap='Reds'), use_container_width=True)

st.markdown("---")
st.header("Simulate KYC Risk Assessment")
with st.form("kyc_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        pep = st.checkbox("PEP (Politically Exposed Person)")
        sanctions = st.checkbox("Sanctions Hit")
        ofac_match = st.checkbox("OFAC Match")
        ofac_country = st.checkbox("OFAC Country")
    with c2:
        fatf_txn = st.checkbox("FATF Non-Cooperative Transaction")
        fatf_entity = st.checkbox("FATF Entity")
        sectoral = st.checkbox("Sectoral Sanctions Hit")
    with c3:
        structuring = st.checkbox("Structuring Pattern Detected")
        rapid = st.checkbox("Rapid Movement Flag")
        trade = st.checkbox("Trade Mispricing Flag")
        
    c4, c5 = st.columns(2)
    with c4:
        opacity = st.slider("Ownership Opacity Score", 0.0, 1.0, 0.5)
    with c5:
        sector_risk = st.selectbox("Sector Risk", options=["Low", "Medium", "High"])
        
    submit = st.form_submit_button("Assess Risk")

if submit:
    payload = {
        "pep_flag": int(pep), "sanctions_flag": int(sanctions), "ofac_match_flag": int(ofac_match),
        "ofac_country_flag": int(ofac_country), "fatf_txn_flag": int(fatf_txn), "fatf_entity_flag": int(fatf_entity),
        "sectoral_sanctions_flag": int(sectoral), "structuring_pattern_flag": int(structuring),
        "rapid_movement_flag": int(rapid), "trade_mispricing_flag": int(trade),
        "ownership_opacity_score": opacity, "sector_risk": sector_risk
    }
    try:
        res = requests.post(f"{BACKEND}/api/compliance/risk/predict", json=payload).json()
        st.success("### Risk Assessment Complete")
        st.metric("KYC Risk Score", f"{res['risk_score']:.4f}")
        st.info(f"**Risk Level:** {res['risk_level']}")
        st.warning(f"**Recommended Action:** {res['recommended_action']}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
