"""Generate notebooks 11, 12, 13"""
import nbformat as nbf

# ═══════ NOTEBOOK 11 ═══════
nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 11 - Complaint Sentiment & NLP Analysis\nLLM-powered summarization, classification, and emotion detection using Groq."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np, os, time
from dotenv import load_dotenv
load_dotenv()
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
import plotly.express as px
"""))
c.append(nbf.v4.new_code_cell("""# LLM setup
provider = os.getenv("LLM_PROVIDER", "groq")
print(f"LLM Provider: {provider}")

if provider == "groq":
    from langchain_groq import ChatGroq
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.1,
                   api_key=os.getenv("GROQ_API_KEY"))
elif provider == "gemini":
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
else:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Quick test
resp = llm.invoke("Say 'LLM connection OK' and nothing else.")
print(f"LLM test: {resp.content.strip()}")
"""))
c.append(nbf.v4.new_code_cell("""# Load data and sample
df = pd.read_csv('data/processed/complaints_clean.csv')
print(f"Full shape: {df.shape}")

sample_df = df.dropna(subset=['narrative'])
sample_df = sample_df[sample_df['narrative'].str.len() > 50]
sample_df = sample_df.sample(n=min(500, len(sample_df)), random_state=SEED).reset_index(drop=True)
print(f"Sample shape: {sample_df.shape}")
"""))
c.append(nbf.v4.new_code_cell("""# STEP 1: Complaint Summarization
summaries = []
checkpoint_path = 'data/processed/complaints_nlp_checkpoint.csv'

for i, row in sample_df.iterrows():
    prompt = f"Summarize this customer financial complaint in 1-2 sentences, focusing on the core issue: {str(row['narrative'])[:1000]}"
    try:
        response = llm.invoke(prompt)
        result = response.content.strip()
    except Exception as e:
        print(f"Error at row {i}: {e}")
        time.sleep(2)
        try:
            response = llm.invoke(prompt[:500])
            result = response.content.strip()
        except:
            result = "Summary unavailable"
    summaries.append(result)
    time.sleep(0.3)
    if (i + 1) % 50 == 0:
        print(f"Summarization checkpoint: {i+1}/{len(sample_df)}")

sample_df['complaint_summary'] = summaries
print(f"Summarization complete. Sample: {summaries[0][:100]}...")
"""))
c.append(nbf.v4.new_code_cell("""# STEP 2: Classification
categories_list = []
for i, row in sample_df.iterrows():
    prompt = (f"Classify this financial complaint into exactly ONE category. "
              f"Categories: Billing, Fraud, Card Declined, Rewards, Customer Service, Service Delay, Credit Reporting, Collections. "
              f"Return ONLY the category name with no other text. "
              f"Complaint: {str(row['narrative'])[:800]}")
    try:
        response = llm.invoke(prompt)
        result = response.content.strip()
    except:
        time.sleep(2)
        try:
            response = llm.invoke(prompt[:400])
            result = response.content.strip()
        except:
            result = "Unknown"
    categories_list.append(result)
    time.sleep(0.3)
    if (i + 1) % 50 == 0:
        print(f"Classification checkpoint: {i+1}/{len(sample_df)}")

sample_df['complaint_category'] = categories_list
print(f"Classification complete.")
print(sample_df['complaint_category'].value_counts())
"""))
c.append(nbf.v4.new_code_cell("""# STEP 3: Emotion Detection
emotions = []
for i, row in sample_df.iterrows():
    prompt = (f"Detect the dominant emotion in this financial complaint. "
              f"Return ONLY one word from: Anger, Frustration, Neutral, Legal Threat, Distress. "
              f"No other text. Complaint: {str(row['narrative'])[:800]}")
    try:
        response = llm.invoke(prompt)
        result = response.content.strip()
    except:
        time.sleep(2)
        try:
            response = llm.invoke(prompt[:400])
            result = response.content.strip()
        except:
            result = "Neutral"
    emotions.append(result)
    time.sleep(0.3)
    if (i + 1) % 50 == 0:
        print(f"Emotion checkpoint: {i+1}/{len(sample_df)}")

sample_df['emotion'] = emotions
print(f"Emotion detection complete.")
print(sample_df['emotion'].value_counts())
"""))
c.append(nbf.v4.new_code_cell("""# Plot 1: complaint_category distribution
fig = px.pie(sample_df, names='complaint_category', title='Complaint Category Distribution',
             hole=0.3, template=TEMPLATE)
