import logging
import shutil
from datetime import datetime

import pandas as pd

from config import INCOMING, PROCESSED, FAILED, LOG_DIR
from db import get_connection
from transform import clean_sales

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def ensure_reference_data(cur, df):
    customers = [
        (cid, f"Customer {cid[1:]}", f"{cid.lower()}@example.com",
         "Hyderabad", "Telangana", datetime.now().date())
        for cid in sorted(df["customer_id"].unique())
    ]

    stores = [
        (sid, f"Store {sid[1:]}", "Hyderabad", "Telangana")
        for sid in sorted(df["store_id"].unique())
    ]

    products = [
        (pid, f"Product {pid[1:]}", "Electronics", 999.00, 650.00)
        for pid in sorted(df["product_id"].unique())
    ]

    cur.executemany(
        """INSERT IGNORE INTO customers
           (customer_id, customer_name, email, city, state, registration_date)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        customers
    )

    cur.executemany(
        """INSERT IGNORE INTO stores
           (store_id, store_name, city, state)
           VALUES (%s, %s, %s, %s)""",
        stores
    )

    cur.executemany(
        """INSERT IGNORE INTO products
           (product_id, product_name, category, price, cost)
           VALUES (%s, %s, %s, %s, %s)""",
        products
    )


def load_file(path):
    logger.info("Processing %s", path.name)

    df = pd.read_csv(path)
    clean, failed = clean_sales(df)

    if clean.empty:
        print(f"FAILED: {path.name} contains no valid records.")
        return

    conn = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        ensure_reference_data(cur, clean)

        orders = [
            (r.order_id, r.customer_id, r.store_id,
             r.order_date.to_pydatetime(), "completed")
            for r in clean.itertuples(index=False)
        ]

        cur.executemany(
            """INSERT IGNORE INTO orders
               (order_id, customer_id, store_id, order_date, status)
               VALUES (%s, %s, %s, %s, %s)""",
            orders
        )

        items = [
            (r.order_id, r.product_id, int(r.quantity),
             float(r.unit_price), float(r.discount))
            for r in clean.itertuples(index=False)
        ]

        cur.executemany(
            """INSERT IGNORE INTO order_items
               (order_id, product_id, quantity, unit_price, discount)
               VALUES (%s, %s, %s, %s, %s)""",
            items
        )

        for r in clean.itertuples(index=False):
            cur.execute(
                """INSERT INTO payments
                   (order_id, payment_method, payment_amount, payment_status)
                   SELECT %s, %s, %s, %s
                   WHERE NOT EXISTS
                   (SELECT 1 FROM payments WHERE order_id = %s)""",
                (r.order_id, r.payment_method, float(r.payment_amount),
                 "paid", r.order_id)
            )

        cur.execute(
            """INSERT INTO pipeline_runs
               (file_name, rows_read, rows_loaded, rows_failed,
                finished_at, status)
               VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s)""",
            (path.name, len(df), len(clean), len(failed), "success")
        )

        conn.commit()
        cur.close()
        conn.close()
        conn = None

        if len(failed) > 0:
            failed.to_csv(FAILED / path.name, index=False)

        destination = PROCESSED / path.name
        if destination.exists():
            destination.unlink()

        shutil.move(str(path), str(destination))

        logger.info(
            "Completed %s | read=%s loaded=%s failed=%s",
            path.name, len(df), len(clean), len(failed)
        )

        print(
            f"SUCCESS: {path.name} | "
            f"Read: {len(df)} | Loaded: {len(clean)} | Failed: {len(failed)}"
        )

    except Exception:
        logger.exception("Pipeline failed for %s", path.name)

        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

        print(f"ERROR: Pipeline failed for {path.name}. Check logs/pipeline.log.")
        raise


def main():
    files = sorted(INCOMING.glob("*.csv"))

    if not files:
        print("No incoming CSV files found.")
        return

    for path in files:
        load_file(path)


if __name__ == "__main__":
    main()
