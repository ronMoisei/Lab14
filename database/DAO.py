# database/dao_customers_sim6.py
from database.DB_connect import DBConnect
from model.customer import Customer  # dataclass: customer_id, first_name, last_name, email, __hash__/__str__

class DAO_CustomersSim6:

    @staticmethod
    def get_customers_min_orders(min_orders: int):
        """
        Prende i clienti con almeno min_orders ordini.
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT c.customer_id, c.first_name, c.last_name, c.email
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        HAVING COUNT(DISTINCT o.order_id) >= %s
        """
        cur.execute(q, (min_orders,))
        res = [Customer(**row) for row in cur]
        cur.close(); conn.close()
        return res

    @staticmethod
    def get_edges_shared_brands(idmap: dict, min_shared: int):
        """
        Crea archi tra clienti con #brand condivisi >= min_shared.
        weight = #brand condivisi.
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT t1.customer_id AS c1, t2.customer_id AS c2, COUNT(DISTINCT t1.brand_id) AS w
        FROM (
            SELECT o.customer_id, p.brand_id
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            JOIN products p ON p.product_id = oi.product_id
            GROUP BY o.customer_id, p.brand_id
        ) t1
        JOIN (
            SELECT o.customer_id, p.brand_id
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            JOIN products p ON p.product_id = oi.product_id
            GROUP BY o.customer_id, p.brand_id
        ) t2
              ON t1.brand_id = t2.brand_id
             AND t1.customer_id < t2.customer_id
        GROUP BY t1.customer_id, t2.customer_id
        HAVING w >= %s
        """
        cur.execute(q, (min_shared,))
        edges = []
        for row in cur:
            c1, c2, w = row["c1"], row["c2"], row["w"]
            if c1 in idmap and c2 in idmap:
                edges.append((idmap[c1], idmap[c2], w))
        cur.close(); conn.close()
        return edges

    @staticmethod
    def get_customer_brands(idmap: dict):
        """
        Mappa: customer -> set(brand_id) acquistati.
        Serve per lo score della ricorsione (copertura brand).
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT o.customer_id, p.brand_id
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY o.customer_id, p.brand_id
        """
        cur.execute(q)
        brandmap = {c: set() for c in idmap.values()}
        for row in cur:
            cid = row["customer_id"]
            if cid in idmap:
                brandmap[idmap[cid]].add(row["brand_id"])
        cur.close(); conn.close()
        return brandmap
