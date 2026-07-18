import streamlit as st, pandas as pd, plotly.express as px, os
from sklearn.decomposition import PCA
from utils.styles import inject_css, section_header

st.set_page_config(layout="wide", page_title="Customer Intelligence", page_icon="👥")
inject_css()
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

PRIMARY   = "#635BFF"
RISK      = "#E74C3C"
SAFE      = "#27AE60"
NEUTRAL   = "#3498DB"
WARNING   = "#F39C12"

st.title("👥 Customer Intelligence")

@st.cache_data(ttl=300)
def load_profile():
    return pd.read_csv("data/processed/unified_customer_profile.csv")

@st.cache_data(ttl=300)
def load_churn():
    return pd.read_csv("data/processed/churn_predictions.csv")

@st.cache_data(ttl=300)
def load_inactivity():
    return pd.read_csv("data/processed/inactivity_scores.csv")

@st.cache_data(ttl=300)
def load_bank_tx():
    return pd.read_csv("data/processed/bank_tx_activity.csv")

@st.cache_data(ttl=300)
def load_customer_clean():
    return pd.read_csv("data/processed/customer_clean.csv")

@st.cache_data(ttl=300)
def load_features():
    return pd.read_parquet("data/feature_store/customer_features.parquet")

try:
    profile_df = load_profile()
    churn_df = load_churn()
    inactivity_df = load_inactivity()
    bank_tx_df = load_bank_tx()
    customer_clean_df = load_customer_clean()
    features_df = load_features()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Segmentation", "Churn Predictions", "Inactivity & Watchlist"])

