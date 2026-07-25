-- ============================================================
-- FinSight AI — SQL Business Reporting Views
-- ============================================================
-- All business KPIs are computed here in SQL, not in Python/React.
-- FastAPI endpoints query these views directly.
-- ============================================================

-- ── EXECUTIVE DASHBOARD VIEWS ────────────────────────────────

-- Total customers & churn metrics
CREATE OR REPLACE VIEW v_executive_kpis AS
SELECT
    COUNT(*)                                                    AS total_customers,
    SUM(CASE WHEN attrition_flag = 'Attrited Customer' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN attrition_flag = 'Attrited Customer' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    )                                                           AS churn_rate_pct,
    ROUND(AVG(credit_limit)::numeric, 2)                        AS avg_credit_limit,
    ROUND(AVG(avg_utilization_ratio)::numeric, 4)               AS avg_utilization
FROM customers;


-- Customer health distribution (from ML predictions)
CREATE OR REPLACE VIEW v_customer_health_distribution AS
SELECT
    risk_label,
    COUNT(*) AS customer_count
FROM customer_predictions
GROUP BY risk_label
ORDER BY customer_count DESC;


-- ── COMPLAINT VIEWS ──────────────────────────────────────────

-- Monthly complaint trend
CREATE OR REPLACE VIEW v_monthly_complaints AS
SELECT
    TO_CHAR(date_received, 'YYYY-MM') AS month,
    COUNT(*)                          AS complaint_count
FROM complaints
WHERE date_received IS NOT NULL
GROUP BY TO_CHAR(date_received, 'YYYY-MM')
ORDER BY month;


-- Complaints by product
CREATE OR REPLACE VIEW v_complaints_by_product AS
SELECT
    product,
    COUNT(*)                                                       AS complaint_count,
    ROUND(100.0 * COUNT(*) / NULLIF(SUM(COUNT(*)) OVER(), 0), 2)  AS pct_of_total
FROM complaints
GROUP BY product
ORDER BY complaint_count DESC;


-- Complaints by issue
CREATE OR REPLACE VIEW v_complaints_by_issue AS
SELECT
    issue,
    COUNT(*) AS complaint_count
FROM complaints
GROUP BY issue
ORDER BY complaint_count DESC
LIMIT 20;


-- State-wise complaints
CREATE OR REPLACE VIEW v_complaints_by_state AS
SELECT
    state,
    COUNT(*) AS complaint_count
FROM complaints
WHERE state IS NOT NULL AND state != ''
GROUP BY state
ORDER BY complaint_count DESC;


