# view/view_products_sim5.py
import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Sim-05 Products Co-Purchase Weighted Graph"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None

        # UI refs
        self._txtSoglia = None
        self._btnCrea = None

        self._txtProd = None
        self._btnVolume = None
        self._btnVicini = None
        self._btnComp = None

        self._txtProd2 = None
        self._btnShortest = None

        self._txtK = None
        self._btnOttimo = None

        self.txt_result = None

    def load_interface(self):
        # riga 1: creazione grafo
        self._txtSoglia = ft.TextField(label="Soglia minimo co-purchase (peso arco)", width=300)
        self._btnCrea   = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        self._page.add(ft.Row([self._txtSoglia, self._btnCrea], alignment=ft.MainAxisAlignment.CENTER))

        # riga 2: prodotto singolo (volume / vicini / componente)
        self._txtProd   = ft.TextField(label="product_id", width=160, disabled=True)
        self._btnVolume = ft.ElevatedButton(text="Incident volume", on_click=self._controller.handleVolume, disabled=True)
        self._btnVicini = ft.ElevatedButton(text="Vicini (peso↓)", on_click=self._controller.handleVicini, disabled=True)
        self._btnComp   = ft.ElevatedButton(text="Componente connessa", on_click=self._controller.handleComp, disabled=True)
        self._page.add(ft.Row([self._txtProd, self._btnVolume, self._btnVicini, self._btnComp],
                              alignment=ft.MainAxisAlignment.CENTER))

        # riga 3: shortest path tra prodotti
        self._txtProd2   = ft.TextField(label="product_id destinazione", width=220, disabled=True)
        self._btnShortest= ft.ElevatedButton(text="Shortest path", on_click=self._controller.handleShortest, disabled=True)
        self._page.add(ft.Row([self._txtProd2, self._btnShortest], alignment=ft.MainAxisAlignment.CENTER))

        # riga 4: bundle ottimo (ricorsione)
        self._txtK     = ft.TextField(label="K", width=120, disabled=True)
        self._btnOttimo= ft.ElevatedButton(text="Bundle ottimo (K, cat-diverse)", on_click=self._controller.handleOttimo, disabled=True)
        self._page.add(ft.Row([self._txtK, self._btnOttimo], alignment=ft.MainAxisAlignment.CENTER))

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
