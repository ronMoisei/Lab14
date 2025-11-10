# controller/controller_stores_sim2.py
import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        """
        Crea il grafo delle transizioni tra store e abilita i controlli successivi.
        """
        self._model.buildGraph()
        nNodi, nArchi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(
            f"Grafo creato. Il grafo contiene {nNodi} nodi e {nArchi} archi."
        ))
        # abilito input e bottoni
        self._view._txtIdStore.disabled = False
        self._view._btnRaggiungibili.disabled = False
        self._view._btnOutVolume.disabled = False
        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False

        # popolo il DD L con un range ragionevole (2..10) oppure dinamico
        self._view._ddLun.options = list(map(lambda x: ft.dropdown.Option(x), list(range(2, 11))))
        self._view.update_page()

    def handleRaggiungibili(self, e):
        """
        Valida lo store e stampa i nodi raggiungibili via BFS (diretta).
        """
        txt = self._view._txtIdStore.value
        if txt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire uno store_id.", color="red"))
            self._view.update_page()
            return

        try:
            sid = int(txt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Lo store_id deve essere numerico.", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(sid):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("store_id non presente nel grafo.", color="red"))
            self._view.update_page()
            return

        s = self._model.getObjectFromId(sid)
        nodes = self._model.getReachableBFS(s)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Raggiungibili da {s}:"))
        for n in nodes:
            self._view.txt_result.controls.append(ft.Text(str(n)))
        self._view.update_page()

    def handleOutVolume(self, e):
        """
        Calcola la somma dei pesi degli archi uscenti dallo store selezionato.
        """
        txt = self._view._txtIdStore.value
        if txt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire uno store_id.", color="red"))
            self._view.update_page()
            return

        try:
            sid = int(txt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Lo store_id deve essere numerico.", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(sid):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("store_id non presente nel grafo.", color="red"))
            self._view.update_page()
            return

        s = self._model.getObjectFromId(sid)
        vol = self._model.outVolume(s)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Out-volume di {s}: {vol}"))
        self._view.update_page()

    def handleCerca(self, e):
        """
        Ricorsione: cammino semplice diretto di lunghezza esatta L a pesi decrescenti,
        a punteggio massimo, con partenza dallo store selezionato.
        """
        # store di partenza
        txt = self._view._txtIdStore.value
        if txt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire uno store_id.", color="red"))
            self._view.update_page()
            return

        try:
            sid = int(txt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Lo store_id deve essere numerico.", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(sid):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("store_id non presente nel grafo.", color="red"))
            self._view.update_page()
            return

        start = self._model.getObjectFromId(sid)

        # L
        lun = self._view._ddLun.value
        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Selezionare una lunghezza L.", color="red"))
            self._view.update_page()
            return
        L = int(lun)

        path, scoreTot = self._model.getOttimo(start, L)

        self._view.txt_result.controls.clear()
        if len(path) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino che rispetti i vincoli richiesti.", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(
            f"Cammino ottimo di lunghezza {L} da {start} trovato con score totale {scoreTot}."))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(str(p)))
        self._view.update_page()
