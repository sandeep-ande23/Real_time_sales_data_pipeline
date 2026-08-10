import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from db import get_connection

st.set_page_config(page_title="Sales Analytics", layout="wide")
st.title("Sales Analytics Dashboard")

def load_data():
    conn = get_connection()
    try:
        kpi = pd.read_sql('''
            WITH order_totals AS (
                SELECT o.order_id,
                       SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) AS order_value
                FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
                WHERE o.status='completed'
                GROUP BY o.order_id
            )
            SELECT SUM(order_value) AS revenue,
                   COUNT(*) AS orders,
                   COUNT(DISTINCT o.customer_id) AS customers,
                   AVG(order_value) AS aov
            FROM order_totals ot JOIN orders o ON o.order_id=ot.order_id
        ''', conn)
        daily = pd.read_sql('''
            SELECT DATE(o.order_date) AS sales_date,
                   SUM(oi.quantity*oi.unit_price*(1-oi.discount)) AS revenue
            FROM orders o JOIN order_items oi ON oi.order_id=o.order_id
            WHERE o.status='completed'
            GROUP BY DATE(o.order_date) ORDER BY sales_date
        ''', conn)
        products = pd.read_sql('''
            SELECT p.product_name,
                   SUM(oi.quantity) AS units_sold,
                   SUM(oi.quantity*oi.unit_price*(1-oi.discount)) AS revenue
            FROM order_items oi JOIN products p ON p.product_id=oi.product_id
            JOIN orders o ON o.order_id=oi.order_id
            WHERE o.status='completed'
            GROUP BY p.product_id,p.product_name ORDER BY revenue DESC LIMIT 10
        ''', conn)
        return kpi, daily, products
    finally:
        conn.close()

try:
    kpi, daily, products = load_data()
    row = kpi.iloc[0]
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Revenue", f"₹{row.revenue:,.0f}")
    c2.metric("Orders", f"{int(row.orders):,}")
    c3.metric("Customers", f"{int(row.customers):,}")
    c4.metric("Average Order", f"₹{row.aov:,.0f}")
    st.subheader("Daily Revenue")
    st.line_chart(daily.set_index("sales_date")["revenue"])
    st.subheader("Top Products")
    st.bar_chart(products.set_index("product_name")["revenue"])
    st.dataframe(products, use_container_width=True)
except Exception as exc:
    st.error("Check PostgreSQL and your .env configuration.")
    st.exception(exc)
