# database/dao_customers_sim4.py
from database.DB_connect import DBConnect
from model.customer import Customer

class DAO_CustomersSim4:

    @staticmethod
    def get_all_customers():
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = "SELECT * FROM customers"
        cur.execute(q)
        res = [Customer(**row) for row in cur]
        cur.close(); conn.close()
        return res

    @staticmethod
    def get_edges_with_overlap(idmap, threshold):
        """
        Coppie di clienti con numero di prodotti distinti comprati in comune >= threshold.
        overlap = COUNT(DISTINCT product_id in comune).
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT c1.customer_id AS u, c2.customer_id AS v, COUNT(DISTINCT oi1.product_id) AS overlap_cnt
        FROM orders o1, orders o2, order_items oi1, order_items oi2,
             customers c1, customers c2
        WHERE c1.customer_id = o1.customer_id
          AND c2.customer_id = o2.customer_id
          AND oi1.order_id = o1.order_id
          AND oi2.order_id = o2.order_id
          AND c1.customer_id < c2.customer_id
          AND oi1.product_id = oi2.product_id
        GROUP BY c1.customer_id, c2.customer_id
        HAVING overlap_cnt >= %s
        """
        cur.execute(q, (threshold,))
        edges = []
        for row in cur:
            u, v, w = row["u"], row["v"], row["overlap_cnt"]
            if u in idmap and v in idmap:
                edges.append((idmap[u], idmap[v], w))
        cur.close(); conn.close()
        return edges
