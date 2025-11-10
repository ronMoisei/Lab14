# view/view_customers_sim6.py
import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Sim-06 Customer Similarity Weighted Graph"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None

        # UI refs
        self._txtMinOrders = None
        self._txtMinShared = None
        self._btnCrea = None

        self._txtCust = None
        self._btnComp = None
        self._btnVicini = None

        self._txtCust2 = None
        self._btnShortest = None

        self._txtSeed = None
        self._txtK = None
        self._btnOttimo = None

        self.txt_result = None

    def load_interface(self):
        # riga 1: creazione grafo
        self._txtMinOrders = ft.TextField(label="min_orders", width=140)
        self._txtMinShared = ft.TextField(label="min_shared_brands", width=180)
        self._btnCrea = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        self._page.add(ft.Row([self._txtMinOrders, self._txtMinShared, self._btnCrea],
                              alignment=ft.MainAxisAlignment.CENTER))

        # riga 2: cliente singolo
        self._txtCust = ft.TextField(label="customer_id A", width=160, disabled=True)
        self._btnComp = ft.ElevatedButton(text="Componente(A)", on_click=self._controller.handleComp, disabled=True)
        self._btnVicini = ft.ElevatedButton(text="Vicini(A) peso↓", on_click=self._controller.handleVicini, disabled=True)
        self._page.add(ft.Row([self._txtCust, self._btnComp, self._btnVicini],
                              alignment=ft.MainAxisAlignment.CENTER))

        # riga 3: shortest path
        self._txtCust2 = ft.TextField(label="customer_id B", width=160, disabled=True)
        self._btnShortest = ft.ElevatedButton(text="Shortest path A→B", on_click=self._controller.handleShortest, disabled=True)
        self._page.add(ft.Row([self._txtCust2, self._btnShortest], alignment=ft.MainAxisAlignment.CENTER))

        # riga 4: ricorsione
        self._txtSeed = ft.TextField(label="seed customer_id", width=160, disabled=True)
        self._txtK = ft.TextField(label="K", width=100, disabled=True)
        self._btnOttimo = ft.ElevatedButton(text="Team ottimo (max brand coverage)", on_click=self._controller.handleOttimo, disabled=True)
        self._page.add(ft.Row([self._txtSeed, self._txtK, self._btnOttimo], alignment=ft.MainAxisAlignment.CENTER))

        # output
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=14, auto_scroll=False)
        self._page.add(self.txt_result)
        self._page.update()

    @property
    def controller(self): return self._controller
    @controller.setter
    def controller(self, c): self._controller = c
    def set_controller(self, c): self._controller = c
    def update_page(self): self._page.update()
