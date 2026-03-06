import pandas as pd

def clean_data(file):

    df = pd.read_csv(file)

    # Remove duplicates
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

    return df