from sqlalchemy import create_engine, text
engine = create_engine("postgresql://postgres:Adityajha123%40@localhost:5432/finsight")
with engine.connect() as conn:
    conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    conn.commit()
print("Database schema wiped.")
