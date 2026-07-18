"""Generate notebook 07_inactivity_detection.ipynb"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 07 - Inactivity Detection\nPart A: Activity scoring from customer data. Part B: Bank transactions standalone analysis."))

c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np, joblib
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))

# PART A
c.append(nbf.v4.new_markdown_cell("## Part A: Inactivity Scoring from Customer Data"))
c.append(nbf.v4.new_code_cell("""df = pd.read_csv('data/processed/customer_clean.csv')
print(f"Shape: {df.shape}")
cols_used = ['CLIENTNUM','Months_Inactive_12_mon','Total_Trans_Ct','Total_Trans_Amt','Total_Revolving_Bal','Avg_Utilization_Ratio']
print("Using columns:", cols_used)
"""))
c.append(nbf.v4.new_code_cell("""def minmax(s):
    \"\"\"Min-max normalize a pandas Series.\"\"\"
    return (s - s.min()) / (s.max() - s.min())

df['norm_trans_ct']    = minmax(df['Total_Trans_Ct'])
df['norm_trans_amt']   = minmax(df['Total_Trans_Amt'])
df['norm_revolving']   = minmax(df['Total_Revolving_Bal'])
df['norm_utilization'] = minmax(df['Avg_Utilization_Ratio'])
df['norm_inactivity']  = minmax(df['Months_Inactive_12_mon'])

df['activity_score'] = (
    0.30 * (1 - df['norm_inactivity']) +
    0.30 * df['norm_trans_ct'] +
    0.20 * df['norm_trans_amt'] +
    0.10 * df['norm_revolving'] +
    0.10 * df['norm_utilization']
)

def assign_category(score):
    \"\"\"Assign activity category based on score thresholds.\"\"\"
    if score >= 0.70: return "Active"
    elif score >= 0.40: return "Moderately Active"
    elif score >= 0.20: return "Inactive"
    else: return "High Risk"

df['activity_category'] = df['activity_score'].apply(assign_category)
df['future_churn_candidate'] = (
    (df['Months_Inactive_12_mon'] >= 3) &
    (df['Avg_Utilization_Ratio'] < 0.15)
)

