import pandas as pd

def load_and_clean_data(path):
    df = pd.read_excel(path)

    # Normalize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Parse dates
    for col in ["date_found", "date_reported", "creation_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    today = pd.Timestamp.today()

    # Days open
    df["days_open"] = (today - df["date_found"]).dt.days

    # Aging buckets
    df["aging_bucket"] = pd.cut(
        df["days_open"],
        bins=[-1, 30, 60, 90, 9999],
        labels=["0–30", "31–60", "61–90", "90+"]
    )

    # Normalize status
    df["issue_status"] = df["issue_status"].str.title()

    return df
