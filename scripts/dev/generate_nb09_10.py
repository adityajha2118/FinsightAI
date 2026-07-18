"""Generate notebooks 09 and 10"""
import nbformat as nbf

# ═══════ NOTEBOOK 09 ═══════
nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 09 - Campaign Prediction\nSMOTE-augmented ML pipeline for campaign conversion prediction."))
c.append(nbf.v4.new_markdown_cell("## Campaign ML -- Note on Data Size\nOriginal dataset: 100 rows. Standard train/test split not viable. Strategy: Apply SMOTE oversampling to reach 500+ balanced samples, then evaluate using StratifiedKFold (5 folds). All results represent cross-validated performance on synthetic-augmented data."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np, joblib, os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import plotly.express as px, plotly.graph_objects as go
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))
c.append(nbf.v4.new_code_cell("""df = pd.read_csv('data/processed/campaign_clean.csv')
print(f"Shape: {df.shape}")
# Feature engineering
df['contacted_before'] = (df['pdays'] != -1).astype(int)
df['campaign_intensity'] = df['campaign'] + df['previous']

# Encode categoricals
cat_cols = ['job','marital','education','default','housing','loan','contact','month','poutcome']
label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

target = 'y_binary'
if target not in df.columns:
    df[target] = (df['y'] == 'yes').astype(int)

feature_cols = [c for c in df.columns if c not in ['y', target, 'index']]
X = df[feature_cols].select_dtypes(include=[np.number])
y = df[target]
print(f"Features: {X.shape}, Target dist:\\n{y.value_counts()}")
"""))
c.append(nbf.v4.new_code_cell("""# SMOTE
smote = SMOTE(random_state=SEED)
X_res, y_res = smote.fit_resample(X, y)
print(f"Original shape: {X.shape}, Resampled: {X_res.shape}")
print(f"Resampled target dist:\\n{y_res.value_counts()}")
"""))
c.append(nbf.v4.new_code_cell("""# Cross-validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
models_cv = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=SEED),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=SEED),
    'XGBoost': XGBClassifier(n_estimators=100, random_state=SEED, eval_metric='auc', use_label_encoder=False)
}
cv_results = []
for name, model in models_cv.items():
    acc_scores = cross_val_score(model, X_res, y_res, cv=skf, scoring='accuracy')
    f1_scores = cross_val_score(model, X_res, y_res, cv=skf, scoring='f1')
    auc_scores = cross_val_score(model, X_res, y_res, cv=skf, scoring='roc_auc')
    print(f"{name}: Acc={acc_scores.mean():.4f}+/-{acc_scores.std():.4f}, "
          f"F1={f1_scores.mean():.4f}+/-{f1_scores.std():.4f}, "
          f"AUC={auc_scores.mean():.4f}+/-{auc_scores.std():.4f}")
    cv_results.append({'Model': name, 'Accuracy': acc_scores.mean(), 'F1': f1_scores.mean(),
                       'ROC-AUC': auc_scores.mean(), 'AUC_std': auc_scores.std()})

cv_df = pd.DataFrame(cv_results)
best_name = cv_df.loc[cv_df['ROC-AUC'].idxmax(), 'Model']
print(f"\\nBest model: {best_name}")
"""))
c.append(nbf.v4.new_code_cell("""# Fit best model on full resampled data
best_model = models_cv[best_name]
best_model.fit(X_res, y_res)
print(f"Best model ({best_name}) trained on full resampled data.")
"""))
c.append(nbf.v4.new_code_cell("""# Plot a: y distribution before/after SMOTE
before = y.value_counts().reset_index(); before.columns=['class','count']; before['stage']='Before SMOTE'
after = y_res.value_counts().reset_index(); after.columns=['class','count']; after['stage']='After SMOTE'
combined = pd.concat([before, after])
combined['class'] = combined['class'].astype(str)
fig = px.bar(combined, x='class', y='count', color='stage', barmode='group',
             color_discrete_sequence=[RISK, SAFE], template=TEMPLATE,
             title='Target Distribution: Before vs After SMOTE')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot b-d: Conversion rates
df_orig = pd.read_csv('data/processed/campaign_clean.csv')
if 'y_binary' not in df_orig.columns: df_orig['y_binary'] = (df_orig['y']=='yes').astype(int)

conv_job = df_orig.groupby('job')['y_binary'].mean().sort_values(ascending=True).reset_index()
fig = px.bar(conv_job, y='job', x='y_binary', orientation='h', color_discrete_sequence=[PRIMARY],
             template=TEMPLATE, title='Conversion Rate by Job')
fig.show()

conv_contact = df_orig.groupby('contact')['y_binary'].mean().reset_index()
fig = px.bar(conv_contact, x='contact', y='y_binary', color_discrete_sequence=[SAFE],
             template=TEMPLATE, title='Conversion Rate by Contact')
fig.show()

conv_month = df_orig.groupby('month')['y_binary'].mean().reset_index()
fig = px.bar(conv_month, x='month', y='y_binary', color_discrete_sequence=[WARNING],
             template=TEMPLATE, title='Conversion Rate by Month')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot e: campaign_intensity vs conversion
df_orig['campaign_intensity'] = df_orig['campaign'] + df_orig['previous']
ci = df_orig.groupby('campaign_intensity')['y_binary'].mean().reset_index()
fig = px.line(ci, x='campaign_intensity', y='y_binary', markers=True,
              color_discrete_sequence=[PRIMARY], template=TEMPLATE,
              title='Campaign Intensity vs Conversion Rate')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot f: Feature importance
if hasattr(best_model, 'feature_importances_'):
    imp = pd.DataFrame({'feature': X.columns, 'importance': best_model.feature_importances_})
    imp = imp.sort_values('importance', ascending=True).tail(15)
    fig = px.bar(imp, y='feature', x='importance', orientation='h',
                 color_discrete_sequence=[PRIMARY], template=TEMPLATE,
                 title=f'Feature Importance - {best_name}')
    fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Save
os.makedirs('models/campaign', exist_ok=True)
joblib.dump(best_model, 'models/campaign/xgboost_campaign.pkl')
print("Saved campaign model")

df[list(X.columns) + [target]].to_parquet('data/features/campaign_features.parquet', index=False)
print("Saved campaign_features.parquet")
"""))
nb.cells = c
nbf.write(nb, 'notebooks/09_campaign_prediction.ipynb')
print("Created 09_campaign_prediction.ipynb")