-- Timely response rate
CREATE OR REPLACE VIEW v_timely_response_rate AS
SELECT
    COUNT(*)                                                                    AS total_complaints,
    SUM(CASE WHEN timely_response = 'Yes' THEN 1 ELSE 0 END)                   AS timely_count,
    ROUND(
        100.0 * SUM(CASE WHEN timely_response = 'Yes' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    )                                                                           AS timely_response_pct
FROM complaints;


-- Average resolution time (days between received and sent to company)
CREATE OR REPLACE VIEW v_avg_resolution_time AS
SELECT
    ROUND(AVG(date_sent_to_company - date_received)::numeric, 1) AS avg_resolution_days
FROM complaints
WHERE date_sent_to_company IS NOT NULL AND date_received IS NOT NULL;


-- Company response distribution
CREATE OR REPLACE VIEW v_company_response_distribution AS
SELECT
    company_response,
    COUNT(*) AS response_count
FROM complaints
WHERE company_response IS NOT NULL
GROUP BY company_response
ORDER BY response_count DESC;


-- Complaint growth (current month vs previous month)
CREATE OR REPLACE VIEW v_complaint_growth AS
WITH monthly AS (
    SELECT
        TO_CHAR(date_received, 'YYYY-MM') AS month,
        COUNT(*) AS cnt
    FROM complaints
    WHERE date_received IS NOT NULL
    GROUP BY TO_CHAR(date_received, 'YYYY-MM')
),
ranked AS (
    SELECT month, cnt,
           LAG(cnt) OVER (ORDER BY month) AS prev_cnt
    FROM monthly
)
SELECT
    month,
    cnt AS current_month_count,
    prev_cnt AS previous_month_count,
    CASE WHEN prev_cnt > 0
         THEN ROUND(100.0 * (cnt - prev_cnt) / prev_cnt, 2)
         ELSE NULL
    END AS growth_pct
FROM ranked
ORDER BY month DESC
LIMIT 1;


-- ── SENTIMENT VIEWS ──────────────────────────────────────────

-- Sentiment distribution
CREATE OR REPLACE VIEW v_sentiment_distribution AS
SELECT
    sentiment_label,
    COUNT(*) AS complaint_count,
    ROUND(AVG(compound_score)::numeric, 4) AS avg_compound
FROM complaint_sentiment
GROUP BY sentiment_label
ORDER BY complaint_count DESC;


-- Sentiment by product (cross-analysis)
CREATE OR REPLACE VIEW v_sentiment_by_product AS
SELECT
    c.product,
    cs.sentiment_label,
    COUNT(*) AS count
FROM complaint_sentiment cs
JOIN complaints c ON c.complaint_id = cs.complaint_id
GROUP BY c.product, cs.sentiment_label
ORDER BY c.product, count DESC;


-- Negative sentiment percentage (for executive KPI)
CREATE OR REPLACE VIEW v_negative_sentiment_pct AS
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN sentiment_label = 'Negative' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    ) AS negative_pct
FROM complaint_sentiment;


-- ── CAMPAIGN VIEWS ───────────────────────────────────────────

-- Campaign success rate
CREATE OR REPLACE VIEW v_campaign_success AS
SELECT
    COUNT(*) AS total_contacts,
    SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END) AS conversions,
    ROUND(
        100.0 * SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    ) AS success_rate_pct
FROM campaigns;


-- Conversion by job
CREATE OR REPLACE VIEW v_conversion_by_job AS
SELECT
    job,
    COUNT(*) AS total,
    SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END) AS conversions,
    ROUND(
        100.0 * SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    ) AS conversion_rate
FROM campaigns
GROUP BY job
ORDER BY conversion_rate DESC;


-- Conversion by education
CREATE OR REPLACE VIEW v_conversion_by_education AS
SELECT
    education,
    COUNT(*) AS total,
    SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END) AS conversions,
    ROUND(
        100.0 * SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    ) AS conversion_rate
FROM campaigns
GROUP BY education
ORDER BY conversion_rate DESC;


-- Conversion by contact method
CREATE OR REPLACE VIEW v_conversion_by_contact AS
SELECT
    contact,
    COUNT(*) AS total,
    SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END) AS conversions,
    ROUND(
        100.0 * SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    ) AS conversion_rate
FROM campaigns
GROUP BY contact
ORDER BY conversion_rate DESC;


