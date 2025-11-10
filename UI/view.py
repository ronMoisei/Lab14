# view/view_brands_sim7.py
import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Sim-07 Brands → Products Directed Weighted Graph"
        self._controller = None

        self._txtIdA = None
        self._txtIdB = None
        self._txtSeed = None
        self._txtK = None
        self._btnBuild = None
        self._btnReach = None
        self._btnShortest = None
        self._btnVicini = None
        self._btnOttimo = None
        self.txt_result = None

    def load_interface(self):
        title = ft.Text("Simulation 7 — Directed Brand→Product Supply Graph", size=18, color="blue")
        self._page.add(title)

        self._btnBuild = ft.ElevatedButton(text="Costruisci Grafo", on_click=self._controller.handleBuild)
        self._page.add(ft.Row([self._btnBuild], alignment=ft.MainAxisAlignment.CENTER))

        self._txtIdA = ft.TextField(label="brand_id A", width=120, disabled=True)
        self._txtIdB = ft.TextField(label="brand_id B", width=120, disabled=True)
        self._btnReach = ft.ElevatedButton(text="Verifica Raggiungibilità", on_click=self._controller.handleReach, disabled=True)
        self._btnShortest = ft.ElevatedButton(text="Shortest Path", on_click=self._controller.handleShortest, disabled=True)
        self._btnVicini = ft.ElevatedButton(text="Vicini(A)", on_click=self._controller.handleVicini, disabled=True)
        self._page.add(ft.Row([self._txtIdA, self._txtIdB, self._btnReach, self._btnShortest, self._btnVicini],
                              alignment=ft.MainAxisAlignment.CENTER))

        self._txtSeed = ft.TextField(label="seed brand_id", width=140, disabled=True)
        self._txtK = ft.TextField(label="K", width=80, disabled=True)
        self._btnOttimo = ft.ElevatedButton(text="Percorso Ottimo (Ricorsione)", on_click=self._controller.handleOttimo, disabled=True)
        self._page.add(ft.Row([self._txtSeed, self._txtK, self._btnOttimo], alignment=ft.MainAxisAlignment.CENTER))

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=10)
        self._page.add(self.txt_result)
        self._page.update()

    def set_controller(self, c): self._controller = c
    def update_page(self): self._page.update()