fig.show()

cat_counts = sample_df['complaint_category'].value_counts().reset_index()
cat_counts.columns = ['category','count']
fig = px.bar(cat_counts, x='category', y='count', color_discrete_sequence=[PRIMARY],
             template=TEMPLATE, title='Complaint Categories')
fig.update_xaxes(tickangle=45)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 2: emotion distribution
emo = sample_df['emotion'].value_counts().reset_index(); emo.columns=['emotion','count']
fig = px.bar(emo, x='emotion', y='count', color_discrete_sequence=[RISK],
             template=TEMPLATE, title='Emotion Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 3: Category x Emotion heatmap
try:
    pivot = sample_df.groupby(['complaint_category','emotion']).size().unstack(fill_value=0)
    fig = px.imshow(pivot, color_continuous_scale='Purples', template=TEMPLATE,
                    title='Category x Emotion Heatmap', text_auto=True)
    fig.show()
except Exception as e:
    print(f"Heatmap error: {e}")
"""))
c.append(nbf.v4.new_code_cell("""# Plot 4: narrative_length by emotion
fig = px.histogram(sample_df, x='narrative_length', color='emotion',
                   template=TEMPLATE, title='Narrative Length by Emotion', nbins=30)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 5: Timely response by category
if 'timely_response' in sample_df.columns:
    ct = sample_df.groupby(['complaint_category','timely_response']).size().reset_index(name='count')
    fig = px.bar(ct, x='complaint_category', y='count', color='timely_response', barmode='group',
                 color_discrete_map={'Yes':SAFE,'No':RISK},
                 template=TEMPLATE, title='Timely Response by Category')
    fig.update_xaxes(tickangle=45)
    fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Save
sample_df.to_csv('data/processed/complaints_with_nlp.csv', index=False)
print(f"Saved complaints_with_nlp.csv - shape: {sample_df.shape}")
"""))
nb.cells = c
nbf.write(nb, 'notebooks/11_complaint_sentiment.ipynb')
print("Created 11_complaint_sentiment.ipynb")

# ═══════ NOTEBOOK 12 ═══════
nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 12 - Escalation Prediction\nPredict complaint escalation using NLP features + ML."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np, joblib, os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, classification_report
import plotly.express as px, plotly.graph_objects as go
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))
c.append(nbf.v4.new_code_cell("""df = pd.read_csv('data/processed/complaints_with_nlp.csv')
print(f"Shape: {df.shape}")

# Target engineering
untimely_responses = ['Untimely response','In progress','No response',"Company can't substantiate response"]
high_emotion = ['Anger','Legal Threat','Distress']

df['escalation_flag'] = (
    (df['company_response'].isin(untimely_responses)) |
    (df['timely_response'] == 'No') |
    (df['emotion'].isin(high_emotion))
).astype(int)

print(f"Escalation rate: {df['escalation_flag'].mean():.4f}")
print(df['escalation_flag'].value_counts())
"""))
c.append(nbf.v4.new_code_cell("""# Feature engineering
le_cat = LabelEncoder()
le_emo = LabelEncoder()
le_prod = LabelEncoder()
le_via = LabelEncoder()

df['category_encoded'] = le_cat.fit_transform(df['complaint_category'].fillna('Unknown'))
df['emotion_encoded'] = le_emo.fit_transform(df['emotion'].fillna('Neutral'))
df['product_encoded'] = le_prod.fit_transform(df['Product'].fillna('Unknown'))
df['via_encoded'] = le_via.fit_transform(df['submitted_via'].fillna('Unknown'))
df['timely_binary'] = (df['timely_response'] == 'No').astype(int)
df['narrative_length'] = df['narrative'].apply(lambda x: len(str(x).split()))

feature_cols = ['category_encoded','emotion_encoded','product_encoded','via_encoded','timely_binary','narrative_length']
X = df[feature_cols]
y = df['escalation_flag']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")
ratio = (y_train==0).sum() / max((y_train==1).sum(), 1)
"""))
c.append(nbf.v4.new_code_cell("""# Train models
rf = RandomForestClassifier(class_weight='balanced', n_estimators=200, random_state=SEED)
rf.fit(X_train, y_train)

xgb = XGBClassifier(scale_pos_weight=ratio, eval_metric='auc', random_state=SEED, use_label_encoder=False)
xgb.fit(X_train, y_train)

for name, model in [('Random Forest', rf), ('XGBoost', xgb)]:
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]
    print(f"\\n{name}:")
    print(f"  Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"  F1: {f1_score(y_test, y_pred):.4f}")
    print(f"  ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
"""))
c.append(nbf.v4.new_code_cell("""# Generate escalation probability
df['escalation_probability'] = xgb.predict_proba(X)[:,1]
"""))
c.append(nbf.v4.new_code_cell("""# Plot a: Escalation rate overall
esc = df['escalation_flag'].value_counts().reset_index(); esc.columns=['flag','count']
esc['label'] = esc['flag'].map({0:'No Escalation',1:'Escalation'})
fig = px.pie(esc, values='count', names='label', hole=0.3,
             color_discrete_sequence=[SAFE, RISK], template=TEMPLATE, title='Escalation Rate')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot b: Escalation rate by category
esc_cat = df.groupby('complaint_category')['escalation_flag'].mean().sort_values(ascending=False).reset_index()
fig = px.bar(esc_cat, x='complaint_category', y='escalation_flag', color_discrete_sequence=[RISK],
             template=TEMPLATE, title='Escalation Rate by Category')
fig.update_xaxes(tickangle=45)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot c: Escalation rate by emotion
esc_emo = df.groupby('emotion')['escalation_flag'].mean().sort_values(ascending=False).reset_index()
fig = px.bar(esc_emo, x='emotion', y='escalation_flag', color_discrete_sequence=[WARNING],
             template=TEMPLATE, title='Escalation Rate by Emotion')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot d: Escalation probability histogram
fig = px.histogram(df, x='escalation_probability', nbins=30, color_discrete_sequence=[RISK],
                   template=TEMPLATE, title='Escalation Probability Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot e: ROC curves
fig = go.Figure()
for name, model, color in [('Random Forest', rf, PRIMARY), ('XGBoost', xgb, RISK)]:
    y_proba = model.predict_proba(X_test)[:,1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)
    fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f"{name} (AUC={auc:.3f})", line=dict(color=color)))
fig.add_trace(go.Scatter(x=[0,1], y=[0,1], name='Random', line=dict(dash='dash', color='gray')))
fig.update_layout(title='ROC Curves', xaxis_title='FPR', yaxis_title='TPR', template=TEMPLATE)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot f: Feature importance RF
imp = pd.DataFrame({'feature': feature_cols, 'importance': rf.feature_importances_})
imp = imp.sort_values('importance', ascending=True)
fig = px.bar(imp, y='feature', x='importance', orientation='h',
             color_discrete_sequence=[PRIMARY], template=TEMPLATE, title='Feature Importance - RF')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot g: Escalation by Product top 10
esc_prod = df.groupby('Product')['escalation_flag'].mean().sort_values(ascending=False).head(10).reset_index()
fig = px.bar(esc_prod, x='Product', y='escalation_flag', color_discrete_sequence=[WARNING],
             template=TEMPLATE, title='Escalation Rate by Product (Top 10)')
fig.update_xaxes(tickangle=45)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Save
os.makedirs('models/escalation', exist_ok=True)
joblib.dump(xgb, 'models/escalation/xgboost_escalation.pkl')
print("Saved escalation model")

df.to_csv('data/processed/complaints_with_escalation.csv', index=False)
print(f"Saved complaints_with_escalation.csv - shape: {df.shape}")
"""))
nb.cells = c
nbf.write(nb, 'notebooks/12_escalation_prediction.ipynb')
print("Created 12_escalation_prediction.ipynb")

# ═══════ NOTEBOOK 13 ═══════
nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 13 - Unified Customer Profile\nMerge segmentation, churn, and inactivity data into a 360-degree customer view."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np
import plotly.express as px
import warnings; warnings.filterwarnings('ignore')
SEED=42
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))
c.append(nbf.v4.new_code_cell("""# Load sources
segments = pd.read_csv('data/processed/customer_with_segments.csv')
print(f"Segments shape: {segments.shape}")
print(f"Columns: {list(segments.columns)}")

churn = pd.read_csv('data/processed/churn_predictions.csv')
print(f"\\nChurn shape: {churn.shape}")

inactivity = pd.read_csv('data/processed/inactivity_scores.csv')
print(f"\\nInactivity shape: {inactivity.shape}")
"""))
c.append(nbf.v4.new_code_cell("""# Merge
profile = segments.copy()
profile = profile.merge(churn[['CLIENTNUM','churn_probability']], on='CLIENTNUM', how='left')
profile = profile.merge(inactivity[['CLIENTNUM','activity_score','activity_category','future_churn_candidate']],
                        on='CLIENTNUM', how='left')
print(f"Merged profile shape: {profile.shape}")

# Derive churn_risk_label
def risk_label(p):
    \"\"\"Assign risk label from churn probability.\"\"\"
    if p >= 0.70: return 'High Risk'
    elif p >= 0.40: return 'Medium Risk'
    else: return 'Loyal'

profile['churn_risk_label'] = profile['churn_probability'].apply(risk_label)
"""))
c.append(nbf.v4.new_code_cell("""# Select final columns
final_cols = ['CLIENTNUM','Customer_Age','Gender','Income_Category','Card_Category',
              'Education_Level','Marital_Status','Credit_Limit','Total_Trans_Amt',
              'Total_Trans_Ct','Avg_Utilization_Ratio','Months_Inactive_12_mon',
              'segment_name','churn_probability','churn_risk_label',
              'activity_score','activity_category','future_churn_candidate']
available = [c for c in final_cols if c in profile.columns]
profile = profile[available]
print(f"Final profile columns ({len(available)}): {available}")
"""))
c.append(nbf.v4.new_code_cell("""# Summary statistics
print("=== Segment Distribution ===")
print(profile['segment_name'].value_counts())
print("\\n=== Mean Churn Probability by Segment ===")
print(profile.groupby('segment_name')['churn_probability'].mean().round(4))
print("\\n=== Mean Activity Score by Segment ===")
print(profile.groupby('segment_name')['activity_score'].mean().round(4))
print(f"\\nFuture churn candidates: {profile['future_churn_candidate'].sum()}")
"""))
c.append(nbf.v4.new_code_cell("""# Plot a: Segment donut
seg = profile['segment_name'].value_counts().reset_index(); seg.columns=['segment','count']
fig = px.pie(seg, values='count', names='segment', hole=0.4, template=TEMPLATE,
             title='Customer Segment Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot b: Mean churn by segment
churn_seg = profile.groupby('segment_name')['churn_probability'].mean().reset_index()
fig = px.bar(churn_seg, x='segment_name', y='churn_probability', color_discrete_sequence=[RISK],
             template=TEMPLATE, title='Mean Churn Probability by Segment')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot c: churn_risk_label pie
crl = profile['churn_risk_label'].value_counts().reset_index(); crl.columns=['label','count']
fig = px.pie(crl, values='count', names='label', hole=0.3,
             color='label', color_discrete_map={'High Risk':RISK,'Medium Risk':WARNING,'Loyal':SAFE},
             template=TEMPLATE, title='Churn Risk Label Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot d: activity_category bar
ac = profile['activity_category'].value_counts().reset_index(); ac.columns=['category','count']
fig = px.bar(ac, x='category', y='count', color='category',
             color_discrete_map={'Active':SAFE,'Moderately Active':NEUTRAL,'Inactive':WARNING,'High Risk':RISK},
             template=TEMPLATE, title='Activity Category Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot e: future_churn_candidate bar
fc = profile['future_churn_candidate'].value_counts().reset_index(); fc.columns=['candidate','count']
fc['candidate'] = fc['candidate'].map({True:'Yes',False:'No'})
fig = px.bar(fc, x='candidate', y='count', color='candidate',
             color_discrete_map={'Yes':RISK,'No':SAFE},
             template=TEMPLATE, title='Future Churn Candidates')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Null audit
print("Null counts per column:")
print(profile.isnull().sum())
"""))
c.append(nbf.v4.new_code_cell("""# Save
profile.to_csv('data/processed/unified_customer_profile.csv', index=False)
print(f"Saved unified_customer_profile.csv - shape: {profile.shape}")

# Overwrite customer_features.parquet
profile.to_parquet('data/features/customer_features.parquet', index=False)
print("Saved customer_features.parquet (overwritten)")
"""))
nb.cells = c
nbf.write(nb, 'notebooks/13_unified_customer_profile.ipynb')
print("Created 13_unified_customer_profile.ipynb")
