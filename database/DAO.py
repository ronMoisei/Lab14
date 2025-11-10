# database/dao_brands_sim7.py
from database.DB_connect import DBConnect
from model.brand import Brand
from model.product import Product

class DAO_BrandsSim7:

    @staticmethod
    def get_all_brands():
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = "SELECT brand_id, brand_name FROM brands"
        cur.execute(q)
        res = [Brand(**row) for row in cur]
        cur.close(); conn.close()
        return res

    @staticmethod
    def get_all_products(idmap_brands: dict):
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT product_id, product_name, brand_id, list_price
        FROM products
        """
        cur.execute(q)
        products = []
        for row in cur:
            if row["brand_id"] in idmap_brands:
                products.append(Product(**row))
        cur.close(); conn.close()
        return products

    @staticmethod
    def get_collab_edges(idmap_products: dict):
        """
        Crea archi product→brand2 se due brand hanno prodotti venduti nello stesso store.
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT p1.product_id AS p1, p2.brand_id AS b2, AVG(p2.list_price) AS cost
        FROM order_items oi1
        JOIN orders o1 ON oi1.order_id = o1.order_id
        JOIN products p1 ON p1.product_id = oi1.product_id
        JOIN order_items oi2 ON oi2.order_id = o1.order_id
        JOIN products p2 ON p2.product_id = oi2.product_id
        WHERE p1.brand_id <> p2.brand_id
        GROUP BY p1.product_id, p2.brand_id
        """
        cur.execute(q)
        edges = []
        for row in cur:
            if row["p1"] in idmap_products:
                edges.append((idmap_products[row["p1"]], row["b2"], row["cost"]))
        cur.close(); conn.close()
        return edges
