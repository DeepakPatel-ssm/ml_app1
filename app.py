from flask import Flask, request, jsonify
import os
from sqlalchemy import create_engine
from flask_cors import CORS
from dotenv import load_dotenv
from data_cleaning import clean_data

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

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

        # Clean data
        df = clean_data(file)

        # Insert into Neon PostgreSQL
        df.to_sql(
            "dataset",
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


@app.route("/data", methods=["GET"])
def get_data():
    try:
        query = "SELECT * FROM dataset"

        df = pd.read_sql(query, engine)

        return jsonify({
            "rows": len(df),
            "data": df.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()

