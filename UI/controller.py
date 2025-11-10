# controller/controller_brands_sim7.py
import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleBuild(self, e):
        self._model.buildGraph()
        n, ecount = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo diretto costruito. Nodi={n}, Archi={ecount}"))
        for c in (self._view._txtIdA, self._view._txtIdB, self._view._txtSeed, self._view._txtK):
            c.disabled = False
        self._view._btnReach.disabled = False
        self._view._btnShortest.disabled = False
        self._view._btnVicini.disabled = False
        self._view._btnOttimo.disabled = False
        self._view.update_page()

    def handleReach(self, e):
        a = self._parse_id(self._view._txtIdA.value)
        b = self._parse_id(self._view._txtIdB.value)
        if a is None or b is None: return
        b1 = self._model._idBrands[a]; b2 = self._model._idBrands[b]
        res = self._model.isReachable(b1, b2)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Raggiungibilità {b1} → {b2}: {res}"))
        self._view.update_page()

    def handleShortest(self, e):
        a = self._parse_id(self._view._txtIdA.value)
        b = self._parse_id(self._view._txtIdB.value)
        if a is None or b is None: return
        b1 = self._model._idBrands[a]; b2 = self._model._idBrands[b]
        path, cost = self._model.shortest_path_min_cost(b1, b2)
        self._view.txt_result.controls.clear()
        if not path:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato.", color="red"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Cammino minimo costo={cost:.2f}"))
            for n in path:
                self._view.txt_result.controls.append(ft.Text(str(n)))
        self._view.update_page()

    def handleVicini(self, e):
        a = self._parse_id(self._view._txtIdA.value)
        if a is None: return
        node = self._model._idBrands[a]
        vic = self._model.neighbors_sorted(node)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Successori di {node}:"))
        for v, w in vic:
            self._view.txt_result.controls.append(ft.Text(f"{v} — costo={w:.2f}"))
        self._view.update_page()

    def handleOttimo(self, e):
        a = self._parse_id(self._view._txtSeed.value)
        ktxt = self._view._txtK.value
        if a is None or ktxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire seed brand_id e K.", color="red"))
            self._view.update_page()
            return
        try:
            K = int(ktxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("K intero.", color="red"))
            self._view.update_page()
            return
        seed = self._model._idBrands[a]
        path, score = self._model.getOttimo(seed, K)
        self._view.txt_result.controls.clear()
        if not path:
            self._view.txt_result.controls.append(ft.Text("Nessun percorso ottimo.", color="red"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Percorso ottimo (costo medio min={score:.2f}):"))
            for p in path:
                self._view.txt_result.controls.append(ft.Text(str(p)))
        self._view.update_page()

    def _parse_id(self, txt):
        try:
            return int(txt)
        except:
            self._view.txt_result.controls.append(ft.Text("ID non valido.", color="red"))
            return None