print("Activity category distribution:")
print(df['activity_category'].value_counts())
print(f"\\nFuture churn candidates: {df['future_churn_candidate'].sum()}")
"""))
c.append(nbf.v4.new_code_cell("""# Plot A1: activity_category distribution
cat_counts = df['activity_category'].value_counts().reset_index()
cat_counts.columns = ['category','count']
fig = px.bar(cat_counts, x='category', y='count', color='category',
             color_discrete_map={'Active':SAFE,'Moderately Active':NEUTRAL,'Inactive':WARNING,'High Risk':RISK},
             template=TEMPLATE, title='Activity Category Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot A2: activity_score histogram
fig = px.histogram(df, x='activity_score', nbins=40, color_discrete_sequence=[PRIMARY],
                   template=TEMPLATE, title='Activity Score Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot A3: Future churn candidate count
fc = df['future_churn_candidate'].value_counts().reset_index()
fc.columns = ['candidate','count']
fc['candidate'] = fc['candidate'].map({True:'Yes',False:'No'})
fig = px.bar(fc, x='candidate', y='count', color='candidate',
             color_discrete_map={'Yes':RISK,'No':SAFE},
             template=TEMPLATE, title='Future Churn Candidates')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot A4: Months_Inactive vs activity_score scatter
fig = px.scatter(df.sample(2000, random_state=SEED), x='Months_Inactive_12_mon', y='activity_score',
                 color='activity_category',
                 color_discrete_map={'Active':SAFE,'Moderately Active':NEUTRAL,'Inactive':WARNING,'High Risk':RISK},
                 template=TEMPLATE, title='Inactivity Months vs Activity Score', opacity=0.6)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot A5: activity_category vs churn
if 'Attrition_Flag' in df.columns:
    ct = df.groupby(['activity_category','Attrition_Flag']).size().reset_index(name='count')
    fig = px.bar(ct, x='activity_category', y='count', color='Attrition_Flag', barmode='group',
                 color_discrete_map={'Existing Customer':SAFE,'Attrited Customer':RISK},
                 template=TEMPLATE, title='Activity Category vs Churn Status')
    fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Save Part A
inactivity_df = df[['CLIENTNUM','activity_score','activity_category','future_churn_candidate']]
inactivity_df.to_csv('data/processed/inactivity_scores.csv', index=False)
print(f"Saved inactivity_scores.csv - shape: {inactivity_df.shape}")

# Save scaler as model
import os; os.makedirs('models/inactivity', exist_ok=True)
mms = MinMaxScaler()
mms.fit(df[['Total_Trans_Ct','Total_Trans_Amt','Total_Revolving_Bal','Avg_Utilization_Ratio','Months_Inactive_12_mon']])
joblib.dump(mms, 'models/inactivity/activity_scorer.pkl')
print("Saved activity_scorer.pkl")
"""))

# PART B
c.append(nbf.v4.new_markdown_cell("## Part B: Bank Transactions Standalone Analysis"))
c.append(nbf.v4.new_code_cell("""btx = pd.read_csv('data/raw/bank_transactions/bank_transactions.csv')
print(f"Shape: {btx.shape}")
btx['TransactionDate'] = pd.to_datetime(btx['TransactionDate'])
btx['PreviousTransactionDate'] = pd.to_datetime(btx['PreviousTransactionDate'])
print(btx.dtypes)
"""))
c.append(nbf.v4.new_code_cell("""# Compute per-account stats
latest_date = btx['TransactionDate'].max()
account_stats = btx.groupby('AccountID').agg(
    last_transaction=('TransactionDate','max'),
    avg_amount=('TransactionAmount','mean'),
    total_transactions=('TransactionID','count'),
    avg_balance=('AccountBalance','mean'),
    avg_login_attempts=('LoginAttempts','mean')
).reset_index()
account_stats['days_since_last'] = (latest_date - account_stats['last_transaction']).dt.days
account_stats['high_risk_account'] = account_stats['days_since_last'] > 60
print(f"Account stats shape: {account_stats.shape}")
print(f"High risk accounts: {account_stats['high_risk_account'].sum()}")
"""))
c.append(nbf.v4.new_code_cell("""# Plot B1-B2: TransactionAmount + AccountBalance histograms
fig = px.histogram(btx, x='TransactionAmount', nbins=40, color_discrete_sequence=[PRIMARY],
                   template=TEMPLATE, title='Transaction Amount Distribution')
fig.show()
fig = px.histogram(btx, x='AccountBalance', nbins=40, color_discrete_sequence=[NEUTRAL],
                   template=TEMPLATE, title='Account Balance Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot B3: TransactionType — pie
tt = btx['TransactionType'].value_counts().reset_index(); tt.columns=['type','count']
fig = px.pie(tt, values='count', names='type', title='Transaction Type', hole=0.3,
             color_discrete_sequence=[PRIMARY, WARNING], template=TEMPLATE)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot B4: Channel distribution
ch = btx['Channel'].value_counts().reset_index(); ch.columns=['channel','count']
fig = px.bar(ch, x='channel', y='count', color_discrete_sequence=[NEUTRAL],
             template=TEMPLATE, title='Channel Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot B5-B6: LoginAttempts + TransactionDuration
la = btx['LoginAttempts'].value_counts().sort_index().reset_index(); la.columns=['attempts','count']
fig = px.bar(la, x='attempts', y='count', color_discrete_sequence=[WARNING],
             template=TEMPLATE, title='Login Attempts Distribution')
fig.show()
fig = px.histogram(btx, x='TransactionDuration', nbins=30, color_discrete_sequence=[PRIMARY],
                   template=TEMPLATE, title='Transaction Duration Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot B7-B8: Occupation + Age
occ = btx['CustomerOccupation'].value_counts().head(10).reset_index(); occ.columns=['occupation','count']
fig = px.bar(occ, x='occupation', y='count', color_discrete_sequence=[NEUTRAL],
             template=TEMPLATE, title='Top 10 Customer Occupations')
fig.show()
fig = px.histogram(btx, x='CustomerAge', nbins=20, color_discrete_sequence=[PRIMARY],
                   template=TEMPLATE, title='Customer Age Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot B9-B10: days_since_last + high_risk
fig = px.histogram(account_stats, x='days_since_last', nbins=30, color_discrete_sequence=[WARNING],
                   template=TEMPLATE, title='Days Since Last Transaction')
fig.show()
hr = account_stats['high_risk_account'].value_counts().reset_index(); hr.columns=['high_risk','count']
hr['high_risk'] = hr['high_risk'].map({True:'High Risk',False:'Normal'})
fig = px.bar(hr, x='high_risk', y='count', color='high_risk',
             color_discrete_map={'High Risk':RISK,'Normal':SAFE},
             template=TEMPLATE, title='High Risk Account Count')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Save Part B
account_stats.to_csv('data/processed/bank_tx_activity.csv', index=False)
print(f"Saved bank_tx_activity.csv - shape: {account_stats.shape}")
"""))

nb.cells = c
nbf.write(nb, 'notebooks/07_inactivity_detection.ipynb')
print("Created 07_inactivity_detection.ipynb")
