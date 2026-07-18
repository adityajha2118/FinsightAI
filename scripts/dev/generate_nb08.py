"""Generate notebook 08_churn_prediction.ipynb"""
import nbformat as nbf
nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 08 - Churn Prediction\nTrain LR, RF, and XGBoost models to predict customer churn."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np, joblib, os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix, roc_curve
import plotly.express as px, plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))
c.append(nbf.v4.new_code_cell("""df = pd.read_csv('data/processed/customer_clean.csv')
df = df[[col for col in df.columns if 'Naive_Bayes' not in col]]
df['churn_label'] = (df['Attrition_Flag'] == 'Attrited Customer').astype(int)
print(f"Shape: {df.shape}")
print(f"Churn distribution:\\n{df['churn_label'].value_counts()}")
"""))
c.append(nbf.v4.new_code_cell("""# Encode categoricals
cat_cols = ['Income_Category','Card_Category','Gender','Education_Level','Marital_Status']
label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

numeric_features = ['Customer_Age','Dependent_count','Months_on_book',
    'Months_Inactive_12_mon','Contacts_Count_12_mon','Credit_Limit',
    'Total_Revolving_Bal','Avg_Open_To_Buy','Total_Amt_Chng_Q4_Q1',
    'Total_Trans_Amt','Total_Trans_Ct','Total_Ct_Chng_Q4_Q1','Avg_Utilization_Ratio']
all_features = numeric_features + cat_cols

X = df[all_features]
y = df['churn_label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")
"""))
c.append(nbf.v4.new_code_cell("""# Train models
models = {}
# Logistic Regression
lr = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=SEED, solver='lbfgs')
lr.fit(X_train, y_train)
models['Logistic Regression'] = lr

# Random Forest
rf = RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=SEED, n_jobs=-1)
rf.fit(X_train, y_train)
models['Random Forest'] = rf

# XGBoost
scale_pos = (y==0).sum() / (y==1).sum()
xgb = XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.05,
                     scale_pos_weight=scale_pos, eval_metric='auc',
                     random_state=SEED, use_label_encoder=False)
xgb.fit(X_train, y_train)
models['XGBoost'] = xgb
print("All models trained.")
"""))
c.append(nbf.v4.new_code_cell("""# Evaluate models
results = []
for name, model in models.items():
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    results.append({'Model': name, 'Accuracy': acc, 'Precision': prec,
                    'Recall': rec, 'F1': f1, 'ROC-AUC': auc})
    print(f"\\n{name}:")
    print(classification_report(y_test, y_pred))

results_df = pd.DataFrame(results)
print("\\n=== Model Comparison ===")
print(results_df.round(4))
best_model_name = results_df.loc[results_df['ROC-AUC'].idxmax(), 'Model']
print(f"\\nBest model by ROC-AUC: {best_model_name}")
"""))
c.append(nbf.v4.new_code_cell("""# Plot a: ROC curves
fig = go.Figure()
colors = [PRIMARY, SAFE, RISK]
for i, (name, model) in enumerate(models.items()):
    y_proba = model.predict_proba(X_test)[:,1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)
    fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f"{name} (AUC={auc:.3f})", line=dict(color=colors[i])))
fig.add_trace(go.Scatter(x=[0,1], y=[0,1], name='Random', line=dict(dash='dash', color='gray')))
fig.update_layout(title='ROC Curves', xaxis_title='FPR', yaxis_title='TPR', template=TEMPLATE)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot b: Confusion matrix (best model)
best_model = models[best_model_name]
cm = confusion_matrix(y_test, best_model.predict(X_test))
fig = px.imshow(cm, text_auto=True, color_continuous_scale='Blues',
                labels=dict(x='Predicted', y='Actual'),
                x=['Existing','Attrited'], y=['Existing','Attrited'],
                template=TEMPLATE, title=f'Confusion Matrix - {best_model_name}')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot c-d: Feature importance RF + XGB
for name, model in [('Random Forest', rf), ('XGBoost', xgb)]:
    imp = pd.DataFrame({'feature': all_features, 'importance': model.feature_importances_})
    imp = imp.sort_values('importance', ascending=True).tail(15)
    fig = px.bar(imp, y='feature', x='importance', orientation='h',
                 color_discrete_sequence=[PRIMARY if name=='Random Forest' else RISK],
                 template=TEMPLATE, title=f'Feature Importance - {name} (Top 15)')
    fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot e: Churn probability distribution
xgb_proba = xgb.predict_proba(X[all_features])[:,1]
fig = px.histogram(x=xgb_proba, nbins=50, color_discrete_sequence=[RISK],
                   template=TEMPLATE, title='Churn Probability Distribution (XGBoost)',
                   labels={'x':'Probability','y':'Count'})
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot f-i: Churn rate breakdowns
df_orig = pd.read_csv('data/processed/customer_clean.csv')
df_orig['churn_label'] = (df_orig['Attrition_Flag'] == 'Attrited Customer').astype(int)

for col, title in [('Card_Category','Churn Rate by Card Category'),
                   ('Income_Category','Churn Rate by Income Category'),
                   ('Gender','Churn Rate by Gender')]:
    cr = df_orig.groupby(col)['churn_label'].mean().reset_index()
    cr.columns = [col, 'churn_rate']
    fig = px.bar(cr, x=col, y='churn_rate', color_discrete_sequence=[RISK],
                 template=TEMPLATE, title=title)
    fig.show()

# Months_Inactive binned vs churn rate
df_orig['inactive_bin'] = pd.cut(df_orig['Months_Inactive_12_mon'], bins=7)
bin_churn = df_orig.groupby('inactive_bin', observed=True)['churn_label'].mean().reset_index()
bin_churn['inactive_bin'] = bin_churn['inactive_bin'].astype(str)
fig = px.line(bin_churn, x='inactive_bin', y='churn_label', markers=True,
              color_discrete_sequence=[RISK], template=TEMPLATE,
              title='Churn Rate by Months Inactive (binned)')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Add churn_probability and save
df['churn_probability'] = xgb_proba
os.makedirs('models/churn', exist_ok=True)
joblib.dump(lr, 'models/churn/logistic_regression.pkl')
joblib.dump(rf, 'models/churn/random_forest.pkl')
joblib.dump(xgb, 'models/churn/xgboost_model.pkl')
print("Saved all churn models")

save_cols = ['CLIENTNUM','churn_probability'] + all_features
df[save_cols].to_csv('data/processed/churn_predictions.csv', index=False)
print(f"Saved churn_predictions.csv - shape: {df[save_cols].shape}")
"""))
nb.cells = c
nbf.write(nb, 'notebooks/08_churn_prediction.ipynb')
print("Created 08_churn_prediction.ipynb")
