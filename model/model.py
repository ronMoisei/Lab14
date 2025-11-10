# model/model_orders_products_sim3.py
import copy
import networkx as nx
from database.dao_orders_products_sim3 import DAO_OrdersProductsSim3

class ModelOrdersProductsSim3:
    def __init__(self):
        self._G = nx.MultiGraph()  # bipartito U=orders, V=products
        self._products = DAO_OrdersProductsSim3.get_all_products()
        self._orders = DAO_OrdersProductsSim3.get_all_orders()

        # id maps
        self._idmap_prod = {p.product_id: p for p in self._products}
        self._idmap_ord = {o.order_id: o for o in self._orders}

        # ricorsione
        self._bestPath = []
        self._bestScore = 0

    # --------- GRAFO ----------
    def buildGraph(self):
        self._G.clear()
        # tag bipartizione per networkx (attributo 'bipartite': 0=orders, 1=products)
        self._G.add_nodes_from(self._orders, bipartite=0)
        self._G.add_nodes_from(self._products, bipartite=1)

        for o, p, qty in DAO_OrdersProductsSim3.get_edges_order_product(self._idmap_ord, self._idmap_prod):
            # MultiGraph: un edge con attr 'weight' = qty
            self._G.add_edge(o, p, weight=qty)

    def getGraphDetails(self):
        return self._G.number_of_nodes(), self._G.number_of_edges()

    def getAllProducts(self):
        return list(self._products)

    def hasProduct(self, pid: int):
        return pid in self._idmap_prod

    def getProductById(self, pid: int):
        return self._idmap_prod[pid]

    # --------- ESERCIZI ----------
    def productIncidentVolume(self, p):
        """
        Somma dei 'weight' su tutti gli archi incidenti al prodotto p.
        MultiGraph: sommiamo su tutte le key di edge paralleli.
        """
        vol = 0
        for u, v, k, data in self._G.edges(p, keys=True, data=True):
            vol += data.get("weight", 0)
        return vol

    def maxComponentSize(self):
        if self._G.number_of_nodes() == 0:
            return 0
        return max(len(cc) for cc in nx.connected_components(self._G))

    def shortestProductToProduct(self, p_src, p_dst):
        """
        Cammino alternato minimo (ignora pesi) tra due prodotti.
        Usa BFS sul multigrafo.
        """
        if p_src == p_dst:
            return [p_src]
        try:
            # su MultiGraph shortest_path usa un grafo semplice sottostante; va bene per alternanza U-V
            path = nx.shortest_path(self._G, source=p_src, target=p_dst)
            # verifica alternanza: Product-Order-Product-...
            return path
        except nx.NetworkXNoPath:
            return []

    # --------- RICORSIONE ----------
    def getOttimo(self, p_start, L):
        """
        Cammino semplice alternato di lunghezza esatta L nodi.
        Indici pari = Product, indici dispari = Order.
        Vincolo: pesi archi strettamente decrescenti.
        Massimizza somma dei pesi.
        """
        self._bestPath = []
        self._bestScore = 0
        if L < 2:
            return [], 0

        parziale = [p_start]
        # primo passo: deve andare a un Order
        for neigh in self._G.neighbors(p_start):
            if getattr(neigh, "order_id", None) is not None:  # è un Order
                # peso dell'arco multi: sommo tutti i paralleli oppure prendo max?
                # coerente con edges aggregati → prendo la somma sulle parallel edges:
                w = self._edge_weight_total(p_start, neigh)
                parziale.append(neigh)
                self._ricorsione(parziale, L, last_w=w)
                parziale.pop()

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, L, last_w):
        # soluzione completa
        if len(parziale) == L:
            sc = self.getScore(parziale)
            if sc > self._bestScore:
                self._bestScore = sc
                self._bestPath = copy.deepcopy(parziale)
            return

        u_prev = parziale[-2]
        u = parziale[-1]

        # alternanza: se u è Order, prossimi devono essere Product; se u è Product, prossimi Order
        want_order = getattr(u, "product_id", None) is not None  # se è Product, voglio Order
        for v in self._G.neighbors(u):
            if v in parziale:
                continue

            is_order = getattr(v, "order_id", None) is not None
            if want_order and not is_order:
                continue
            if not want_order and is_order:
                continue

            w_new = self._edge_weight_total(u, v)
            if w_new < last_w:
                parziale.append(v)
                self._ricorsione(parziale, L, last_w=w_new)
                parziale.pop()

    def getScore(self, path):
        """
        Somma dei pesi sugli archi consecutivi del path in MultiGraph.
        Usiamo il totale delle parallel edges tra i due estremi.
        """
        if len(path) < 2:
            return 0
        tot = 0
        for i in range(len(path) - 1):
            tot += self._edge_weight_total(path[i], path[i + 1])
        return tot

    def _edge_weight_total(self, u, v):
        """
        In un MultiGraph ci possono essere più archi u-v con 'weight'.
        Sommiamo tutte le chiavi.
        """
        total = 0
        if self._G.has_edge(u, v):
            # edges(u, v, data=True, keys=True) per iterare sugli archi paralleli
            for k, data in self._G[u][v].items():
                total += data.get("weight", 0)
        return total
