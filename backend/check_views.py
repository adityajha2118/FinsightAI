from sqlalchemy import create_engine, text
engine = create_engine("postgresql://postgres:Adityajha123%40@localhost:5432/finsight")
with engine.connect() as conn:
    print("v_sentiment_by_product:", conn.execute(text("SELECT * FROM v_sentiment_by_product LIMIT 3")).mappings().all())
    print("v_company_response_distribution:", conn.execute(text("SELECT * FROM v_company_response_distribution LIMIT 3")).mappings().all())
