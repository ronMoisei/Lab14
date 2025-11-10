# model/model_stores_sim2.py
import copy
import networkx as nx
from database.dao_stores_sim2 import DAO_StoresSim2

class ModelStoresSim2:
    def __init__(self):
        self._G = nx.DiGraph()
        self._stores = DAO_StoresSim2.get_all_stores()
        self._idmap = {s.store_id: s for s in self._stores}

        # campi per la ricorsione
        self._bestPath = []
        self._bestScore = 0

    # ---------- GRAFO ----------
    def buildGraph(self):
        """
        Crea il grafo diretto pesato delle transizioni tra store.
        """
        self._G.clear()
        self._G.add_nodes_from(self._stores)
        for e in DAO_StoresSim2.get_transition_edges(self._idmap):
            # e.o1 -> e.o2 con peso e.peso
            self._G.add_edge(e.o1, e.o2, weight=e.peso)

    def getGraphDetails(self):
        return self._G.number_of_nodes(), self._G.number_of_edges()

    def getAllNodes(self):
        return list(self._G.nodes())

    def outVolume(self, s):
        """
        Somma dei pesi degli archi uscenti dallo store s.
        """
        vol = 0
        for _, v, data in self._G.out_edges(s, data=True):
            vol += data["weight"]
        return vol

    def getReachableBFS(self, s):
        """
        Nodi raggiungibili da s via BFS sui soli archi diretti.
        Restituisce i nodi escluso s.
        """
        tree = nx.bfs_tree(self._G, s)  # su DiGraph: segue la direzione
        nodes = list(tree.nodes())
        return nodes[1:]  # escluso s

    def getIdMap(self):
        return self._idmap

    def hasNode(self, store_id: int):
        return store_id in self._idmap

    def getObjectFromId(self, store_id: int):
        return self._idmap[store_id]

    # ---------- RICORSIONE ----------
    def getOttimo(self, start, L):
        """
        Cammino semplice diretto di lunghezza esatta L a pesi strettamente decrescenti.
        Massimizza la somma dei pesi.
        L >= 2: numero di nodi nel path.
        """
        self._bestPath = []
        self._bestScore = 0

        if L < 2:
            return [], 0

        parziale = [start]
        # primo passo: proviamo ogni vicino uscente
        for v in self._G.successors(start):
            parziale.append(v)
            self._ricorsione(parziale, L)
            parziale.pop()

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, L):
        # Se ho raggiunto L nodi, valuto la soluzione e termino
        if len(parziale) == L:
            sc = self.getScore(parziale)
            if sc > self._bestScore:
                self._bestScore = sc
                self._bestPath = copy.deepcopy(parziale)
            return

        # Espansione: rispetto il vincolo "peso nuovo < peso precedente"
        u_prev = parziale[-2]
        u = parziale[-1]
        w_prev = self._G[u_prev][u]["weight"]

        for v in self._G.successors(u):
            if v in parziale:
                continue
            w_new = self._G[u][v]["weight"]
            if w_new < w_prev:
                parziale.append(v)
                self._ricorsione(parziale, L)
                parziale.pop()

    def getScore(self, path):
        """
        Somma dei pesi sugli archi consecutivi del path diretto.
        """
        if len(path) < 2:
            return 0
        tot = 0
        for i in range(len(path) - 1):
            tot += self._G[path[i]][path[i + 1]]["weight"]
        return tot
