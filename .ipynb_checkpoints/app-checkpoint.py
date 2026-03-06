# from flask import Flask
# from sqlalchemy import create_engine, text

# app = Flask(__name__)

# DATABASE_URL = "postgresql://neondb_owner:npg_iEjZAknp63HS@ep-nameless-dew-aix0a760-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True
# )

# @app.route("/")
# def home():
#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT 1"))
#         return f"Database Connected! Result: {result.fetchone()}"

# if __name__ == "__main__":
#     app.run(debug=True)

import pandas as pd
from sqlalchemy import create_engine

# Neon PostgreSQL connection
DATABASE_URL = "postgresql://neondb_owner:npg_iEjZAknp63HS@ep-nameless-dew-aix0a760-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

# Load CSV
df = pd.read_csv("adani.csv")

# Upload to Neon
df.to_sql(
    "users",        # table name
    engine,
    if_exists="replace",   # replace table if exists
    index=False
)

print("CSV uploaded successfully!")