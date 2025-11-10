# model/model_products_sim1.py
import copy
import networkx as nx
from database.DAO import DAO_ProdSim1

class ModelProdSim1:
    def __init__(self):
        self._G = nx.Graph()
        self._products = DAO_ProdSim1.get_all_products()
        self._idmap = {p.product_id: p for p in self._products}

        # campi per la ricorsione
        self._bestPath = []
        self._bestScore = 0

    # ---------- GRAFO ----------
    def buildGraph(self):
        self._G.clear()
        self._G.add_nodes_from(self._products)
        for e in DAO_ProdSim1.get_edges_copurchase(self._idmap):
            self._G.add_edge(e.o1, e.o2, weight=e.peso)

    def getGraphDetails(self):
        return self._G.number_of_nodes(), self._G.number_of_edges()

    def getAllNodes(self):
        return list(self._G.nodes())

    def getNeighborsSorted(self, p):
        vic = []
        for v in self._G.neighbors(p):
            vic.append((v, self._G[p][v]["weight"]))
        vic.sort(key=lambda x: x[1], reverse=True)
        return vic

    def edgeVolume(self, p):
        """
        Somma dei pesi degli archi incidenti a p.
        """
        vol = 0
        for v in self._G.neighbors(p):
            vol += self._G[p][v]["weight"]
        return vol

    def maxComponentSize(self):
        if self._G.number_of_nodes() == 0:
            return 0
        comps = nx.connected_components(self._G)
        return max(len(cc) for cc in comps)

    # ---------- RICORSIONE ----------
    def getOttimo(self, source, L):
        """
        Path semplice di lunghezza esatta L, tutto nella stessa categoria del source.
        Massimizza la somma dei pesi degli archi.
        """
        self._bestPath = []
        self._bestScore = 0

        if L < 2:
            return [], 0

        cat = source.category_id
        parziale = [source]

        # primo passo: solo vicini della stessa categoria
        for v in self._G.neighbors(source):
            if v.category_id == cat:
                parziale.append(v)
                self._ricorsione(parziale, L, cat)
                parziale.pop()

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, L, cat):
        # soluzione completa
        if len(parziale) == L:
            sc = self.getScore(parziale)
            if sc > self._bestScore:
                self._bestScore = sc
                self._bestPath = copy.deepcopy(parziale)
            return

        # altrimenti espando con nodi non ancora presenti e stessa categoria
        last = parziale[-1]
        for v in self._G.neighbors(last):
            if v in parziale:
                continue
            if v.category_id != cat:
                continue
            parziale.append(v)
            self._ricorsione(parziale, L, cat)
            parziale.pop()

    def getScore(self, path):
        """
        Somma pesi archi consecutivi del path.
        """
        if len(path) < 2:
            return 0
        tot = 0
        for i in range(len(path) - 1):
            tot += self._G[path[i]][path[i + 1]]["weight"]
        return tot
