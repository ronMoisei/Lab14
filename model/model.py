# model/model_customers_sim6.py
import copy
import networkx as nx
from database.dao_customers_sim6 import DAO_CustomersSim6

class ModelCustomersSim6:
    def __init__(self):
        self._G = nx.Graph()
        self._customers = []
        self._idmap = {}
        # supporto ricorsione
        self._cust_brands = {}  # customer -> set(brand_id)
        self._bestPath = []
        self._bestScore = 0

    # ---------- grafo ----------
    def buildGraph(self, min_orders: int, min_shared: int):
        self._G.clear()
        self._customers = DAO_CustomersSim6.get_customers_min_orders(min_orders)
        self._idmap = {c.customer_id: c for c in self._customers}
        self._G.add_nodes_from(self._customers)

        edges = DAO_CustomersSim6.get_edges_shared_brands(self._idmap, min_shared)
        for u, v, w in edges:
            self._G.add_edge(u, v, weight=w)

        # precompute brand coverage
        self._cust_brands = DAO_CustomersSim6.get_customer_brands(self._idmap)

    def getGraphDetails(self):
        return self._G.number_of_nodes(), self._G.number_of_edges()

    def hasCustomer(self, cid: int):
        return cid in self._idmap

    def getCustomer(self, cid: int):
        return self._idmap[cid]

    # ---------- esercizi ----------
    def component_size(self, cnode):
        cc = nx.node_connected_component(self._G, cnode)
        return len(cc)

    def neighbors_sorted(self, cnode):
        vic = []
        for v in self._G.neighbors(cnode):
            vic.append((v, self._G[cnode][v]["weight"]))
        vic.sort(key=lambda x: x[1], reverse=True)
        return vic

    def shortest_path_unweighted(self, src, dst):
        try:
            return nx.shortest_path(self._G, src, dst)
        except nx.NetworkXNoPath:
            return []

    # ---------- ricorsione ----------
    def getOttimo(self, seed, K: int):
        """
        Seleziona K clienti nella componente connessa di seed massimizzando
        la copertura di brand unici acquistati dal team.
        Score = | ∪_c brands(c) |.
        """
        self._bestPath = []
        self._bestScore = 0

        comp = list(nx.node_connected_component(self._G, seed))
        # seed incluso
        parziale = [seed]
        # unione brand corrente
        current_brands = set(self._cust_brands.get(seed, set()))

        self._ricorsione(parziale, K, comp, current_brands)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, K, candidates, current_brands: set):
        if len(parziale) == K:
            score = self.getScore(current_brands)
            if score > self._bestScore:
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            return

        for cust in candidates:
            if cust in parziale:
                continue
            # aggiungo
            parziale.append(cust)
            prev_size = len(current_brands)
            # aggiorno insieme brand (in place + rollback)
            add_brands = self._cust_brands.get(cust, set())
            # efficienza: union in place
            old_snapshot = None
            # salvo snapshot SOLO se necessario per rollback veloce
            if add_brands:
                old_snapshot = current_brands.copy()
                current_brands |= add_brands

            self._ricorsione(parziale, K, candidates, current_brands)

            # rollback
            parziale.pop()
            if add_brands:
                current_brands.clear()
                current_brands |= old_snapshot
            # se nessun brand aggiunto, nessuna azione

    def getScore(self, brands_union: set):
        return len(brands_union)
