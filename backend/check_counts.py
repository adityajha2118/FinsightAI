from sqlalchemy import create_engine, text
engine = create_engine("postgresql://postgres:Adityajha123%40@localhost:5432/finsight")
with engine.connect() as conn:
    print("customer_segments:", conn.execute(text("SELECT COUNT(*) FROM customer_segments")).scalar())
    print("customer_predictions:", conn.execute(text("SELECT COUNT(*) FROM customer_predictions")).scalar())
    print("complaint_sentiment:", conn.execute(text("SELECT COUNT(*) FROM complaint_sentiment")).scalar())
