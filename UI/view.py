# view/view_stores_sim2.py
import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Sim-02 Stores Transition – Directed Weighted Graph"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT

        # controller (inizializzato nel main)
        self._controller = None

        # UI elements
        self._title = None
        self._btnCreaGrafo = None
        self._txtIdStore = None
        self._btnRaggiungibili = None
        self._btnOutVolume = None
        self._ddLun = None
        self._btnCerca = None
        self.txt_result = None

    def load_interface(self):
        self._title = ft.Text("Sim-02 — Stores Transition Graph", color="blue", size=22)
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)

        row1 = ft.Row([self._title, self._btnCreaGrafo], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # Input store e azioni
        self._txtIdStore = ft.TextField(label="store_id di partenza", disabled=True, width=220)
        self._btnRaggiungibili = ft.ElevatedButton(text="Raggiungibili (BFS)",
                                                   on_click=self._controller.handleRaggiungibili, disabled=True)
        self._btnOutVolume = ft.ElevatedButton(text="Out-volume",
                                               on_click=self._controller.handleOutVolume, disabled=True)

        row2 = ft.Row([self._txtIdStore, self._btnRaggiungibili, self._btnOutVolume],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # Ricerca cammino ottimo con L fisso, pesi decrescenti
        self._ddLun = ft.Dropdown(label="Lunghezza L", disabled=True, width=160)
        self._btnCerca = ft.ElevatedButton(text="Cammino ottimo (L, pesi decrescenti)",
                                           on_click=self._controller.handleCerca, disabled=True)

        row3 = ft.Row([self._ddLun, self._btnCerca], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # Output
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=16, auto_scroll=False)
        self._page.controls.append(self.txt_result)
        self._page.update()

    # wiring del controller
    @property
    def controller(self): return self._controller
    @controller.setter
    def controller(self, c): self._controller = c
    def set_controller(self, c): self._controller = c

    def update_page(self): self._page.update()