# ═══════ NOTEBOOK 10 ═══════
nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 10 - KYC Risk Prediction\nTrain RF and XGBoost to predict KYC/AML risk."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np, joblib, os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, classification_report
import plotly.express as px, plotly.graph_objects as go
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))
c.append(nbf.v4.new_code_cell("""df = pd.read_csv('data/processed/kyc_clean.csv')
print(f"Shape: {df.shape}")

# Encode sector_risk
sector_map = {'Low': 0, 'Medium': 1, 'High': 2}
df['sector_risk_encoded'] = df['sector_risk'].map(sector_map).fillna(0).astype(int)

# Fill nulls for flag columns
flag_cols = ['ofac_match_flag','fatf_txn_flag','structuring_pattern_flag',
             'rapid_movement_flag','trade_mispricing_flag','pep_flag',
             'sanctions_flag','fatf_entity_flag','ofac_country_flag',
             'sectoral_sanctions_flag','ownership_opacity_score']
for col in flag_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# Target engineering
df['kyc_risk_score'] = (
    0.25 * df['pep_flag'].fillna(0) +
    0.25 * df['sanctions_flag'].fillna(0) +
    0.15 * df['ofac_match_flag'].fillna(0) +
    0.10 * df['structuring_pattern_flag'].fillna(0) +
    0.10 * df['rapid_movement_flag'].fillna(0) +
    0.05 * df['trade_mispricing_flag'].fillna(0) +
    0.05 * df['fatf_txn_flag'].fillna(0) +
    0.05 * df['ownership_opacity_score'].fillna(0)
)
threshold = df['kyc_risk_score'].quantile(0.75)
df['kyc_risk_flag'] = (df['kyc_risk_score'] > threshold).astype(int)
print(f"Threshold: {threshold:.4f}")
print(f"Flag distribution:\\n{df['kyc_risk_flag'].value_counts()}")
"""))
c.append(nbf.v4.new_code_cell("""# Features and split
feature_cols = flag_cols + ['sector_risk_encoded']
feature_cols = [c for c in feature_cols if c in df.columns]
X = df[feature_cols]
y = df['kyc_risk_flag']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")
ratio = (y_train==0).sum() / (y_train==1).sum()
print(f"Scale pos weight: {ratio:.2f}")
"""))
c.append(nbf.v4.new_code_cell("""# Train models
rf = RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=SEED, n_jobs=-1)
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
    print(classification_report(y_test, y_pred))
"""))
c.append(nbf.v4.new_code_cell("""# Assign risk_level using best model (XGBoost)
best_model = xgb
proba = best_model.predict_proba(X)[:,1]
def risk_level(p):
    \"\"\"Assign risk level from probability.\"\"\"
    if p > 0.75: return 'Critical'
    elif p > 0.50: return 'High Risk'
    elif p > 0.25: return 'Medium Risk'
    else: return 'Low Risk'
df['risk_level'] = pd.Series(proba).apply(risk_level)
print("Risk level distribution:")
print(df['risk_level'].value_counts())
"""))
c.append(nbf.v4.new_code_cell("""# Plot a: risk_level donut
rl = df['risk_level'].value_counts().reset_index(); rl.columns=['level','count']
fig = px.pie(rl, values='count', names='level', hole=0.4,
             color='level', color_discrete_map={'Critical':RISK,'High Risk':WARNING,'Medium Risk':NEUTRAL,'Low Risk':SAFE},
             template=TEMPLATE, title='KYC Risk Level Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot b: sector_risk vs kyc_risk_flag
ct = df.groupby(['sector_risk','kyc_risk_flag']).size().reset_index(name='count')
ct['kyc_risk_flag'] = ct['kyc_risk_flag'].map({0:'Low Risk',1:'High Risk'})
fig = px.bar(ct, x='sector_risk', y='count', color='kyc_risk_flag', barmode='group',
             color_discrete_map={'Low Risk':SAFE,'High Risk':RISK},
             template=TEMPLATE, title='Sector Risk vs KYC Risk Flag')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot c: pep_flag vs sanctions_flag
ct = df.groupby(['pep_flag','sanctions_flag']).size().reset_index(name='count')
ct['pep_flag'] = ct['pep_flag'].astype(str)
ct['sanctions_flag'] = ct['sanctions_flag'].astype(str)
fig = px.bar(ct, x='pep_flag', y='count', color='sanctions_flag', barmode='stack',
             template=TEMPLATE, title='PEP Flag vs Sanctions Flag Co-occurrence')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot d-e: structuring + opacity
v = df['structuring_pattern_flag'].value_counts().reset_index(); v.columns=['flag','count']
fig = px.bar(v, x='flag', y='count', color_discrete_sequence=[NEUTRAL], template=TEMPLATE, title='Structuring Pattern Flag')
fig.show()

fig = px.box(df.dropna(subset=['ownership_opacity_score']), x='risk_level', y='ownership_opacity_score',
             color='risk_level', color_discrete_map={'Critical':RISK,'High Risk':WARNING,'Medium Risk':NEUTRAL,'Low Risk':SAFE},
             template=TEMPLATE, title='Ownership Opacity Score by Risk Level')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot f: ROC curves
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
c.append(nbf.v4.new_code_cell("""# Plot g: Feature importance RF
imp = pd.DataFrame({'feature': feature_cols, 'importance': rf.feature_importances_})
imp = imp.sort_values('importance', ascending=True)
fig = px.bar(imp, y='feature', x='importance', orientation='h',
             color_discrete_sequence=[PRIMARY], template=TEMPLATE, title='Feature Importance - Random Forest')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot h: Top 15 client_country by high risk
if 'client_country' in df.columns:
    hr_country = df[df['kyc_risk_flag']==1]['client_country'].value_counts().head(15).reset_index()
    hr_country.columns = ['country','count']
    fig = px.bar(hr_country, x='country', y='count', color_discrete_sequence=[RISK],
                 template=TEMPLATE, title='Top 15 Client Countries by High Risk Count')
    fig.update_xaxes(tickangle=45)
    fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Save
os.makedirs('models/kyc', exist_ok=True)
joblib.dump(rf, 'models/kyc/random_forest_kyc.pkl')
joblib.dump(xgb, 'models/kyc/xgboost_kyc.pkl')
print("Saved KYC models")

save_cols = ['client_id','kyc_risk_score','risk_level'] + feature_cols
df[save_cols].to_parquet('data/features/kyc_features.parquet', index=False)
print("Saved kyc_features.parquet")
"""))
nb.cells = c
nbf.write(nb, 'notebooks/10_kyc_risk_prediction.ipynb')
print("Created 10_kyc_risk_prediction.ipynb")
