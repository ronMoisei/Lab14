# model/model_brands_sim7.py
import copy
import networkx as nx
from database.dao_brands_sim7 import DAO_BrandsSim7

class ModelBrandsSim7:
    def __init__(self):
        self._G = nx.DiGraph()
        self._brands = []
        self._products = []
        self._idBrands = {}
        self._idProducts = {}

        # ricorsione
        self._bestPath = []
        self._bestScore = float('inf')

    # ---------- grafo ----------
    def buildGraph(self):
        self._G.clear()
        self._brands = DAO_BrandsSim7.get_all_brands()
        self._idBrands = {b.brand_id: b for b in self._brands}

        self._products = DAO_BrandsSim7.get_all_products(self._idBrands)
        self._idProducts = {p.product_id: p for p in self._products}

        # aggiungi archi brand→product
        for p in self._products:
            b = self._idBrands[p.brand_id]
            self._G.add_edge(b, p, weight=p.list_price)

        # aggiungi archi product→brand2 (collaborazioni)
        for p1, b2id, cost in DAO_BrandsSim7.get_collab_edges(self._idProducts):
            if b2id in self._idBrands:
                self._G.add_edge(p1, self._idBrands[b2id], weight=cost)

    def getGraphDetails(self):
        return self._G.number_of_nodes(), self._G.number_of_edges()

    # ---------- esercizi ----------
    def isReachable(self, b1, b2):
        return nx.has_path(self._G, b1, b2)

    def shortest_path_min_cost(self, b1, b2):
        try:
            return nx.shortest_path(self._G, b1, b2, weight="weight"), nx.shortest_path_length(self._G, b1, b2, weight="weight")
        except nx.NetworkXNoPath:
            return [], None

    def neighbors_sorted(self, node):
        succ = []
        for v in self._G.successors(node):
            succ.append((v, self._G[node][v]["weight"]))
        succ.sort(key=lambda x: x[1])
        return succ

    # ---------- ricorsione ----------
    def getOttimo(self, seed, K):
        """
        Minimizza il costo medio tra brand raggiungibili.
        """
        self._bestPath = []
        self._bestScore = float('inf')

        reachables = [n for n in self._G.nodes if nx.has_path(self._G, seed, n)]
        parziale = [seed]
        current_cost = 0
        self._ricorsione(parziale, K, reachables, current_cost)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, K, candidates, current_cost):
        if len(parziale) == K:
            score = self.getScore(current_cost, K)
            if score < self._bestScore:
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            return

        last = parziale[-1]
        for succ in self._G.successors(last):
            if succ in parziale:
                continue
            cost = self._G[last][succ]["weight"]
            parziale.append(succ)
            self._ricorsione(parziale, K, candidates, current_cost + cost)
            parziale.pop()

    def getScore(self, total_cost, k):
        """
        Minimizza il costo medio.
        """
        return total_cost / k if k > 0 else float('inf')
