# controller/controller_orders_products_sim3.py
import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._model.buildGraph()
        nNodi, nArchi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo bipartito creato. Nodi={nNodi}, Archi={nArchi}."))
        # abilito controlli
        self._view._txtIdProd.disabled = False
        self._view._btnVolume.disabled = False
        self._view._btnMaxCC.disabled = False
        self._view._txtIdProd2.disabled = False
        self._view._btnShortest.disabled = False
        self._view._ddL.disabled = False
        self._view._btnBest.disabled = False

        # popolo L: lunghezze plausibili
        self._view._ddL.options = list(map(lambda x: ft.dropdown.Option(x), list(range(2, 11))))
        self._view.update_page()

    def handleVolume(self, e):
        txt = self._view._txtIdProd.value
        if txt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire product_id.", color="red"))
            self._view.update_page()
            return
        try:
            pid = int(txt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("product_id deve essere numerico.", color="red"))
            self._view.update_page()
            return
        if not self._model.hasProduct(pid):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Prodotto non presente.", color="red"))
            self._view.update_page()
            return

        p = self._model.getProductById(pid)
        vol = self._model.productIncidentVolume(p)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Incident volume di {p}: {vol}"))
        self._view.update_page()

    def handleMaxCC(self, e):
        size = self._model.maxComponentSize()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Dimensione max componente connessa: {size}"))
        self._view.update_page()

    def handleShortest(self, e):
        t1 = self._view._txtIdProd.value
        t2 = self._view._txtIdProd2.value
        if t1 == "" or t2 == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire due product_id.", color="red"))
            self._view.update_page()
            return
        try:
            p1, p2 = int(t1), int(t2)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Gli id devono essere numerici.", color="red"))
            self._view.update_page()
            return
        if not self._model.hasProduct(p1) or not self._model.hasProduct(p2):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Prodotto non presente nel grafo.", color="red"))
            self._view.update_page()
            return

        src = self._model.getProductById(p1)
        dst = self._model.getProductById(p2)
        path = self._model.shortestProductToProduct(src, dst)

        self._view.txt_result.controls.clear()
        if len(path) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino alternato trovato.", color="red"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Shortest alternating path {src} → {dst}:"))
            for n in path:
                self._view.txt_result.controls.append(ft.Text(str(n)))
        self._view.update_page()

    def handleBest(self, e):
        t = self._view._txtIdProd.value
        if t == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire product_id di partenza.", color="red"))
            self._view.update_page()
            return
        try:
            pid = int(t)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("product_id deve essere numerico.", color="red"))
            self._view.update_page()
            return
        if not self._model.hasProduct(pid):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Prodotto non presente nel grafo.", color="red"))
            self._view.update_page()
            return

        Lval = self._view._ddL.value
        if Lval is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare L.", color="red"))
            self._view.update_page()
            return
        L = int(Lval)

        p0 = self._model.getProductById(pid)
        path, score = self._model.getOttimo(p0, L)

        self._view.txt_result.controls.clear()
        if len(path) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino che rispetta i vincoli.", color="red"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino ottimo di lunghezza {L} da {p0} con score totale {score}."))
            for n in path:
                self._view.txt_result.controls.append(ft.Text(str(n)))
        self._view.update_page()
