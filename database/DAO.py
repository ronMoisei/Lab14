# database/dao_products_sim1.py
from database.DB_connect import DBConnect
from model.product import Product
from model.arco import Arco  # dataclass: o1, o2, peso

class DAO_ProdSim1:

    @staticmethod
    def get_all_products():
        """
        Tutti i prodotti come vertici del grafo.
        """
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM products"
        cursor.execute(query)
        res = [Product(**row) for row in cursor]
        cursor.close(); conn.close()
        return res

    @staticmethod
    def get_edges_copurchase(idmap):
        """
        Coppie di prodotti che compaiono nello stesso ordine.
        weight = numero ordini condivisi.
        """
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT oi1.product_id AS p1, oi2.product_id AS p2, COUNT(*) AS peso
        FROM order_items oi1, order_items oi2
        WHERE oi1.order_id = oi2.order_id
          AND oi1.product_id < oi2.product_id
        GROUP BY oi1.product_id, oi2.product_id
        """
        cursor.execute(query)

        res = []
        for row in cursor:
            p1, p2, w = row["p1"], row["p2"], row["peso"]
            if p1 in idmap and p2 in idmap and w > 0:
                res.append(Arco(idmap[p1], idmap[p2], w))
        cursor.close(); conn.close()
        return res
