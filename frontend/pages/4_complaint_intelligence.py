import streamlit as st, pandas as pd, plotly.express as px, requests, os
from utils.styles import inject_css, section_header

st.set_page_config(layout="wide", page_title="Complaint Intelligence", page_icon="📋")
inject_css()
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

PRIMARY   = "#635BFF"
RISK      = "#E74C3C"
SAFE      = "#27AE60"
NEUTRAL   = "#3498DB"
WARNING   = "#F39C12"

st.title("📋 Complaint Intelligence (GenAI)")

@st.cache_data(ttl=300)
def load_complaints_nlp():
    return pd.read_csv("data/processed/complaints_with_nlp.csv")

@st.cache_data(ttl=300)
def load_escalation():
    return pd.read_csv("data/processed/complaints_with_escalation.csv")

tab1, tab2, tab3 = st.tabs(["NLP Insights", "Escalation Predictions", "Live GenAI Agent"])

with tab1:
    st.header("Sentiment & Classification")
    try:
        nlp_df = load_complaints_nlp()
        c1, c2 = st.columns(2)
        
        with c1:
            cat = nlp_df['complaint_category'].value_counts().reset_index()
            cat.columns = ['category', 'count']
            fig = px.pie(cat, values='count', names='category', title="Complaint Categories (AI Classified)", hole=0.3, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            emo = nlp_df['emotion'].value_counts().reset_index()
            emo.columns = ['emotion', 'count']
            fig = px.bar(emo, x='emotion', y='count', title="Detected Emotions", color='emotion', color_discrete_map={"Anger": RISK, "Frustration": WARNING, "Neutral": NEUTRAL, "Legal Threat": RISK, "Distress": WARNING}, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
        st.subheader("Sample AI Summaries")
        samples = nlp_df[['narrative', 'complaint_category', 'emotion', 'complaint_summary']].sample(10)
        for _, row in samples.iterrows():
            with st.expander(f"{row['complaint_category']} - {row['emotion']}"):
                st.write("**Original:**", str(row['narrative'])[:500] + "...")
                st.write("**AI Summary:**", row['complaint_summary'])
                
    except Exception as e:
        st.error(f"Error loading NLP data: {e}")

with tab2:
    st.header("Escalation Predictions")
    try:
        esc_df = load_escalation()
        c1, c2 = st.columns(2)
        
        with c1:
            fig = px.histogram(esc_df, x='escalation_probability', nbins=30, title="Escalation Probability Distribution", color_discrete_sequence=[RISK], template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            esc_emo = esc_df.groupby('emotion')['escalation_flag'].mean().reset_index()
            fig = px.bar(esc_emo, x='emotion', y='escalation_flag', title="Escalation Rate by Emotion", color_discrete_sequence=[WARNING], template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
        st.subheader("Top Risk Complaints")
        top_risk = esc_df.sort_values('escalation_probability', ascending=False).head(20)
        st.dataframe(top_risk[['Product', 'complaint_category', 'emotion', 'escalation_probability', 'timely_response']].style.background_gradient(subset=['escalation_probability'], cmap='Reds'), use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading escalation data: {e}")

with tab3:
    st.header("Live GenAI Complaint Agent")
    st.info("Paste a customer complaint below to instantly summarize, classify, detect emotion, and generate a response using LangGraph & Groq.")
    
    section_header("🤖 AI Agent Architecture")
    st.markdown("""
    <div style='background:#1a1a2e;border:1px solid #635BFF33;border-radius:12px;
                 padding:1.2rem;margin-bottom:1rem;'>
      <div style='color:#CBD5E1;font-size:0.85rem;line-height:2;'>
        <strong style='color:#635BFF;'>Processing Pipeline (LangGraph StateGraph):</strong><br>
        📥 Input Narrative
        → 📋 <strong>Summarize</strong> (Gemini 1.5 Flash)
        → 🏷️ <strong>Classify</strong> (8 categories)
        → 😤 <strong>Detect Emotion</strong> (5 emotions)
        → ⚡ <strong>Score Escalation</strong> (XGBoost)
        → 🚦 <strong>Route Priority</strong> (Business Rules)
        → 💬 <strong>Generate Response</strong> (LLM)
        → ✅ Output
      </div>
    </div>
    """, unsafe_allow_html=True)

    sample_complaints = {
        "Select a sample...": "",
        "Fraud Dispute (High Escalation)": 
            "I have been trying to dispute a fraudulent charge of $847 on my credit card "
            "for over 3 months. Every time I call, I am transferred between departments "
            "with no resolution. This is completely unacceptable and I am now consulting "
            "with my attorney about legal options.",
        "Billing Issue (Medium)":
            "I was charged twice for my annual fee this month. I called customer service "
            "and was told it would be reversed but it has been 2 weeks and nothing has "
            "happened. I am very frustrated with this experience.",
        "Rewards Problem (Standard)":
            "I redeemed my cashback rewards last week but the credit has not appeared "
            "on my account yet. The website says it should take 3-5 days but it has "
            "been 8 days now. Please help."
    }
    selected = st.selectbox("📋 Or choose a sample complaint:", list(sample_complaints.keys()))
    if selected != "Select a sample...":
        narrative_default = sample_complaints[selected]
    else:
        narrative_default = ""

    narrative = st.text_area("📝 Paste complaint narrative", value=narrative_default, height=180)
    submit = st.button("Process Complaint")
    
    if submit and narrative:
        with st.spinner("Processing through AI pipeline..."):
            try:
                res = requests.post(f"{BACKEND}/api/complaints/process", json={"narrative": narrative}).json()
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Category", res.get('category', 'N/A'))
                c2.metric("Emotion", res.get('emotion', 'N/A'))
                c3.metric("Escalation Risk", f"{res.get('escalation_probability', 0):.2%}")
                
                st.markdown("### AI Summary")
                st.write(res.get('summary', ''))
                
                st.markdown("### Routing & Resolution")
                st.write(f"**Priority:** {res.get('priority_level', 'N/A')}")
                st.write(f"**Team:** {res.get('assigned_team', 'N/A')}")
                st.write(f"**Action:** {res.get('recommended_action', 'N/A')}")
                
                st.markdown("### Suggested Response")
                st.success(res.get('suggested_response', ''))
                
            except Exception as e:
                st.error(f"Failed to process complaint: {e}")
