# controller/controller_products_sim5.py
import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        txt = self._view._txtSoglia.value
        if txt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire soglia minimo co-purchase.", color="red"))
            self._view.update_page()
            return
        try:
            T = int(txt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("La soglia deve essere intera.", color="red"))
            self._view.update_page()
            return
        if T <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("La soglia deve essere > 0.", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(T)
        nN, nE = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: nodi={nN}, archi={nE}"))
        # abilito controlli
        for c in (self._view._txtProd, self._view._btnVolume, self._view._btnVicini,
                  self._view._btnComp, self._view._txtProd2, self._view._btnShortest,
                  self._view._txtK, self._view._btnOttimo):
            c.disabled = False
        self._view.update_page()

    def handleVolume(self, e):
        p = self._parse_pid(self._view._txtProd.value)
        if p is None: return
        prod = self._model.getProduct(p)
        vol = self._model.incident_volume(prod)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Incident volume di {prod}: {vol}"))
        self._view.update_page()

    def handleVicini(self, e):
        p = self._parse_pid(self._view._txtProd.value)
        if p is None: return
        prod = self._model.getProduct(p)
        vic = self._model.neighbors_sorted(prod)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Vicini di {prod} (peso desc):"))
        for v, w in vic:
            self._view.txt_result.controls.append(ft.Text(f"{v} — weight: {w}"))
        self._view.update_page()

    def handleComp(self, e):
        p = self._parse_pid(self._view._txtProd.value)
        if p is None: return
        prod = self._model.getProduct(p)
        size = self._model.component_size(prod)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Size componente connessa di {prod}: {size}"))
        self._view.update_page()

    def handleShortest(self, e):
        p1 = self._parse_pid(self._view._txtProd.value);   p2 = self._parse_pid(self._view._txtProd2.value)
        if p1 is None or p2 is None: return
        src = self._model.getProduct(p1); dst = self._model.getProduct(p2)
        path = self._model.shortest_path_unweighted(src, dst)
        self._view.txt_result.controls.clear()
        if len(path) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato.", color="red"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Shortest path {src} → {dst}:"))
            for n in path:
                self._view.txt_result.controls.append(ft.Text(str(n)))
        self._view.update_page()

    def handleOttimo(self, e):
        pid = self._parse_pid(self._view._txtProd.value)
        if pid is None: return
        txtK = self._view._txtK.value
        if txtK == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire K.", color="red"))
            self._view.update_page()
            return
        try:
            K = int(txtK)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("K deve essere intero.", color="red"))
            self._view.update_page()
            return
        if K < 1:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("K deve essere >= 1.", color="red"))
            self._view.update_page()
            return

        seed = self._model.getProduct(pid)
        bundle, score = self._model.getOttimo(seed, K)
        self._view.txt_result.controls.clear()
        if len(bundle) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessuna soluzione trovata.", color="red"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Bundle ottimo K={K} da seed {seed} — score interno={score}"))
            for n in bundle:
                self._view.txt_result.controls.append(ft.Text(str(n)))
        self._view.update_page()

    # --- helpers ---
    def _parse_pid(self, txt):
        if txt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire product_id.", color="red"))
            self._view.update_page()
            return None
        try:
            pid = int(txt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("product_id non numerico.", color="red"))
            self._view.update_page()
            return None
        if not self._model.hasProduct(pid):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Prodotto non presente.", color="red"))
            self._view.update_page()
            return None
        return pid
