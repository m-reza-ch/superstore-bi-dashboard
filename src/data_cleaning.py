import pandas as pd
from src.config import *


def load_and_clean(path):
    df = pd.read_csv(path, encoding="latin1")

    # Normalize text columns
    for col in [
        "Category",
        "Sub-Category",
        "Region",
        "Segment",
        "State",
        "City",
        "Product Name",
    ]:
        df[col] = df[col].astype(str).str.strip()

    # Convert dates
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

    # Convert numeric columns safely
    for col in [SALES_COL, PROFIT_COL, QUANTITY_COL, "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows missing critical fields
    df = df.dropna(subset=[DATE_COL, SALES_COL, REGION_COL, CATEGORY_COL])

    # Business validation
    df = df[df[QUANTITY_COL] > 0]
    df = df[df[SALES_COL] >= 0]

    # Impute remaining numeric NaNs
    df[[SALES_COL, PROFIT_COL, QUANTITY_COL]] = df[
        [SALES_COL, PROFIT_COL, QUANTITY_COL]
    ].fillna(0)

    df = df.drop_duplicates()

    return df
