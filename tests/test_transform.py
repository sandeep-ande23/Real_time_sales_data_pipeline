import pandas as pd
from src.transform import clean_sales

def test_clean_sales_rejects_invalid_rows():
    df = pd.DataFrame([
        {"order_id":"O1","customer_id":"C1","store_id":"S1","order_date":"2026-08-01",
         "product_id":"P1","quantity":2,"unit_price":100,"discount":0.1,
         "payment_method":"UPI","payment_amount":180},
        {"order_id":"O2","customer_id":"C2","store_id":"S1","order_date":"bad",
         "product_id":"P2","quantity":-1,"unit_price":100,"discount":2,
         "payment_method":"Card","payment_amount":100}
    ])
    clean, failed = clean_sales(df)
    assert len(clean) == 1
    assert len(failed) == 1
