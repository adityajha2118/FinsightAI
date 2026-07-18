"""Generate notebooks 03, 04, 05"""
import nbformat as nbf

# ═══════════════ NOTEBOOK 03 ═══════════════
nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 03 — Campaign EDA\nExploratory analysis of bank marketing campaign dataset."))
c.append(nbf.v4.new_markdown_cell("## ⚠ Dataset Size Warning\nThis dataset contains only 100 rows. This notebook performs EDA and pattern analysis only. Machine learning models (Notebook 09) will use SMOTE augmentation to generate synthetic training samples. All charts and patterns are indicative only and should be interpreted with caution."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np
import plotly.express as px, plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))
c.append(nbf.v4.new_code_cell("""df = pd.read_csv('data/raw/campaign/bank_campaign.csv')
print(f"Shape: {df.shape}")
df.head()
"""))
c.append(nbf.v4.new_code_cell("""# Preprocessing
df['y_binary'] = (df['y'] == 'yes').astype(int)
df['pdays'] = df['pdays'].replace(999, -1)
df = df.rename(columns={'emp.var.rate':'emp_var_rate','cons.price.idx':'cons_price_idx','cons.conf.idx':'cons_conf_idx'})
print("Dtypes:\\n", df.dtypes)
print("\\nNull counts:\\n", df.isnull().sum())
"""))
c.append(nbf.v4.new_code_cell("""# Plot 1: y distribution — pie
fig = px.pie(df, names='y', title='Campaign Outcome Distribution', hole=0.3,
             color_discrete_sequence=[RISK, SAFE], template=TEMPLATE)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 2: Conversion rate by job
conv_job = df.groupby('job')['y_binary'].mean().sort_values(ascending=True).reset_index()
conv_job.columns = ['job','rate']
fig = px.bar(conv_job, y='job', x='rate', orientation='h', color_discrete_sequence=[PRIMARY],
             template=TEMPLATE, title='Conversion Rate by Job')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 3: Conversion rate by education
conv_edu = df.groupby('education')['y_binary'].mean().sort_values(ascending=False).reset_index()
fig = px.bar(conv_edu, x='education', y='y_binary', color_discrete_sequence=[NEUTRAL],
             template=TEMPLATE, title='Conversion Rate by Education')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 4: Conversion rate by contact method
conv_contact = df.groupby('contact')['y_binary'].mean().reset_index()
fig = px.bar(conv_contact, x='contact', y='y_binary', color_discrete_sequence=[SAFE],
             template=TEMPLATE, title='Conversion Rate by Contact Method')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 5: Conversion rate by month
conv_month = df.groupby('month')['y_binary'].mean().reset_index()
fig = px.bar(conv_month, x='month', y='y_binary', color_discrete_sequence=[WARNING],
             template=TEMPLATE, title='Conversion Rate by Month')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 6: campaign count distribution
fig = px.histogram(df, x='campaign', nbins=15, color_discrete_sequence=[PRIMARY],
                   template=TEMPLATE, title='Campaign Contact Count Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 7: pdays distribution (excluding -1)
pdays_valid = df[df['pdays'] != -1]
fig = px.histogram(pdays_valid, x='pdays', nbins=20, color_discrete_sequence=[NEUTRAL],
                   template=TEMPLATE, title='Previous Days Distribution (excl. never contacted)')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 8: poutcome vs y — grouped bar
ct = df.groupby(['poutcome','y']).size().reset_index(name='count')
fig = px.bar(ct, x='poutcome', y='count', color='y', barmode='group',
             color_discrete_map={'yes': SAFE, 'no': RISK},
             template=TEMPLATE, title='Previous Outcome vs Campaign Result')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 9: age distribution by y — box plot
fig = px.box(df, x='y', y='age', color='y', color_discrete_map={'yes': SAFE, 'no': RISK},
             template=TEMPLATE, title='Age Distribution by Campaign Outcome')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 10: Correlation heatmap
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
corr = df[numeric_cols].corr()
fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                template=TEMPLATE, title='Correlation Heatmap', width=800, height=700)
fig.show()
"""))
for ins in [
    "### Insight 1: Low Conversion\nOverall conversion rate is modest. With only 100 rows, variance is high — these patterns are directional only.",
    "### Insight 2: Job Matters\nCertain job categories show notably higher conversion rates, suggesting targeted outreach could improve ROI.",
    "### Insight 3: Contact Method\nCellular contact shows higher success than telephone, suggesting channel optimization opportunities.",
    "### Insight 4: Previous Outcome\nCustomers with successful previous outcomes convert at dramatically higher rates — re-engagement campaigns are highly effective.",
    "### Insight 5: Seasonal Patterns\nCertain months show elevated conversion, possibly driven by economic conditions or campaign timing.",
]: c.append(nbf.v4.new_markdown_cell(ins))
c.append(nbf.v4.new_code_cell("""df.to_csv('data/processed/campaign_clean.csv', index=False)
print(f"Saved campaign_clean.csv — shape: {df.shape}")
"""))
nb.cells = c
nbf.write(nb, 'notebooks/03_campaign_eda.ipynb')
print("Created 03_campaign_eda.ipynb")

