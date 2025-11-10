# database/dao_orders_products_sim3.py
from database.DB_connect import DBConnect
from model.product import Product
from model.order import Order  # dataclass con almeno order_id

class DAO_OrdersProductsSim3:

    @staticmethod
    def get_all_products():
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = "SELECT * FROM products"
        cur.execute(q)
        res = [Product(**row) for row in cur]
        cur.close(); conn.close()
        return res

    @staticmethod
    def get_all_orders():
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = "SELECT * FROM orders"
        cur.execute(q)
        res = [Order(**row) for row in cur]
        cur.close(); conn.close()
        return res

    @staticmethod
    def get_edges_order_product(idmap_orders, idmap_products):
        """
        Crea archi order–product con peso = SUM(quantity) per quella coppia.
        MultiGraph: aggiungiamo un arco per ciascuna riga, ma qui torniamo
        già aggregato per robustezza.
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT oi.order_id AS oid, oi.product_id AS pid, SUM(oi.quantity) AS qty
        FROM order_items oi
        GROUP BY oi.order_id, oi.product_id
        """
        cur.execute(q)
        res = []
        for row in cur:
            oid, pid, qty = row["oid"], row["pid"], row["qty"]
            if oid in idmap_orders and pid in idmap_products and qty is not None and qty > 0:
                res.append((idmap_orders[oid], idmap_products[pid], qty))
        cur.close(); conn.close()
        return res