-- Campaign fatigue analysis
CREATE OR REPLACE VIEW v_campaign_fatigue AS
SELECT
    campaign_count AS contacts_made,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END) AS conversions,
    ROUND(
        100.0 * SUM(CASE WHEN subscribed = 'yes' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    ) AS conversion_rate
FROM campaigns
GROUP BY campaign_count
ORDER BY campaign_count;


-- ── COMPLIANCE / KYC VIEWS ───────────────────────────────────

-- Risk distribution (will be populated after compliance scoring)
CREATE OR REPLACE VIEW v_risk_distribution AS
SELECT
    CASE
        WHEN (pep_flag + sanctions_flag + ofac_country_flag + structuring_pattern_flag) >= 3 THEN 'Critical'
        WHEN (pep_flag + sanctions_flag + ofac_country_flag + structuring_pattern_flag) >= 2 THEN 'High'
        WHEN (pep_flag + sanctions_flag + ofac_country_flag + structuring_pattern_flag) >= 1 THEN 'Medium'
        ELSE 'Low'
    END AS risk_tier,
    COUNT(*) AS profile_count
FROM kyc_profiles
GROUP BY risk_tier
ORDER BY profile_count DESC;


-- Country risk summary
CREATE OR REPLACE VIEW v_country_risk AS
SELECT
    country,
    COUNT(*) AS profile_count,
    SUM(pep_flag) AS pep_count,
    SUM(sanctions_flag) AS sanctions_count,
    SUM(ofac_country_flag) AS ofac_count
FROM kyc_profiles
GROUP BY country
ORDER BY profile_count DESC
LIMIT 20;


-- Sector risk summary
CREATE OR REPLACE VIEW v_sector_risk AS
SELECT
    sector,
    sector_risk,
    COUNT(*) AS profile_count,
    ROUND(AVG(ownership_opacity_score)::numeric, 3) AS avg_opacity
FROM kyc_profiles
GROUP BY sector, sector_risk
ORDER BY profile_count DESC;


-- High risk customers
CREATE OR REPLACE VIEW v_high_risk_customers AS
SELECT
    profile_id,
    client_id,
    client_name,
    sector,
    country,
    pep_flag,
    sanctions_flag,
    ownership_opacity_score,
    (pep_flag + sanctions_flag + ofac_country_flag + structuring_pattern_flag
     + rapid_movement_flag + trade_mispricing_flag) AS total_flags
FROM kyc_profiles
WHERE (pep_flag + sanctions_flag + ofac_country_flag + structuring_pattern_flag) >= 2
ORDER BY total_flags DESC;


-- ── SEGMENTATION VIEWS ───────────────────────────────────────

-- Segment distribution
CREATE OR REPLACE VIEW v_segment_distribution AS
SELECT
    segment_name,
    COUNT(*) AS customer_count
FROM customer_segments
GROUP BY segment_name
ORDER BY customer_count DESC;


-- Segment profiles (avg metrics per segment)
CREATE OR REPLACE VIEW v_segment_profiles AS
SELECT
    cs.segment_name,
    COUNT(*) AS customer_count,
    ROUND(AVG(c.credit_limit)::numeric, 2) AS avg_credit_limit,
    ROUND(AVG(c.total_trans_amt)::numeric, 2) AS avg_trans_amt,
    ROUND(AVG(c.total_trans_ct)::numeric, 1) AS avg_trans_ct,
    ROUND(AVG(c.avg_utilization_ratio)::numeric, 4) AS avg_utilization,
    ROUND(AVG(c.months_inactive_12_mon)::numeric, 1) AS avg_months_inactive,
    ROUND(AVG(cp.churn_probability)::numeric, 4) AS avg_churn_prob
FROM customer_segments cs
JOIN customers c ON c.client_id = cs.client_id
LEFT JOIN customer_predictions cp ON cp.client_id = cs.client_id
GROUP BY cs.segment_name
ORDER BY avg_credit_limit DESC;


-- Churn distribution
CREATE OR REPLACE VIEW v_churn_distribution AS
SELECT
    risk_label,
    COUNT(*) AS customer_count,
    ROUND(AVG(churn_probability)::numeric, 4) AS avg_churn_prob
FROM customer_predictions
GROUP BY risk_label
ORDER BY avg_churn_prob DESC;


-- Inactive customers watchlist
CREATE OR REPLACE VIEW v_inactive_customers AS
SELECT
    c.client_id,
    c.customer_age,
    c.income_category,
    c.card_category,
    c.months_inactive_12_mon,
    c.total_trans_ct,
    c.avg_utilization_ratio,
    cp.churn_probability,
    cp.activity_score,
    cs.segment_name
FROM customers c
LEFT JOIN customer_predictions cp ON cp.client_id = c.client_id
LEFT JOIN customer_segments cs ON cs.client_id = c.client_id
WHERE c.months_inactive_12_mon >= 3
ORDER BY cp.churn_probability DESC NULLS LAST;
