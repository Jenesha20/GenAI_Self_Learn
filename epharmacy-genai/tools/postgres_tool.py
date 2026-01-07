import os
import psycopg2
from typing import Dict, Optional

DB_CONFIG = {
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
    "dbname": os.getenv("PG_DB"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
}

def _get_conn():
    return psycopg2.connect(**DB_CONFIG)


def fetch_product_info(product_query: str) -> Dict:
    """
    Fetch product details by name or SKU.
    """
    try:
        conn = _get_conn()
        cur = conn.cursor()

        query = """
        SELECT product_id, name, price, sku, requires_prescription
        FROM products
        WHERE name ILIKE %s
        LIMIT 1
        """
        cur.execute(query, (f"%{product_query}%",))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if not row:
            return {
                "status": "not_found",
                "data": None,
                "message": "Product not found"
            }

        product = {
            "product_id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "stock": row[3],
            "requires_prescription": bool(row[4]),
        }

        return {
            "status": "success",
            "data": product,
            "message": "Product fetched"
        }

    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "message": str(e)
        }
    
def fetch_products_by_category(category_name: str) -> Dict:
    """
    Fetch products by category name (e.g., cold, fever, cough).
    Uses join between products and categories tables.
    """
    try:
        conn = _get_conn()
        cur = conn.cursor()

        query = """
        SELECT 
            p.product_id,
            p.name,
            p.price,
            p.sku,
            p.requires_prescription
        FROM products p
        JOIN categories c
            ON p.category_id = c.category_id
        WHERE c.name ILIKE %s
          AND p.is_active = TRUE
        LIMIT 10
        """

        cur.execute(query, (f"%{category_name}%",))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        if not rows:
            return {
                "status": "not_found",
                "data": [],
                "message": "No products found for this category"
            }

        products = []
        for row in rows:
            products.append({
                "product_id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "sku": row[3],
                "requires_prescription": bool(row[4]),
            })

        return {
            "status": "success",
            "data": products,
            "message": "Products fetched"
        }

    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "message": str(e)
        }
