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

# import pandas as pd
# from sqlalchemy import create_engine

# # Neon PostgreSQL connection
# DATABASE_URL = "postgresql://neondb_owner:npg_iEjZAknp63HS@ep-nameless-dew-aix0a760-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

# engine = create_engine(DATABASE_URL)

# # Load CSV
# df = pd.read_csv("adani.csv")

# # Upload to Neon
# df.to_sql(
#     "users",        # table name
#     engine,
#     if_exists="replace",   # replace table if exists
#     index=False
# )

# print("CSV uploaded successfully!")

from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Neon PostgreSQL connection
DATABASE_URL = "postgresql://neondb_owner:npg_iEjZAknp63HS@ep-nameless-dew-aix0a760-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

@app.route("/")
def home():
    return "Flask API Running"

@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read CSV file
        df = pd.read_csv(file)

        # -----------------------------
        # DATA CLEANING
        # -----------------------------

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Fill numeric missing values
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

        # Fill categorical missing values
        cat_cols = df.select_dtypes(include=["object"]).columns
        df[cat_cols] = df[cat_cols].fillna("Unknown")

        # Remove extra spaces
        for col in cat_cols:
            df[col] = df[col].astype(str).str.strip()

        # Standardize column names
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(" ", "_")

        # -----------------------------
        # INSERT INTO NEON DATABASE
        # -----------------------------

        df.to_sql(
            "dataset",      # table name
            engine,
            if_exists="append",
            index=False
        )

        return jsonify({
            "message": "File uploaded and cleaned successfully",
            "rows_inserted": len(df),
            "columns": list(df.columns)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)