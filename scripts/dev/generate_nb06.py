"""Generate notebook 06_customer_segmentation.ipynb"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
c = []
c.append(nbf.v4.new_markdown_cell("# 06 - Customer Segmentation (KMeans)\nCluster customers into actionable segments based on credit and transaction features."))
c.append(nbf.v4.new_code_cell("""import pandas as pd, numpy as np, joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import plotly.express as px, plotly.graph_objects as go
import warnings; warnings.filterwarnings('ignore')
SEED=42; np.random.seed(SEED)
PRIMARY='#635BFF'; RISK='#E74C3C'; SAFE='#27AE60'; NEUTRAL='#3498DB'; WARNING='#F39C12'; TEMPLATE='plotly_white'
"""))
c.append(nbf.v4.new_code_cell("""df = pd.read_csv('data/processed/customer_clean.csv')
print(f"Shape: {df.shape}")
features = ['Credit_Limit','Total_Trans_Amt','Total_Trans_Ct',
            'Avg_Utilization_Ratio','Total_Revolving_Bal','Months_Inactive_12_mon']
df = df.dropna(subset=features)
print(f"Shape after dropping nulls: {df.shape}")
"""))
c.append(nbf.v4.new_code_cell("""# StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])
print(f"Scaled shape: {X_scaled.shape}")
"""))
c.append(nbf.v4.new_code_cell("""# Elbow method
inertias = []
K_range = range(2, 11)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=SEED, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
fig = px.line(x=list(K_range), y=inertias, markers=True,
              labels={'x':'k','y':'Inertia'},
              title='Elbow Method - Inertia vs k', template=TEMPLATE)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Silhouette scores
sil_scores = []
for k in range(2, 9):
    km = KMeans(n_clusters=k, random_state=SEED, n_init=10)
    labels = km.fit_predict(X_scaled)
    sil_scores.append(silhouette_score(X_scaled, labels))
    print(f"k={k}: silhouette={sil_scores[-1]:.4f}")
optimal_k = range(2, 9)[np.argmax(sil_scores)]
print(f"\\nOptimal k by silhouette: {optimal_k}")
# Use k=5 as target for 5 named segments
optimal_k = 5
print(f"Using k={optimal_k} for 5 named segments")
fig = px.bar(x=list(range(2,9)), y=sil_scores, labels={'x':'k','y':'Silhouette Score'},
             title='Silhouette Score by k', template=TEMPLATE, color_discrete_sequence=[PRIMARY])
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Fit final KMeans
kmeans = KMeans(n_clusters=optimal_k, random_state=SEED, n_init=10)
df['cluster_id'] = kmeans.fit_predict(X_scaled)
print("Cluster counts:")
print(df['cluster_id'].value_counts().sort_index())
"""))
c.append(nbf.v4.new_code_cell("""# Assign human-readable names based on cluster means
cluster_means = df.groupby('cluster_id')[features].mean()
print("Cluster means:\\n", cluster_means.round(2))

# Deterministic assignment
engagement = cluster_means['Credit_Limit'] + cluster_means['Total_Trans_Amt']
premium_cluster = engagement.idxmax()

remaining = [i for i in range(optimal_k) if i != premium_cluster]
daily_cluster = cluster_means.loc[remaining, 'Total_Trans_Ct'].idxmax()

remaining = [i for i in remaining if i != daily_cluster]
atrisk_cluster = cluster_means.loc[remaining, 'Months_Inactive_12_mon'].idxmax()

remaining = [i for i in remaining if i != atrisk_cluster]
# Deal Hunters: lowest revolving bal among remaining
deal_cluster = cluster_means.loc[remaining, 'Total_Revolving_Bal'].idxmin()

remaining = [i for i in remaining if i != deal_cluster]
silent_cluster = remaining[0] if remaining else deal_cluster

cluster_map = {
    premium_cluster: 'Premium Customers',
    daily_cluster: 'Daily Spenders',
    atrisk_cluster: 'At-Risk Customers',
    deal_cluster: 'Deal Hunters',
    silent_cluster: 'Silent Users'
}
print("\\nCluster mapping:", cluster_map)
df['segment_name'] = df['cluster_id'].map(cluster_map)
kmeans.cluster_map_ = cluster_map
print("\\nSegment distribution:")
print(df['segment_name'].value_counts())
"""))
c.append(nbf.v4.new_code_cell("""# PCA 2D scatter
pca = PCA(n_components=2, random_state=SEED)
pca_result = pca.fit_transform(X_scaled)
df['pca_1'] = pca_result[:, 0]
df['pca_2'] = pca_result[:, 1]
fig = px.scatter(df, x='pca_1', y='pca_2', color='segment_name',
                 title='Customer Segments (PCA 2D)', template=TEMPLATE, opacity=0.6)
fig.show()
"""))
c.append(nbf.v4.new_code_cell("""# Cluster profile table
profile = df.groupby('segment_name')[features].mean().round(2)
print("Cluster Profile:")
profile
"""))
c.append(nbf.v4.new_code_cell("""# Save models
import os
os.makedirs('models/segmentation', exist_ok=True)
joblib.dump(kmeans, 'models/segmentation/kmeans_model.pkl')
joblib.dump(scaler, 'models/segmentation/scaler.pkl')
print("Saved KMeans model and scaler")

# Save outputs
df.to_csv('data/processed/customer_with_segments.csv', index=False)
df[features + ['cluster_id','segment_name']].to_parquet('data/features/customer_features.parquet', index=False)
print(f"Saved customer_with_segments.csv - shape: {df.shape}")
print(f"Saved customer_features.parquet")
"""))

nb.cells = c
nbf.write(nb, 'notebooks/06_customer_segmentation.ipynb')
print("Created 06_customer_segmentation.ipynb")
