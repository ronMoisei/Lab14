# model/model_products_sim5.py
import copy
import networkx as nx
from database.dao_products_sim5 import DAO_ProductsSim5

class ModelProductsSim5:
    def __init__(self):
        self._G = nx.Graph()
        self._products = DAO_ProductsSim5.get_all_products()
        self._idmap = {p.product_id: p for p in self._products}

        # ricorsione
        self._bestPath = []
        self._bestScore = 0

    # ---------- grafo ----------
    def buildGraph(self, min_weight: int):
        self._G.clear()
        self._G.add_nodes_from(self._products)
        for u, v, w in DAO_ProductsSim5.get_copurchase_edges(self._idmap, min_weight):
            self._G.add_edge(u, v, weight=w)

    def getGraphDetails(self):
        return self._G.number_of_nodes(), self._G.number_of_edges()

    def hasProduct(self, pid: int):
        return pid in self._idmap

    def getProduct(self, pid: int):
        return self._idmap[pid]

    # ---------- esercizi ----------
    def incident_volume(self, p):
        tot = 0
        for _, v, data in self._G.edges(p, data=True):
            tot += data.get("weight", 0)
        return tot

    def component_size(self, p):
        cc = nx.node_connected_component(self._G, p)
        return len(cc)

    def shortest_path_unweighted(self, p_src, p_dst):
        try:
            return nx.shortest_path(self._G, p_src, p_dst)
        except nx.NetworkXNoPath:
            return []

    def neighbors_sorted(self, p):
        vic = []
        for v in self._G.neighbors(p):
            vic.append((v, self._G[p][v]["weight"]))
        vic.sort(key=lambda x: x[1], reverse=True)
        return vic

    # ---------- ricorsione ----------
    def getOttimo(self, seed, K):
        """
        Bundle di K prodotti nella componente di 'seed' con:
        - obiettivo: massimizzare somma dei pesi degli archi interni al bundle
        - vincolo: al più 1 prodotto per category_id
        """
        self._bestPath = []
        self._bestScore = 0

        comp = list(nx.node_connected_component(self._G, seed))
        # seed deve essere incluso
        parziale = [seed]
        used_cat = {seed.category_id: 1}

        self._ricorsione(parziale, K, comp, used_cat)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, K, candidates, used_cat: dict):
        if len(parziale) == K:
            score = self.getScore(parziale)
            if score > self._bestScore:
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            return

        for prod in candidates:
            if prod in parziale:
                continue
            # vincolo: max 1 per category_id
            if prod.category_id in used_cat:
                continue

            parziale.append(prod)
            used_cat[prod.category_id] = 1
            self._ricorsione(parziale, K, candidates, used_cat)
            parziale.pop()
            used_cat.pop(prod.category_id, None)

    def getScore(self, bundle):
        """
        Somma dei pesi degli archi interni al bundle.
        Se due prodotti non adiacenti, contributo 0.
        """
        s = 0
        n = len(bundle)
        for i in range(n):
            for j in range(i + 1, n):
                u, v = bundle[i], bundle[j]
                if self._G.has_edge(u, v):
                    s += self._G[u][v]["weight"]
        return s
