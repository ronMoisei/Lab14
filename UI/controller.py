# controller/controller_customers_sim6.py
import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        txtMinOrd = self._view._txtMinOrders.value
        txtMinShared = self._view._txtMinShared.value

        # validazioni
        if txtMinOrd == "" or txtMinShared == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire min_orders e min_shared.", color="red"))
            self._view.update_page()
            return
        try:
            min_orders = int(txtMinOrd)
            min_shared = int(txtMinShared)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Parametri interi richiesti.", color="red"))
            self._view.update_page()
            return
        if min_orders < 1 or min_shared < 1:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Valori devono essere >= 1.", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(min_orders, min_shared)
        nN, nE = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: nodi={nN}, archi={nE}"))

        # abilito i controlli successivi
        for c in (self._view._txtCust, self._view._btnComp, self._view._btnVicini,
                  self._view._txtCust2, self._view._btnShortest,
                  self._view._txtSeed, self._view._txtK, self._view._btnOttimo):
            c.disabled = False
        self._view.update_page()

    def handleComp(self, e):
        cid = self._parse_cid(self._view._txtCust.value)
        if cid is None: return
        c = self._model.getCustomer(cid)
        size = self._model.component_size(c)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Componente di {c}: size={size}"))
        self._view.update_page()

    def handleVicini(self, e):
        cid = self._parse_cid(self._view._txtCust.value)
        if cid is None: return
        c = self._model.getCustomer(cid)
        vic = self._model.neighbors_sorted(c)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Vicini di {c} per #brand condivisi:"))
        for v, w in vic:
            self._view.txt_result.controls.append(ft.Text(f"{v} — weight={w}"))
        self._view.update_page()

    def handleShortest(self, e):
        c1 = self._parse_cid(self._view._txtCust.value)
        c2 = self._parse_cid(self._view._txtCust2.value)
        if c1 is None or c2 is None: return
        s = self._model.getCustomer(c1)
        d = self._model.getCustomer(c2)
        path = self._model.shortest_path_unweighted(s, d)
        self._view.txt_result.controls.clear()
        if len(path) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato.", color="red"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Shortest path {s} → {d}:"))
            for n in path:
                self._view.txt_result.controls.append(ft.Text(str(n)))
        self._view.update_page()

    def handleOttimo(self, e):
        seed_id = self._parse_cid(self._view._txtSeed.value)
        if seed_id is None: return
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

        seed = self._model.getCustomer(seed_id)
        team, score = self._model.getOttimo(seed, K)
        self._view.txt_result.controls.clear()
        if len(team) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessuna soluzione trovata.", color="red"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Team ottimo K={K} da seed {seed} — brand coperti: {score}"))
            for m in team:
                self._view.txt_result.controls.append(ft.Text(str(m)))
        self._view.update_page()

    # --- helper ---
    def _parse_cid(self, txt):
        if txt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire customer_id.", color="red"))
            self._view.update_page()
            return None
        try:
            cid = int(txt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("customer_id non numerico.", color="red"))
            self._view.update_page()
            return None
        if not self._model.hasCustomer(cid):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Cliente non presente nel grafo.", color="red"))
            self._view.update_page()
            return None
        return cid
