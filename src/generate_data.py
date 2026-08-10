from datetime import datetime, timedelta
import random
import pandas as pd
from config import INCOMING

random.seed(42)
customers = [f"C{i:04d}" for i in range(1, 51)]
stores = [f"S{i:03d}" for i in range(1, 7)]
products = [f"P{i:04d}" for i in range(1, 21)]
prices = {p: round(random.uniform(199, 4999), 2) for p in products}

rows = []
start = datetime.now() - timedelta(days=30)
for i in range(1, 501):
    product = random.choice(products)
    qty = random.randint(1, 5)
    discount = random.choice([0, 0, 0.05, 0.10, 0.15])
    total = round(qty * prices[product] * (1 - discount), 2)
    rows.append({
        "order_id": f"O{100000+i}",
        "customer_id": random.choice(customers),
        "store_id": random.choice(stores),
        "order_date": start + timedelta(
            days=random.randint(0, 29),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        ),
        "product_id": product,
        "quantity": qty,
        "unit_price": prices[product],
        "discount": discount,
        "payment_method": random.choice(["UPI", "Card", "Cash", "NetBanking"]),
        "payment_amount": total,
    })

out = INCOMING / "sales_sample.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"Generated {len(rows)} rows at {out}")
