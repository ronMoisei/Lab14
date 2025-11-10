# controller/controller_categories_sim8.py
import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleBuild(self, e):
        txt = self._view._txtMinShared.value
        if txt == "":
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Inserire min_shared_orders.", color="red"))
            self._view.update_page()
            return
        try:
            m = int(txt)
        except ValueError:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Parametro intero.", color="red"))
            self._view.update_page()
            return
        if m < 1:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Valore ≥ 1.", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(m)
        n, ecount = self._model.getGraphDetails()

        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Grafo creato. Nodi={n}, Archi={ecount}"))
        for c in (self._view._txtCatA, self._view._txtCatB, self._view._txtSeed, self._view._txtK):
            c.disabled = False
        self._view._btnComp.disabled = False
        self._view._btnVicini.disabled = False
        self._view._btnShortest.disabled = False
        self._view._btnOttimo.disabled = False
        self._view.update_page()

    def handleComp(self, e):
        cid = self._parse_id(self._view._txtCatA.value)
        if cid is None: return
        c = self._model.getCategory(cid)
        size = self._model.longest_component_size_from(c)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Componente di {c}: size={size}"))
        self._view.update_page()

    def handleVicini(self, e):
        cid = self._parse_id(self._view._txtCatA.value)
        if cid is None: return
        c = self._model.getCategory(cid)
        vic = self._model.neighbors_sorted(c)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Vicini di {c} (peso ordini condivisi ↓):"))
        for v, w in vic:
            self._view.lst_result.controls.append(ft.Text(f"{v} — weight={w}"))
        self._view.update_page()

    def handleShortest(self, e):
        a = self._parse_id(self._view._txtCatA.value)
        b = self._parse_id(self._view._txtCatB.value)
        if a is None or b is None: return
        ca = self._model.getCategory(a); cb = self._model.getCategory(b)
        path = self._model.shortest_path_unweighted(ca, cb)
        self._view.lst_result.controls.clear()
        if not path:
            self._view.lst_result.controls.append(ft.Text("Nessun cammino.", color="red"))
        else:
            self._view.lst_result.controls.append(ft.Text(f"Shortest path {ca} → {cb}:"))
            for n in path:
                self._view.lst_result.controls.append(ft.Text(str(n)))
        self._view.update_page()

    def handleOttimo(self, e):
        sid = self._parse_id(self._view._txtSeed.value)
        ktxt = self._view._txtK.value
        if sid is None or ktxt == "":
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Inserire seed category_id e K.", color="red"))
            self._view.update_page()
            return
        try:
            K = int(ktxt)
        except ValueError:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("K intero.", color="red"))
            self._view.update_page()
            return
        seed = self._model.getCategory(sid)
        team, score = self._model.getOttimo(seed, K)
        self._view.lst_result.controls.clear()
        if not team:
            self._view.lst_result.controls.append(ft.Text("Nessuna soluzione.", color="red"))
        else:
            self._view.lst_result.controls.append(ft.Text(f"Set ottimo K={K} da seed {seed} — clienti coperti={score}"))
            for c in team:
                self._view.lst_result.controls.append(ft.Text(str(c)))
        self._view.update_page()

    def _parse_id(self, txt):
        if txt == "":
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Inserire category_id.", color="red"))
            self._view.update_page()
            return None
        try:
            cid = int(txt)
        except ValueError:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("category_id non numerico.", color="red"))
            self._view.update_page()
            return None
        if not self._model.hasCategory(cid):
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Categoria non presente.", color="red"))
            self._view.update_page()
            return None
        return cid
