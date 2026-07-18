"""Generate notebook 02_transaction_eda.ipynb"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell("# 02 — Transaction & Fraud EDA\nExploratory analysis of credit card transactions dataset (1.29M rows)."))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

SEED = 42
np.random.seed(SEED)

PRIMARY  = '#635BFF'
RISK     = '#E74C3C'
SAFE     = '#27AE60'
NEUTRAL  = '#3498DB'
WARNING  = '#F39C12'
TEMPLATE = 'plotly_white'
"""))

cells.append(nbf.v4.new_code_cell("""# Load raw data
df = pd.read_csv('data/raw/transactions/transactions.csv')
print(f"Shape: {df.shape}")
df.head()
"""))

cells.append(nbf.v4.new_code_cell("""# Preprocessing
df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
df['trans_month'] = df['trans_date_trans_time'].dt.month
df['trans_hour']  = df['trans_date_trans_time'].dt.hour
df['trans_day']   = df['trans_date_trans_time'].dt.dayofweek
df['merch_zipcode'] = df['merch_zipcode'].fillna(0)
df = df.drop(columns=['cc_num','trans_num','unix_time'], errors='ignore')
print(f"Shape after preprocessing: {df.shape}")
"""))

cells.append(nbf.v4.new_code_cell("""# Shape, dtypes, null counts
print("Dtypes:\\n", df.dtypes)
print("\\nNull counts:\\n", df.isnull().sum())
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 1: Transaction amount histogram + box plot
fig = make_subplots(rows=1, cols=2, subplot_titles=('Amount Histogram','Amount Box Plot'))
fig.add_trace(go.Histogram(x=df['amt'], nbinsx=50, marker_color=PRIMARY), row=1, col=1)
fig.add_trace(go.Box(y=df['amt'], marker_color=PRIMARY), row=1, col=2)
fig.update_layout(title='Transaction Amount Distribution', template=TEMPLATE, showlegend=False)
fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 2: Fraud vs legitimate
counts = df['is_fraud'].value_counts().reset_index()
counts.columns = ['is_fraud','count']
counts['label'] = counts['is_fraud'].map({0:'Legitimate', 1:'Fraud'})
counts['pct'] = (counts['count'] / counts['count'].sum() * 100).round(2)
fig = px.bar(counts, x='label', y='count', text='pct', color='label',
             color_discrete_map={'Legitimate': SAFE, 'Fraud': RISK},
             template=TEMPLATE, title='Fraud vs Legitimate Transactions')
fig.update_traces(texttemplate='%{text}%', textposition='outside')
fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 3: Mean amt by category (top 15)
cat_amt = df.groupby('category')['amt'].mean().sort_values(ascending=True).tail(15).reset_index()
fig = px.bar(cat_amt, y='category', x='amt', orientation='h', color_discrete_sequence=[PRIMARY],
             template=TEMPLATE, title='Mean Transaction Amount by Category (Top 15)')
fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 4: Top 15 merchants by fraud count
fraud_merch = df[df['is_fraud']==1].groupby('merchant').size().sort_values(ascending=False).head(15).reset_index(name='fraud_count')
fig = px.bar(fraud_merch, x='merchant', y='fraud_count', color_discrete_sequence=[RISK],
             template=TEMPLATE, title='Top 15 Merchants by Fraud Count')
fig.update_xaxes(tickangle=45)
fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 5: Transactions per month
monthly = df.groupby('trans_month').size().reset_index(name='count')
fig = px.line(monthly, x='trans_month', y='count', markers=True, color_discrete_sequence=[PRIMARY],
              template=TEMPLATE, title='Transactions per Month')
fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 6: Transactions per hour of day
hourly = df.groupby('trans_hour').size().reset_index(name='count')
fig = px.bar(hourly, x='trans_hour', y='count', color_discrete_sequence=[NEUTRAL],
             template=TEMPLATE, title='Transactions per Hour of Day')
fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 7: Fraud amt distribution vs legitimate — overlaid histogram
fig = go.Figure()
fig.add_trace(go.Histogram(x=df[df['is_fraud']==0]['amt'], name='Legitimate', marker_color=SAFE, opacity=0.6, nbinsx=50))
fig.add_trace(go.Histogram(x=df[df['is_fraud']==1]['amt'], name='Fraud', marker_color=RISK, opacity=0.6, nbinsx=50))
fig.update_layout(barmode='overlay', template=TEMPLATE, title='Amount Distribution: Fraud vs Legitimate')
fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 8: Fraud rate by category
fraud_rate = df.groupby('category').agg(total=('is_fraud','count'), fraud=('is_fraud','sum')).reset_index()
fraud_rate['rate'] = (fraud_rate['fraud'] / fraud_rate['total'] * 100).round(2)
fraud_rate = fraud_rate.sort_values('rate', ascending=False)
fig = px.bar(fraud_rate, x='category', y='rate', color_discrete_sequence=[RISK],
             template=TEMPLATE, title='Fraud Rate by Category (%)')
fig.update_xaxes(tickangle=45)
fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 9: Gender distribution — pie
gen = df['gender'].value_counts().reset_index()
gen.columns = ['gender','count']
fig = px.pie(gen, values='count', names='gender', color_discrete_sequence=[PRIMARY, WARNING],
             template=TEMPLATE, title='Gender Distribution', hole=0.3)
fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 10: Top 15 cities by transaction count
if 'city' in df.columns:
    city_counts = df['city'].value_counts().head(15).reset_index()
    city_counts.columns = ['city','count']
    fig = px.bar(city_counts, x='city', y='count', color_discrete_sequence=[NEUTRAL],
                 template=TEMPLATE, title='Top 15 Cities by Transaction Count')
    fig.update_xaxes(tickangle=45)
    fig.show()
"""))

cells.append(nbf.v4.new_code_cell("""# Plot 11: Correlation heatmap
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
corr = df[numeric_cols].corr()
fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                template=TEMPLATE, title='Correlation Heatmap — Numeric Columns',
                width=900, height=800)
fig.show()
"""))

for insight in [
    "### Insight 1: Fraud Class Imbalance\nFraud transactions represent a tiny fraction of total volume. Any ML model must address this extreme imbalance through sampling or class weighting.",
    "### Insight 2: Category Risk\nCertain merchant categories show disproportionately higher fraud rates. These categories should receive enhanced monitoring in real-time fraud detection systems.",
    "### Insight 3: Temporal Patterns\nTransaction volume peaks during certain hours. Fraud patterns may exploit off-peak hours when monitoring may be less vigilant.",
    "### Insight 4: Amount Thresholds\nFraudulent transactions tend toward higher amounts. Amount-based thresholds combined with category flags could form effective rule-based filters.",
    "### Insight 5: Geographic Concentration\nTransaction volume concentrates in specific cities/regions. Geographic anomaly detection could flag out-of-pattern transactions.",
]:
    cells.append(nbf.v4.new_markdown_cell(insight))

cells.append(nbf.v4.new_code_cell("""# Save cleaned data
df.to_csv('data/processed/transaction_clean.csv', index=False)
print(f"Saved transaction_clean.csv — shape: {df.shape}")
"""))

nb.cells = cells
nbf.write(nb, 'notebooks/02_transaction_eda.ipynb')
print("Created 02_transaction_eda.ipynb")
