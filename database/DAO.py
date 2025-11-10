# database/dao_categories_sim8.py
from database.DB_connect import DBConnect
from model.category import Category  # dataclass con __hash__ e __str__

class DAO_CategoriesSim8:

    @staticmethod
    def get_all_categories():
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = "SELECT category_id, category_name FROM categories"
        cur.execute(q)
        res = [Category(**row) for row in cur]
        cur.close(); conn.close()
        return res

    @staticmethod
    def get_edges_cocart(idmap_categories: dict, min_shared_orders: int):
        """
        Edge {c1,c2} con peso = #ordini distinti che contengono almeno
        un prodotto di c1 e almeno un prodotto di c2.
        Filtra con HAVING peso >= min_shared_orders.
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        WITH order_cat AS (
            SELECT o.order_id, p.category_id
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            JOIN products p ON p.product_id = oi.product_id
            GROUP BY o.order_id, p.category_id
        )
        SELECT oc1.category_id AS c1, oc2.category_id AS c2, COUNT(*) AS w
        FROM order_cat oc1
        JOIN order_cat oc2
          ON oc1.order_id = oc2.order_id
         AND oc1.category_id < oc2.category_id
        GROUP BY oc1.category_id, oc2.category_id
        HAVING COUNT(*) >= %s
        """
        cur.execute(q, (min_shared_orders,))
        edges = []
        for row in cur:
            c1, c2, w = row["c1"], row["c2"], row["w"]
            if c1 in idmap_categories and c2 in idmap_categories:
                edges.append((idmap_categories[c1], idmap_categories[c2], w))
        cur.close(); conn.close()
        return edges

    @staticmethod
    def get_customers_by_category(idmap_categories: dict):
        """
        Mappa: Category -> set(customer_id) che hanno acquistato almeno un prodotto di tale categoria.
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT DISTINCT p.category_id, o.customer_id
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        """
        cur.execute(q)
        cmap = {c: set() for c in idmap_categories.values()}
        for row in cur:
            cid = row["category_id"]
            if cid in idmap_categories:
                cmap[idmap_categories[cid]].add(row["customer_id"])
        cur.close(); conn.close()
        return cmap