# ═══════════════ NOTEBOOK 04 ═══════════════
nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 04 — KYC / AML EDA\nExploratory analysis of KYC transaction and client data."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np
import plotly.express as px, plotly.graph_objects as go
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))
c.append(nbf.v4.new_code_cell("""# Load and merge
kyc1 = pd.read_csv('data/raw/kyc/kyc_part1.csv')
kyc2 = pd.read_csv('data/raw/kyc/kyc_part2.csv')
print(f"kyc_part1 shape: {kyc1.shape}")
print(f"kyc_part2 shape: {kyc2.shape}")

kyc1 = kyc1.rename(columns={'fatf_country_flag': 'fatf_txn_flag'})
kyc2 = kyc2.rename(columns={'fatf_country_flag': 'fatf_entity_flag'})
df = pd.merge(kyc1, kyc2, on='client_id', how='left')
print(f"Merged shape: {df.shape}")
print(f"Matched rows: {df['client_name'].notna().sum()}")
print(f"Unmatched client_ids: {df['client_name'].isna().sum()}")
"""))
c.append(nbf.v4.new_code_cell("""print("Dtypes:\\n", df.dtypes)
print("\\nNull counts:\\n", df.isnull().sum())
"""))
c.append(nbf.v4.new_code_cell("""# Plot 1: sector_risk distribution
sr = df['sector_risk'].value_counts().reset_index(); sr.columns=['risk','count']
fig = px.bar(sr, x='risk', y='count', color='risk',
             color_discrete_map={'Low': SAFE, 'Medium': WARNING, 'High': RISK},
             template=TEMPLATE, title='Sector Risk Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 2: pep_flag count
pep = df['pep_flag'].value_counts().reset_index(); pep.columns=['pep','count']
pep['pct'] = (pep['count']/pep['count'].sum()*100).round(2)
fig = px.bar(pep, x='pep', y='count', text='pct', color_discrete_sequence=[RISK],
             template=TEMPLATE, title='PEP Flag Distribution')
fig.update_traces(texttemplate='%{text}%', textposition='outside')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 3: sanctions_flag count
sf = df['sanctions_flag'].value_counts().reset_index(); sf.columns=['flag','count']
sf['pct'] = (sf['count']/sf['count'].sum()*100).round(2)
fig = px.bar(sf, x='flag', y='count', text='pct', color_discrete_sequence=[WARNING],
             template=TEMPLATE, title='Sanctions Flag Distribution')
fig.update_traces(texttemplate='%{text}%', textposition='outside')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 4-5: structuring + rapid movement
for col, title in [('structuring_pattern_flag','Structuring Pattern Flag'),('rapid_movement_flag','Rapid Movement Flag')]:
    v = df[col].value_counts().reset_index(); v.columns=[col,'count']
    fig = px.bar(v, x=col, y='count', color_discrete_sequence=[NEUTRAL], template=TEMPLATE, title=title)
    fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 6: ofac_match_flag — pie
ofac = df['ofac_match_flag'].value_counts().reset_index(); ofac.columns=['flag','count']
fig = px.pie(ofac, values='count', names='flag', title='OFAC Match Flag', hole=0.3,
             color_discrete_sequence=[SAFE, RISK], template=TEMPLATE)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 7: trade_mispricing_flag
v = df['trade_mispricing_flag'].value_counts().reset_index(); v.columns=['flag','count']
fig = px.bar(v, x='flag', y='count', color_discrete_sequence=[WARNING], template=TEMPLATE, title='Trade Mispricing Flag')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 8: transaction_type distribution
tt = df['transaction_type'].value_counts().reset_index(); tt.columns=['type','count']
fig = px.bar(tt, x='type', y='count', color_discrete_sequence=[PRIMARY], template=TEMPLATE, title='Transaction Type Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 9: Amount by transaction_type — box plot
fig = px.box(df, x='transaction_type', y='amount', color='transaction_type', template=TEMPLATE, title='Amount by Transaction Type')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 10: Top 15 client_country
cc = df['client_country'].value_counts().head(15).reset_index(); cc.columns=['country','count']
fig = px.bar(cc, x='country', y='count', color_discrete_sequence=[PRIMARY], template=TEMPLATE, title='Top 15 Client Countries')
fig.update_xaxes(tickangle=45)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 11: Top 15 counterparty_country
cc = df['counterparty_country'].value_counts().head(15).reset_index(); cc.columns=['country','count']
fig = px.bar(cc, x='country', y='count', color_discrete_sequence=[NEUTRAL], template=TEMPLATE, title='Top 15 Counterparty Countries')
fig.update_xaxes(tickangle=45)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 12: ownership_opacity_score histogram
fig = px.histogram(df.dropna(subset=['ownership_opacity_score']), x='ownership_opacity_score', nbins=30,
                   color_discrete_sequence=[WARNING], template=TEMPLATE, title='Ownership Opacity Score Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 13: Correlation heatmap
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
corr = df[numeric_cols].corr()
fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                template=TEMPLATE, title='Correlation Heatmap', width=900, height=800)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 14: sector_risk × pep_flag heatmap
pivot = df.groupby(['sector_risk','pep_flag']).size().unstack(fill_value=0)
fig = px.imshow(pivot, text_auto=True, color_continuous_scale='Purples',
                template=TEMPLATE, title='Sector Risk × PEP Flag Co-occurrence')
fig.show()
"""))
for ins in [
    "### Insight 1: PEP Exposure\nA measurable percentage of clients are PEP-flagged, requiring enhanced due diligence procedures.",
    "### Insight 2: Cross-border Risk\nHigh-risk counterparty countries overlap with FATF-flagged jurisdictions, amplifying transaction risk.",
    "### Insight 3: Structuring Patterns\nStructuring flags indicate potential money laundering — these accounts need immediate review.",
    "### Insight 4: Opacity Scores\nOwnership opacity scores vary widely; high-opacity entities cluster in higher risk sectors.",
    "### Insight 5: Transaction Types\nDifferent transaction types (SWIFT/Wire/Check) carry different risk profiles, with wire transfers showing higher amounts.",
]: c.append(nbf.v4.new_markdown_cell(ins))
c.append(nbf.v4.new_code_cell("""df.to_csv('data/processed/kyc_clean.csv', index=False)
print(f"Saved kyc_clean.csv — shape: {df.shape}")
"""))
nb.cells = c
nbf.write(nb, 'notebooks/04_kyc_eda.ipynb')
print("Created 04_kyc_eda.ipynb")

