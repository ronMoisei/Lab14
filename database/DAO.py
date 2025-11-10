# database/dao_products_sim5.py
from database.DB_connect import DBConnect
from model.product import Product  # dataclass con product_id, product_name, brand_id, category_id, list_price

class DAO_ProductsSim5:

    @staticmethod
    def get_all_products():
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        # Portiamo anche brand_id e category_id per il vincolo di diversità
        q = """
        SELECT p.product_id, p.product_name, p.brand_id, p.category_id, p.list_price
        FROM products p
        """
        cur.execute(q)
        res = [Product(**row) for row in cur]
        cur.close(); conn.close()
        return res

    @staticmethod
    def get_copurchase_edges(idmap, min_weight: int):
        """
        Archi {p1,p2} con weight = #ordini in cui p1 e p2 sono co-presenti.
        min_weight: soglia minima sul peso.
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT oi1.product_id AS p1, oi2.product_id AS p2, COUNT(DISTINCT oi1.order_id) AS w
        FROM order_items oi1
        JOIN order_items oi2
          ON oi1.order_id = oi2.order_id
         AND oi1.product_id < oi2.product_id
        GROUP BY oi1.product_id, oi2.product_id
        HAVING w >= %s
        """
        cur.execute(q, (min_weight,))
        edges = []
        for row in cur:
            p1, p2, w = row["p1"], row["p2"], row["w"]
            if p1 in idmap and p2 in idmap:
                edges.append((idmap[p1], idmap[p2], w))
        cur.close(); conn.close()
        return edges
