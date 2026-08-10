import pandas as pd

REQUIRED_COLUMNS = [
    "order_id", "customer_id", "store_id", "order_date",
    "product_id", "quantity", "unit_price", "discount",
    "payment_method", "payment_amount"
]

def clean_sales(df: pd.DataFrame):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    work = df.copy()
    work["order_date"] = pd.to_datetime(work["order_date"], errors="coerce")
    work["quantity"] = pd.to_numeric(work["quantity"], errors="coerce")
    work["unit_price"] = pd.to_numeric(work["unit_price"], errors="coerce")
    work["discount"] = pd.to_numeric(work["discount"], errors="coerce").fillna(0)
    work["payment_amount"] = pd.to_numeric(work["payment_amount"], errors="coerce")

    valid = (
        work["order_id"].notna()
        & work["customer_id"].notna()
        & work["store_id"].notna()
        & work["product_id"].notna()
        & work["order_date"].notna()
        & work["quantity"].notna()
        & (work["quantity"] > 0)
        & work["unit_price"].notna()
        & (work["unit_price"] >= 0)
        & (work["discount"] >= 0)
        & (work["discount"] <= 1)
        & work["payment_amount"].notna()
        & (work["payment_amount"] >= 0)
    )

    clean = work.loc[valid].copy()
    failed = work.loc[~valid].copy()
    clean["quantity"] = clean["quantity"].astype(int)
    clean = clean.drop_duplicates(subset=["order_id", "product_id"])
    return clean, failed