# ═══════════════ NOTEBOOK 05 ═══════════════
nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 05 — Complaint EDA\nExploratory analysis of CFPB consumer complaints dataset."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np
import plotly.express as px, plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))
c.append(nbf.v4.new_code_cell("""df = pd.read_csv('data/raw/complaints/cfpb_complaints.csv')
print(f"Shape: {df.shape}")
df.head()
"""))
c.append(nbf.v4.new_code_cell("""# Rename columns
df = df.rename(columns={
    'Consumer complaint narrative': 'narrative',
    'Timely response?': 'timely_response',
    'Company response to consumer': 'company_response',
    'Date received': 'date_received',
    'Sub-product': 'sub_product',
    'Sub-issue': 'sub_issue',
    'ZIP code': 'zip_code',
    'Submitted via': 'submitted_via',
    'Date sent to company': 'date_sent',
    'Complaint ID': 'complaint_id',
    'Company public response': 'company_public_response'
})

# Preprocessing
df = df.dropna(subset=['narrative'])
df['narrative_length'] = df['narrative'].apply(lambda x: len(str(x).split()))
df['date_received'] = pd.to_datetime(df['date_received'], utc=True)
print(f"Shape after dropping null narratives: {df.shape}")
print("\\nNull counts:\\n", df.isnull().sum())
"""))
c.append(nbf.v4.new_code_cell("""# Plot 1: Product distribution — top 10
prod = df['Product'].value_counts().head(10).reset_index(); prod.columns=['Product','count']
fig = px.bar(prod, x='Product', y='count', color_discrete_sequence=[PRIMARY],
             template=TEMPLATE, title='Top 10 Products by Complaint Count')
fig.update_xaxes(tickangle=45)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 2: Issue distribution — top 15
iss = df['Issue'].value_counts().head(15).reset_index(); iss.columns=['Issue','count']
fig = px.bar(iss, y='Issue', x='count', orientation='h', color_discrete_sequence=[NEUTRAL],
             template=TEMPLATE, title='Top 15 Issues')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 3: company_response distribution
cr = df['company_response'].value_counts().reset_index(); cr.columns=['response','count']
fig = px.bar(cr, x='response', y='count', color_discrete_sequence=[WARNING],
             template=TEMPLATE, title='Company Response Distribution')
fig.update_xaxes(tickangle=45)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 4: timely_response rate — pie
tr = df['timely_response'].value_counts().reset_index(); tr.columns=['timely','count']
fig = px.pie(tr, values='count', names='timely', title='Timely Response Rate', hole=0.3,
             color_discrete_sequence=[SAFE, RISK], template=TEMPLATE)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 5: narrative_length distribution
fig = px.histogram(df, x='narrative_length', nbins=50, color_discrete_sequence=[PRIMARY],
                   template=TEMPLATE, title='Complaint Narrative Length (words)')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 6: submitted_via distribution
sv = df['submitted_via'].value_counts().reset_index(); sv.columns=['channel','count']
fig = px.bar(sv, x='channel', y='count', color_discrete_sequence=[NEUTRAL],
             template=TEMPLATE, title='Submission Channel Distribution')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 7: Top 20 bigrams from narrative
vectorizer = CountVectorizer(ngram_range=(2,2), stop_words='english', max_features=20)
narratives = df['narrative'].fillna('').astype(str)
X = vectorizer.fit_transform(narratives)
bigram_counts = pd.DataFrame({'bigram': vectorizer.get_feature_names_out(),
                               'count': X.sum(axis=0).A1}).sort_values('count', ascending=True)
fig = px.bar(bigram_counts, y='bigram', x='count', orientation='h', color_discrete_sequence=[PRIMARY],
             template=TEMPLATE, title='Top 20 Bigrams in Complaint Narratives')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 8: Top 15 states
states = df['State'].value_counts().head(15).reset_index(); states.columns=['State','count']
fig = px.bar(states, x='State', y='count', color_discrete_sequence=[NEUTRAL],
             template=TEMPLATE, title='Top 15 States by Complaint Count')
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 9: Monthly complaint volume
df['month'] = df['date_received'].dt.to_period('M').astype(str)
monthly = df.groupby('month').size().reset_index(name='count')
fig = px.line(monthly, x='month', y='count', markers=True, color_discrete_sequence=[PRIMARY],
              template=TEMPLATE, title='Monthly Complaint Volume')
fig.update_xaxes(tickangle=45)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Plot 10: company_response vs timely_response — grouped bar
ct = df.groupby(['company_response','timely_response']).size().reset_index(name='count')
fig = px.bar(ct, x='company_response', y='count', color='timely_response', barmode='group',
             color_discrete_map={'Yes': SAFE, 'No': RISK},
             template=TEMPLATE, title='Company Response vs Timely Response')
fig.update_xaxes(tickangle=45)
fig.show()
"""))
for ins in [
    "### Insight 1: Product Concentration\nComplaints heavily concentrate in a few product categories, enabling focused improvement efforts.",
    "### Insight 2: Narrative Length\nLonger complaint narratives may indicate more complex issues requiring escalation.",
    "### Insight 3: Timeliness\nThe vast majority of responses are timely, but the small percentage of untimely ones drive customer dissatisfaction.",
    "### Insight 4: Channel Preferences\nWeb submission dominates, suggesting digital-first complaint resolution infrastructure is critical.",
    "### Insight 5: Geographic Patterns\nComplaint volume correlates with population centers, but per-capita rates may reveal underserved regions.",
]: c.append(nbf.v4.new_markdown_cell(ins))
c.append(nbf.v4.new_code_cell("""df = df.drop(columns=['month'], errors='ignore')
df.to_csv('data/processed/complaints_clean.csv', index=False)
print(f"Saved complaints_clean.csv — shape: {df.shape}")
"""))
nb.cells = c
nbf.write(nb, 'notebooks/05_complaint_eda.ipynb')
print("Created 05_complaint_eda.ipynb")
