import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaProdotti(self, e):
        """
        Crea il grafo dei prodotti co-acquistati e abilita i controlli successivi.
        """
        self._model.buildGraph()
        nNodi, nArchi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(
            f"Grafo creato. Il grafo contiene {nNodi} nodi e {nArchi} archi."
        ))
        # abilito input e bottone componente
        self._view._txtIdProdotto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()

    def handleCompConnessa(self, e):
        """
        Dato un product_id, valida l'input, verifica l'esistenza nel grafo,
        stampa la size della componente connessa che lo contiene e
        popola il DD per la lunghezza L (>=2 e < size componente).
        """
        txtInput = self._view._txtIdProdotto.value

        if txtInput == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un product_id.", color="red"))
            self._view.update_page()
            return

        try:
            idInput = int(txtInput)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Il valore inserito non è un numero.", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(idInput):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("L'id inserito non corrisponde a un nodo del grafo.", color="red"))
            self._view.update_page()
            return

        sizeCC = self._model.getInfoConnessa(idInput)
        prodotto = self._model.getObjectFromId(idInput)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa che contiene {prodotto} ha dimensione pari a {sizeCC}.")
        )

        # abilito ricerca cammino e popolo DD lunghezze ammissibili
        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False

        valori = list(range(2, sizeCC))  # L valido: 2 .. sizeCC-1
        self._view._ddLun.options = list(map(lambda x: ft.dropdown.Option(x), valori))

        self._view.update_page()

    def handleCerca(self, e):
        """
        Risolve il problema ricorsivo: path semplice di lunghezza esatta L
        nella stessa categoria del prodotto di partenza, massimizzando la somma dei pesi.
        Stampa path e score totale.
        """
        # sorgente
        try:
            source = self._model.getObjectFromId(int(self._view._txtIdProdotto.value))
        except Exception:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Product_id non valido.", color="red"))
            self._view.update_page()
            return

        # lunghezza L
        lun = self._view._ddLun.value
        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare un parametro Lunghezza.", color="red"))
            self._view.update_page()
            return
        L = int(lun)

        path, scoreTot = self._model.getOttimo(source, L)

        self._view.txt_result.controls.clear()
        if len(path) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino valido con i vincoli richiesti.", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(
            f"Cammino ottimo di lunghezza {L} dalla sorgente {source} "
            f"(categoria {source.category_id}) trovato con score totale {scoreTot}."
        ))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(str(p)))
        self._view.update_page()
