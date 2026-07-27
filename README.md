<div align="center">

# 📊 FinSight AI: Unified Customer Intelligence & Retention Analytics Platform

**An enterprise fintech analytics platform combining predictive machine learning, NLP, and full-stack engineering to solve critical financial sector challenges including churn prevention, compliance monitoring, and customer support operations.**

[🚀 Project Overview](#project-overview) · [💼 Business Problems Solved](#business-problems-solved) · [🏛️ System Architecture](#system-architecture) · [🗄️ Datasets](#datasets-section) · [🧠 Modules](#modules) · [💻 Local Setup](#local-setup)

</div>

---

## 🎯 PROJECT OVERVIEW

FinSight AI simulates the advanced data analytics infrastructure of a modern, top-tier financial institution like American Express. By leveraging massive datasets, machine learning, Natural Language Processing (NLP), and a modern React/FastAPI stack, this unified intelligence platform completely modernizes customer lifecycle management.

Rather than relying on siloed data systems, FinSight AI combines multiple independent analytics engines into a single **Unified Intelligence Platform** with a sleek, Amex-branded interface:
* **Customer Lifecycle Management**: Tracking customers from acquisition through daily usage to long-term loyalty.
* **Customer Retention & Churn Prevention**: Proactively identifying at-risk customers before they close their accounts.
* **Campaign Optimization**: Targeting the right customers with the right marketing messages at the right time.
* **Compliance Monitoring**: Automating Anti-Money Laundering (AML) and Know Your Customer (KYC) risk detection.
* **Complaint Intelligence**: Utilizing Natural Language Processing (NLTK VADER) to classify emotions and resolve customer grievances.
* **Executive Decision Support**: Providing C-suite leadership with a real-time, interactive Next.js dashboard of portfolio health.

---

## 💼 BUSINESS PROBLEMS SOLVED

Financial institutions lose billions annually due to fragmented data and reactive strategies. FinSight AI addresses six critical challenges:

### 1. Customer Churn
* **Why it matters:** Acquiring a new credit card customer costs 5-25x more than retaining an existing one.
* **How FinSight solves it:** Trains XGBoost and Random Forest models on historical behavioral data to predict churn probability, allowing the retention team to intervene proactively.

### 2. Customer Inactivity
* **Why it matters:** "Silent attrition" occurs when a customer stops using their card but leaves the account open.
* **How FinSight solves it:** Activity scoring models flag customers exhibiting early signs of dormancy based on transaction frequency and volume drops.

### 3. Poor Campaign Performance
* **Why it matters:** Blanket marketing campaigns have abysmal conversion rates and annoy customers.
* **How FinSight solves it:** ML models predict the likelihood of conversion based on past interactions and demographics, optimizing target lists.

### 4. KYC Compliance Challenges
* **Why it matters:** Regulators heavily penalize banks for facilitating money laundering or doing business with sanctioned entities.
* **How FinSight solves it:** Analyzes transaction patterns, country risks, and entity opacity to assign real-time risk tiers (Low, Medium, High, Critical).

### 5. Customer Complaint Escalation
* **Why it matters:** Unresolved complaints escalate to regulatory bodies like the CFPB, incurring legal costs.
* **How FinSight solves it:** An NLP layer using VADER sentiment analysis classifies incoming complaints, detects severe emotional distress, and routes high-risk cases to priority teams.

### 6. Lack of Customer Segmentation
* **Why it matters:** Treating all customers equally ignores vast differences in profitability and risk.
* **How FinSight solves it:** K-Means clustering algorithmically groups customers into distinct personas (e.g., "Premium Customers", "Deal Hunters").

---

## 🏛️ SYSTEM ARCHITECTURE & TECH STACK

FinSight AI employs a highly modular, modern full-stack architecture. 

* **Frontend:** Built with **Next.js 15, React 19, and Tailwind CSS**. Features a custom Amex Design System (white theme, Amex blue accents) pulling real-time data from the backend.
* **Backend:** **FastAPI (Python)** serving REST endpoints, executing business logic, and querying the database.
* **Database:** **PostgreSQL** database utilizing SQL Views (e.g., `v_executive_kpis`) to aggregate massive datasets instantly for the frontend.
* **Machine Learning & EDA:** 21 **Jupyter Notebooks** using Scikit-Learn, XGBoost, and Plotly. (Notebooks are pre-configured with Kaleido to natively render static PNG graphs on GitHub).
* **NLP Layer:** NLTK VADER sentiment analysis for emotion detection, combined with rule-based categorization for complaint routing.

---

## 💻 LOCAL SETUP (For Recruiters & Developers)

Want to run this massive platform locally? Follow these steps:

### 1. Start the PostgreSQL Database
Ensure you have a PostgreSQL server running locally or via Docker with your financial data loaded into the `finsight` database. Ensure the SQL views in `sql/02_views.sql` have been executed.

### 2. Run the FastAPI Backend
```bash
# Navigate to the project root
cd FinSight-AI

# Install Python dependencies (requires Python 3.10+)
pip install -r requirements.txt

# Start the FastAPI server
python -m uvicorn backend.main:app --reload --port 8000
```
*The backend will be live at http://localhost:8000. You can view the API documentation at http://localhost:8000/docs.*

### 3. Run the Next.js Frontend
```bash
# Open a new terminal tab and navigate to the frontend
cd FinSight-AI/finsight-frontend

# Install Node dependencies (requires Node.js 18+)
npm install

# Start the Next.js dev server
npm run dev
```
*The frontend dashboard will be live at http://localhost:3000.*

---

## 📓 MACHINE LEARNING NOTEBOOKS

All data science work, exploratory data analysis (EDA), and machine learning pipelines are contained in the `notebooks/` directory. 

*All notebooks have been configured to render static PNG plots so you can view the charts directly on GitHub without running them.*

* `01_customer_eda.ipynb` -> `05_complaint_eda.ipynb`: Cleans raw datasets and performs EDA.
* `06_customer_segmentation.ipynb`: Trains K-Means clustering (k=5).
* `07_inactivity_detection.ipynb`: Builds scoring to identify silent attrition.
* `08_churn_prediction.ipynb`: Trains XGBoost to output churn probability.
* `09_campaign_prediction.ipynb`: Addresses severe data imbalance with SMOTE.
* `10_kyc_risk_prediction.ipynb`: Ensembles transaction and entity risk flags.
* `11_complaint_sentiment.ipynb`: NLP processing for sentiment and routing.
* `12_escalation_prediction.ipynb`: Trains an XGBoost model on the newly generated NLP data to predict CFPB escalation.
* `13_unified_customer_profile.ipynb`: Joins multiple ML outputs into a single, master 360-degree customer view.

---

## 🏆 FINAL DELIVERABLES & BUSINESS VALUE

This platform delivers a complete, end-to-end blueprint for modern financial intelligence. 

**What was achieved in this project:**
1. **Full-Stack Application:** Built a complete Next.js and FastAPI application from the ground up to visualize complex data.
2. **Database Engineering:** Replaced static CSV serving with a robust PostgreSQL database utilizing complex SQL Views.
3. **Design System:** Created a pixel-perfect, premium Amex-style UI architecture.
4. **Data Science Pipelines:** Executed 21 comprehensive Jupyter Notebooks covering EDA, clustering, tree-based models, and NLP. 

</div>
