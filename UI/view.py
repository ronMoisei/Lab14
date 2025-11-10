# view/view_products_sim1.py
import flet as ft

class ViewProdSim1(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Sim-01 Products Co-purchase – Weighted Graph"
        self._ctl = None

        self.dd_products = None
        self.txt_L = None
        self.lst = None

    def load_interface(self):
        self.dd_products = ft.Dropdown(label="Prodotto")
        self.txt_L = ft.TextField(label="L (lunghezza esatta)", width=180)

        btnBuild = ft.ElevatedButton("Crea grafo", on_click=self._ctl.handleBuild)
        btnVic   = ft.ElevatedButton("Vicini ordinati", on_click=self._ctl.handleNeighbors)
        btnVol   = ft.ElevatedButton("Edge volume", on_click=self._ctl.handleVolume)
        btnCC    = ft.ElevatedButton("Max componente", on_click=self._ctl.handleMaxCC)
        btnBest  = ft.ElevatedButton("Cammino ottimo (L)", on_click=self._ctl.handleBestPath)

        self.lst = ft.ListView(expand=1, spacing=8, padding=10, auto_scroll=False)

        self._page.add(
            ft.Row([btnBuild]),
            ft.Row([self.dd_products, self.txt_L, btnVic, btnVol, btnCC, btnBest]),
            self.lst
        )
        self._page.update()

    def set_controller(self, c): self._ctl = c
    def update_page(self): self._page.update()
