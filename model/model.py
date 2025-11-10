# model/model_customers_sim4.py
import copy
import networkx as nx
from database.dao_customers_sim4 import DAO_CustomersSim4

class ModelCustomersSim4:
    def __init__(self):
        self._G = nx.Graph()
        self._customers = DAO_CustomersSim4.get_all_customers()
        self._idmap = {c.customer_id: c for c in self._customers}

        # ricorsione
        self._bestPath = []
        self._bestScore = float("inf")

    # ---------- grafo ----------
    def buildGraph(self, T):
        self._G.clear()
        self._G.add_nodes_from(self._customers)
        for u, v, w in DAO_CustomersSim4.get_edges_with_overlap(self._idmap, T):
            self._G.add_edge(u, v, overlap=w)

    def getGraphDetails(self):
        return self._G.number_of_nodes(), self._G.number_of_edges()

    def hasCustomer(self, cid: int):
        return cid in self._idmap

    def getCustomer(self, cid: int):
        return self._idmap[cid]

    # ---------- esercizi ----------
    def neighbors_sorted(self, c):
        vic = []
        for v in self._G.neighbors(c):
            vic.append((v, self._G[c][v]["overlap"]))
        vic.sort(key=lambda x: x[1], reverse=True)
        return vic  # [(neighbor, overlap), ...]

    def component_size(self, c):
        cc = nx.node_connected_component(self._G, c)
        return len(cc)

    def shortest_path(self, c1, c2):
        try:
            return nx.shortest_path(self._G, c1, c2)
        except nx.NetworkXNoPath:
            return []

    # ---------- ricorsione ----------
    def getOttimo(self, seed, K):
        """
        Team di K clienti nella componente di seed.
        Minimizza la somma degli overlap interni (diversificazione).
        """
        self._bestPath = []
        self._bestScore = float("inf")

        comp = nx.node_connected_component(self._G, seed)
        candidates = list(comp)

        parziale = [seed]
        self._ricorsione(parziale, K, candidates)
        return self._bestPath, (0 if not self._bestPath else self.getScore(self._bestPath))

    def _ricorsione(self, parziale, K, candidates):
        if len(parziale) == K:
            score = self.getScore(parziale)
            if score < self._bestScore:
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            return

        # scelta successivi solo tra candidati rimanenti non già selezionati
        for c in candidates:
            if c in parziale:
                continue
            parziale.append(c)
            self._ricorsione(parziale, K, candidates)
            parziale.pop()

    def getScore(self, team):
        """
        Somma degli overlap sugli archi interni al team.
        Se due clienti nel team non sono adiacenti, contributo 0.
        """
        s = 0
        n = len(team)
        for i in range(n):
            for j in range(i + 1, n):
                u, v = team[i], team[j]
                if self._G.has_edge(u, v):
                    s += self._G[u][v]["overlap"]
        return s
