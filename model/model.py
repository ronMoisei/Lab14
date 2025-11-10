# model/model_categories_sim8.py
import copy
import networkx as nx
from database.dao_categories_sim8 import DAO_CategoriesSim8

class ModelCategoriesSim8:
    def __init__(self):
        self._G = nx.Graph()
        self._categories = []
        self._idCat = {}
        self._cat_customers = {}  # Category -> set(customer_id)

        # ricorsione
        self._bestSet = []
        self._bestScore = 0

    # ------- grafo -------
    def buildGraph(self, min_shared_orders: int):
        self._G.clear()
        self._categories = DAO_CategoriesSim8.get_all_categories()
        self._idCat = {c.category_id: c for c in self._categories}
        self._G.add_nodes_from(self._categories)

        for u, v, w in DAO_CategoriesSim8.get_edges_cocart(self._idCat, min_shared_orders):
            self._G.add_edge(u, v, weight=w)

        self._cat_customers = DAO_CategoriesSim8.get_customers_by_category(self._idCat)

    def getGraphDetails(self):
        return self._G.number_of_nodes(), self._G.number_of_edges()

    def hasCategory(self, cid: int):
        return cid in self._idCat

    def getCategory(self, cid: int):
        return self._idCat[cid]

    # ------- esercizi -------
    def longest_component_size_from(self, category):
        cc = nx.node_connected_component(self._G, category)
        return len(cc)

    def neighbors_sorted(self, category):
        res = []
        for v in self._G.neighbors(category):
            res.append((v, self._G[category][v]["weight"]))
        res.sort(key=lambda x: x[1], reverse=True)
        return res

    def shortest_path_unweighted(self, src, dst):
        try:
            return nx.shortest_path(self._G, src, dst)
        except nx.NetworkXNoPath:
            return []

    # ------- ricorsione -------
    def getOttimo(self, seed_category, K: int):
        """
        Seleziona K categorie nella componente del seed massimizzando
        il numero di clienti distinti coperti.
        """
        self._bestSet = []
        self._bestScore = 0

        comp = list(nx.node_connected_component(self._G, seed_category))
        parziale = [seed_category]
        current_customers = set(self._cat_customers.get(seed_category, set()))

        self._ricorsione(parziale, K, comp, current_customers)
        return self._bestSet, self._bestScore

    def _ricorsione(self, parziale, K, candidates, current_customers: set):
        if len(parziale) == K:
            score = self.getScore(current_customers)
            if score > self._bestScore:
                self._bestScore = score
                self._bestSet = copy.deepcopy(parziale)
            return

        for cat in candidates:
            if cat in parziale:
                continue
            parziale.append(cat)
            add = self._cat_customers.get(cat, set())
            if add:
                snap = current_customers.copy()
                current_customers |= add
                self._ricorsione(parziale, K, candidates, current_customers)
                current_customers.clear(); current_customers |= snap
            else:
                self._ricorsione(parziale, K, candidates, current_customers)
            parziale.pop()

    def getScore(self, customers_union: set):
        return len(customers_union)
