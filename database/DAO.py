# database/dao_stores_sim2.py
from database.DB_connect import DBConnect
from model.store import Store
from model.arco import Arco  # dataclass: o1, o2, peso

class DAO_StoresSim2:

    @staticmethod
    def get_all_stores():
        """
        Restituisce tutti gli store come nodi del grafo.
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = "SELECT * FROM stores"
        cur.execute(q)
        res = [Store(**row) for row in cur]
        cur.close(); conn.close()
        return res

    @staticmethod
    def get_transition_edges(idmap):
        """
        Costruisce archi diretti tra store sulla base delle transizioni cliente:
        per ogni cliente, ordini ordinati per data. Per ogni coppia di ordini
        consecutivi (o1 -> o2) con store diversi, aggiunge transizione store(o1) -> store(o2).
        Peso = count transizioni.
        Implementazione SQL classica: self join + 'successivo ordine' via subquery MIN(data > ...).
        """
        conn = DBConnect.get_connection()
        cur = conn.cursor(dictionary=True)
        q = """
        SELECT o1.store_id AS s1, o2.store_id AS s2, COUNT(*) AS peso
        FROM orders o1, orders o2
        WHERE o1.customer_id = o2.customer_id
          AND o1.store_id <> o2.store_id
          AND o2.order_date = (
                SELECT MIN(o3.order_date)
                FROM orders o3
                WHERE o3.customer_id = o1.customer_id
                  AND o3.order_date > o1.order_date
          )
        GROUP BY o1.store_id, o2.store_id
        """
        cur.execute(q)
        res = []
        for row in cur:
            s1, s2, w = row["s1"], row["s2"], row["peso"]
            if s1 in idmap and s2 in idmap and w > 0:
                res.append(Arco(idmap[s1], idmap[s2], w))
        cur.close(); conn.close()
        return res
