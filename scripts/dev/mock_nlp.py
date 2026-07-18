import pandas as pd
import numpy as np
import random

df = pd.read_csv('data/processed/complaints_clean.csv')
sample_df = df.dropna(subset=['narrative'])
sample_df = sample_df[sample_df['narrative'].str.len() > 50]
sample_df = sample_df.sample(n=min(500, len(sample_df)), random_state=42).reset_index(drop=True)

categories = ["Billing", "Fraud", "Card Declined", "Rewards", "Customer Service", "Service Delay", "Credit Reporting", "Collections"]
emotions = ["Anger", "Frustration", "Neutral", "Legal Threat", "Distress"]

sample_df['complaint_summary'] = ["Simulated summary for testing purposes."] * len(sample_df)
np.random.seed(42)
sample_df['complaint_category'] = np.random.choice(categories, size=len(sample_df))
sample_df['emotion'] = np.random.choice(emotions, size=len(sample_df))

sample_df.to_csv('data/processed/complaints_with_nlp.csv', index=False)
print("Created mock complaints_with_nlp.csv")
