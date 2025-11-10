# controller/controller_customers_sim4.py
import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        txtT = self._view._txtThreshold.value
        if txtT == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire soglia T.", color="red"))
            self._view.update_page()
            return
        try:
            T = int(txtT)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("T deve essere un intero.", color="red"))
            self._view.update_page()
            return
        if T <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("T deve essere positivo.", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(T)
        nN, nE = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato. Nodi={nN}, Archi={nE}"))

        # abilita controlli
        self._view._txtIdCustomer.disabled = False
        self._view._btnDettagli.disabled = False
        self._view._btnComp.disabled = False
        self._view._txtIdCustomer2.disabled = False
        self._view._btnShortest.disabled = False
        self._view._txtK.disabled = False
        self._view._btnTeam.disabled = False
        self._view.update_page()

    def handleDettagli(self, e):
        t = self._view._txtIdCustomer.value
        if t == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire customer_id.", color="red"))
            self._view.update_page()
            return
        try:
            cid = int(t)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("customer_id deve essere numerico.", color="red"))
            self._view.update_page()
            return
        if not self._model.hasCustomer(cid):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Cliente non presente.", color="red"))
            self._view.update_page()
            return

        c = self._model.getCustomer(cid)
        vic = self._model.neighbors_sorted(c)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grado di {c}: {len(vic)}"))
        for v, w in vic:
            self._view.txt_result.controls.append(ft.Text(f"{v} — overlap: {w}"))
        self._view.update_page()

    def handleComp(self, e):
        t = self._view._txtIdCustomer.value
        if t == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire customer_id.", color="red"))
            self._view.update_page()
            return
        try:
            cid = int(t)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("customer_id deve essere numerico.", color="red"))
            self._view.update_page()
            return
        if not self._model.hasCustomer(cid)):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Cliente non presente.", color="red"))
            self._view.update_page()
            return

        c = self._model.getCustomer(cid)
        size = self._model.component_size(c)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Componente connessa che contiene {c}: size={size}"))
        self._view.update_page()

    def handleShortest(self, e):
        t1 = self._view._txtIdCustomer.value
        t2 = self._view._txtIdCustomer2.value
        if t1 == "" or t2 == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire i due customer_id.", color="red"))
            self._view.update_page()
            return
        try:
            c1, c2 = int(t1), int(t2)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Gli id devono essere numerici.", color="red"))
            self._view.update_page()
            return
        if not self._model.hasCustomer(c1) or not self._model.hasCustomer(c2):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Cliente non presente.", color="red"))
            self._view.update_page()
            return

        s1 = self._model.getCustomer(c1)
        s2 = self._model.getCustomer(c2)
        path = self._model.shortest_path(s1, s2)
        self._view.txt_result.controls.clear()
        if len(path) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato.", color="red"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Shortest path {s1} → {s2}:"))
            for n in path:
                self._view.txt_result.controls.append(ft.Text(str(n)))
        self._view.update_page()

    def handleTeam(self, e):
        # seed + K
        t = self._view._txtIdCustomer.value
        ktxt = self._view._txtK.value
        if t == "" or ktxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire seed e K.", color="red"))
            self._view.update_page()
            return
        try:
            cid = int(t); K = int(ktxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Valori non numerici.", color="red"))
            self._view.update_page()
            return
        if K < 1:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("K deve essere >= 1.", color="red"))
            self._view.update_page()
            return
        if not self._model.hasCustomer(cid):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Cliente seed non presente.", color="red"))
            self._view.update_page()
            return

        seed = self._model.getCustomer(cid)
        team, score = self._model.getOttimo(seed, K)

        self._view.txt_result.controls.clear()
        if len(team) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessuna soluzione trovata.", color="red"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Team diversificato di K={K} con seed {seed}, overlap interno totale={score}."))
            for m in team:
                self._view.txt_result.controls.append(ft.Text(str(m)))
        self._view.update_page()
