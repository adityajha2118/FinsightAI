import streamlit as st, pandas as pd, plotly.express as px, requests, os

st.set_page_config(layout="wide", page_title="Campaign Analytics", page_icon="📣")
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

PRIMARY   = "#635BFF"
SAFE      = "#27AE60"
WARNING   = "#F39C12"

st.title("📣 Campaign Analytics")

@st.cache_data(ttl=300)
def load_campaign_stats():
    try:
        return requests.get(f"{BACKEND}/api/campaign/stats").json()
    except Exception as e:
        st.error(f"Failed to fetch stats: {e}")
        return None

stats = load_campaign_stats()

if stats:
    st.subheader("Conversion Metrics")
    c1, c2 = st.columns(2)
    c1.metric("Overall Success Rate", f"{stats['success_rate']['success_rate']}%")
    c2.metric("Total Records", f"{stats['success_rate']['total_records']:,}")
    
    st.markdown("---")
    c3, c4, c5 = st.columns(3)
    
    with c3:
        job_df = pd.DataFrame(list(stats['by_job'].items()), columns=['Job', 'Conversion Rate'])
        fig = px.bar(job_df.sort_values('Conversion Rate'), y='Job', x='Conversion Rate', orientation='h', title="Conversion by Job", color_discrete_sequence=[PRIMARY], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c4:
        contact_df = pd.DataFrame(list(stats['by_contact'].items()), columns=['Contact', 'Conversion Rate'])
        fig = px.bar(contact_df, x='Contact', y='Conversion Rate', title="Conversion by Contact Method", color_discrete_sequence=[SAFE], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c5:
        month_df = pd.DataFrame(list(stats['by_month'].items()), columns=['Month', 'Conversion Rate'])
        fig = px.bar(month_df, x='Month', y='Conversion Rate', title="Conversion by Month", color_discrete_sequence=[WARNING], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.header("Predict Campaign Conversion")
with st.form("campaign_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        job = st.selectbox("Job (Encoded)", options=[0,1,2,3,4,5,6,7,8,9,10,11])
        marital = st.selectbox("Marital (Encoded)", options=[0,1,2])
        education = st.selectbox("Education (Encoded)", options=[0,1,2,3,4,5,6,7])
        default = st.selectbox("Default (Encoded)", options=[0,1,2])
    with c2:
        housing = st.selectbox("Housing (Encoded)", options=[0,1,2])
        loan = st.selectbox("Loan (Encoded)", options=[0,1,2])
        contact = st.selectbox("Contact Method (Encoded)", options=[0,1])
        month = st.selectbox("Month (Encoded)", options=[0,1,2,3,4,5,6,7,8,9])
        campaign = st.number_input("Campaign Contacts", value=1.0)
    with c3:
        pdays = st.number_input("Days since last contact (pdays)", value=999.0)
        previous = st.number_input("Previous contacts", value=0.0)
        poutcome = st.selectbox("Previous Outcome (Encoded)", options=[0,1,2])
        emp_var_rate = st.number_input("Emp. Var Rate", value=1.1)
        cons_price_idx = st.number_input("Cons. Price Index", value=93.994)
        
    c4, c5 = st.columns(2)
    with c4:
        cons_conf_idx = st.number_input("Cons. Conf. Index", value=-36.4)
        euribor3m = st.number_input("Euribor 3m", value=4.857)
    with c5:
        nr_employed = st.number_input("Num Employed", value=5191.0)
        
    submit = st.form_submit_button("Predict Conversion")

if submit:
    payload = {
        "age": age, "job": job, "marital": marital, "education": education,
        "default": default, "housing": housing, "loan": loan, "contact": contact,
        "month": month, "campaign": campaign, "pdays": pdays, "previous": previous,
        "poutcome": poutcome, "emp_var_rate": emp_var_rate,
        "cons_price_idx": cons_price_idx, "cons_conf_idx": cons_conf_idx,
        "euribor3m": euribor3m, "nr_employed": nr_employed,
        "contacted_before": 1 if pdays != 999 else 0,
        "campaign_intensity": campaign + previous
    }
    try:
        res = requests.post(f"{BACKEND}/api/campaign/predict", json=payload).json()
        prob = res.get("conversion_probability", 0)
        st.success(f"### Predicted Conversion Probability: {prob:.2%}")
        if prob > 0.5:
            st.info("Likely to convert! High priority prospect.")
        else:
            st.warning("Unlikely to convert.")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