with tab1:
    st.header("Customer Segmentation")
    c1, c2 = st.columns(2)
    
    with c1:
        seg = profile_df['segment_name'].value_counts().reset_index()
        seg.columns = ['segment', 'count']
        fig = px.pie(seg, values='count', names='segment', title="Segment Distribution", hole=0.4, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        churn_seg = profile_df.groupby('segment_name')['churn_probability'].mean().reset_index()
        fig = px.bar(churn_seg, x='segment_name', y='churn_probability', title="Mean Churn Probability per Segment", color_discrete_sequence=[RISK], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    st.subheader("Cluster Profile")
    prof_table = profile_df.groupby('segment_name')[['Credit_Limit', 'Total_Trans_Amt', 'Total_Trans_Ct', 'Avg_Utilization_Ratio']].mean().round(2)
    st.dataframe(prof_table, use_container_width=True)
    
    if 'segment_name' in profile_df.columns and 'churn_probability' in profile_df.columns:
        segments = profile_df.groupby('segment_name').agg(
            count=('CLIENTNUM','count'),
            avg_churn=('churn_probability','mean'),
            avg_credit=('Credit_Limit','mean')
        ).reset_index()
        
        st.markdown("**📋 Segment Business Insights**")
        seg_cols = st.columns(len(segments))
        for i, (_, row) in enumerate(segments.iterrows()):
            with seg_cols[i]:
                risk_color = '#E74C3C' if row['avg_churn'] > 0.5 else \
                             '#F39C12' if row['avg_churn'] > 0.3 else '#27AE60'
                st.markdown(f"""
                <div style='background:#1a1a2e;border:1px solid {risk_color}44;
                            border-radius:10px;padding:1rem;text-align:center;'>
                  <div style='color:{risk_color};font-size:1.2rem;font-weight:700;'>
                    {row['avg_churn']:.0%}</div>
                  <div style='color:#CBD5E1;font-size:0.75rem;font-weight:600;
                              margin:4px 0;'>{row['segment_name']}</div>
                  <div style='color:#94A3B8;font-size:0.7rem;'>
                    {int(row['count']):,} customers</div>
                </div>""", unsafe_allow_html=True)

    st.subheader("PCA 2D Scatter")
    try:
        pca = PCA(n_components=2)
        numeric_features = ['Credit_Limit','Total_Trans_Amt','Total_Trans_Ct','Avg_Utilization_Ratio','Total_Revolving_Bal','Months_Inactive_12_mon']
        pca_result = pca.fit_transform(features_df[numeric_features].fillna(0))
        features_df['pca_1'] = pca_result[:, 0]
        features_df['pca_2'] = pca_result[:, 1]
        fig = px.scatter(features_df, x='pca_1', y='pca_2', color='segment_name', template="plotly_white", opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"PCA generation failed: {e}")

with tab2:
    st.header("Churn Predictions")
    c1, c2 = st.columns(2)
    
    with c1:
        fig = px.histogram(churn_df, x='churn_probability', nbins=40, title="Churn Probability Distribution", color_discrete_sequence=[RISK], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        crl = profile_df['churn_risk_label'].value_counts().reset_index()
        crl.columns = ['label', 'count']
        fig = px.bar(crl, x='label', y='count', title="Churn Risk Label Distribution", color='label', color_discrete_map={"High Risk": RISK, "Medium Risk": WARNING, "Loyal": SAFE}, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    c3, c4, c5 = st.columns(3)
    
    with c3:
        cr1 = profile_df.groupby('Card_Category')['churn_probability'].mean().reset_index()
        fig = px.bar(cr1, x='Card_Category', y='churn_probability', title="Churn Rate by Card Category", color_discrete_sequence=[PRIMARY], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c4:
        cr2 = profile_df.groupby('Income_Category')['churn_probability'].mean().reset_index()
        fig = px.bar(cr2, x='Income_Category', y='churn_probability', title="Churn Rate by Income", color_discrete_sequence=[PRIMARY], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c5:
        cr3 = profile_df.groupby('Gender')['churn_probability'].mean().reset_index()
        fig = px.bar(cr3, x='Gender', y='churn_probability', title="Churn Rate by Gender", color_discrete_sequence=[PRIMARY], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 50 Churn Risk Customers")
    top_50 = profile_df[['CLIENTNUM', 'churn_probability', 'churn_risk_label', 'segment_name']].sort_values('churn_probability', ascending=False).head(50)
    
    def color_risk(val):
        color = '#ffebee' if val == 'High Risk' else '#fff8e1' if val == 'Medium Risk' else '#e8f5e9'
        return f'background-color: {color}'
        
    st.dataframe(top_50.style.map(color_risk, subset=['churn_risk_label']), use_container_width=True)

    # Feature importance bar chart
    st.markdown("---")
    section_header("🎯 Key Churn Drivers", "Top features by XGBoost importance")
    
    try:
        import joblib, pandas as pd
        model = joblib.load("models/churn/xgboost_model.pkl")
        if hasattr(model, 'feature_importances_'):
            feat_names = [
                'Customer_Age','Dependent_count','Months_on_book',
                'Months_Inactive_12_mon','Contacts_Count_12_mon',
                'Credit_Limit','Total_Revolving_Bal','Avg_Open_To_Buy',
                'Total_Amt_Chng_Q4_Q1','Total_Trans_Amt','Total_Trans_Ct',
                'Total_Ct_Chng_Q4_Q1','Avg_Utilization_Ratio',
                'Income_Category','Card_Category','Gender',
                'Education_Level','Marital_Status'
            ]
            importances = model.feature_importances_
            fi_df = pd.DataFrame({'Feature': feat_names[:len(importances)],
                                   'Importance': importances}).sort_values(
                                   'Importance', ascending=True).tail(12)
            fig = px.bar(fi_df, x='Importance', y='Feature',
                         orientation='h', title="XGBoost Feature Importance",
                         color='Importance', color_continuous_scale='Blues',
                         template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.caption(f"Feature importance chart: {e}")

with tab3:
    st.header("Inactivity & Watchlist")
    c1, c2 = st.columns(2)
    
    with c1:
        ac = inactivity_df['activity_category'].value_counts().reset_index()
        ac.columns = ['category', 'count']
        fig = px.bar(ac, x='category', y='count', color='category', color_discrete_map={'Active': SAFE, 'Moderately Active': NEUTRAL, 'Inactive': WARNING, 'High Risk': RISK}, title="Activity Category", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        fig = px.histogram(inactivity_df, x='activity_score', nbins=40, title="Activity Score", color_discrete_sequence=[PRIMARY], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    c3, c4 = st.columns(2)
    
    with c3:
        fc = inactivity_df['future_churn_candidate'].value_counts().reset_index()
        fc.columns = ['candidate', 'count']
        fc['candidate'] = fc['candidate'].map({True: 'Yes', False: 'No'})
        fig = px.bar(fc, x='candidate', y='count', color='candidate', color_discrete_map={'Yes': RISK, 'No': SAFE}, title="Future Churn Candidates", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c4:
        fig = px.histogram(customer_clean_df, x='Months_Inactive_12_mon', title="Months Inactive", color_discrete_sequence=[WARNING], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    st.subheader("Bank Transactions Activity")
    c5, c6 = st.columns(2)
    with c5:
        fig = px.histogram(bank_tx_df, x='avg_balance', title="Account Balance Distribution", color_discrete_sequence=[NEUTRAL], template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    with c6:
        hr = bank_tx_df['high_risk_account'].value_counts().reset_index()
        hr.columns = ['high_risk', 'count']
        hr['high_risk'] = hr['high_risk'].map({True: 'Yes', False: 'No'})
        fig = px.pie(hr, values='count', names='high_risk', title="High Risk Accounts (>60 days inactive)", color='high_risk', color_discrete_map={'Yes': RISK, 'No': SAFE}, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    st.subheader("Future Churn Watchlist")
    watchlist = inactivity_df[inactivity_df['future_churn_candidate'] == True].sort_values('activity_score', ascending=True).head(100)
    st.dataframe(watchlist, use_container_width=True)
