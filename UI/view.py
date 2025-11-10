# view/view_orders_products_sim3.py
import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Sim-03 Orders–Products Bipartite MultiGraph"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT

        self._controller = None

        self._btnCrea = None
        self._txtIdProd = None
        self._btnVolume = None
        self._btnMaxCC = None

        self._txtIdProd2 = None
        self._btnShortest = None

        self._ddL = None
        self._btnBest = None

        self.txt_result = None

    def load_interface(self):
        self._btnCrea = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        self._page.add(ft.Row([self._btnCrea], alignment=ft.MainAxisAlignment.CENTER))

        # riga 2: volume / max CC
        self._txtIdProd = ft.TextField(label="product_id", disabled=True, width=180)
        self._btnVolume = ft.ElevatedButton(text="Incident volume", on_click=self._controller.handleVolume, disabled=True)
        self._btnMaxCC = ft.ElevatedButton(text="Max componente", on_click=self._controller.handleMaxCC, disabled=True)
        self._page.add(ft.Row([self._txtIdProd, self._btnVolume, self._btnMaxCC],
                              alignment=ft.MainAxisAlignment.CENTER))

        # riga 3: shortest alternating path tra prodotti
        self._txtIdProd2 = ft.TextField(label="product_id destinazione", disabled=True, width=220)
        self._btnShortest = ft.ElevatedButton(text="Shortest alternating path",
                                              on_click=self._controller.handleShortest, disabled=True)
        self._page.add(ft.Row([self._txtIdProd2, self._btnShortest], alignment=ft.MainAxisAlignment.CENTER))

        # riga 4: cammino ottimo alternato L
        self._ddL = ft.Dropdown(label="L (n nodi)", disabled=True, width=160)
        self._btnBest = ft.ElevatedButton(text="Cammino ottimo (L, pesi decrescenti)",
                                          on_click=self._controller.handleBest, disabled=True)
        self._page.add(ft.Row([self._ddL, self._btnBest], alignment=ft.MainAxisAlignment.CENTER))

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
