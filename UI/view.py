# view/view_categories_sim8.py
import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Sim-08 Category Co-Purchase Weighted Graph"
        self._controller = None

        self._txtMinShared = None
        self._btnBuild = None

        self._txtCatA = None
        self._txtCatB = None
        self._btnComp = None
        self._btnVicini = None
        self._btnShortest = None

        self._txtSeed = None
        self._txtK = None
        self._btnOttimo = None

        self.lst_result = None

    def load_interface(self):
        title = ft.Text("Simulation 8 — Category Co-Purchase Weighted Graph", size=18, color="blue")
        self._page.add(title)

        self._txtMinShared = ft.TextField(label="min_shared_orders", width=180)
        self._btnBuild = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleBuild)
        self._page.add(ft.Row([self._txtMinShared, self._btnBuild], alignment=ft.MainAxisAlignment.CENTER))

        self._txtCatA = ft.TextField(label="category_id A", width=150, disabled=True)
        self._txtCatB = ft.TextField(label="category_id B", width=150, disabled=True)
        self._btnComp = ft.ElevatedButton(text="Comp(A)", on_click=self._controller.handleComp, disabled=True)
        self._btnVicini = ft.ElevatedButton(text="Vicini(A)", on_click=self._controller.handleVicini, disabled=True)
        self._btnShortest = ft.ElevatedButton(text="Shortest A→B", on_click=self._controller.handleShortest, disabled=True)
        self._page.add(ft.Row([self._txtCatA, self._btnComp, self._btnVicini, self._txtCatB, self._btnShortest],
                              alignment=ft.MainAxisAlignment.CENTER))

        self._txtSeed = ft.TextField(label="seed category_id", width=160, disabled=True)
        self._txtK = ft.TextField(label="K", width=80, disabled=True)
        self._btnOttimo = ft.ElevatedButton(text="Ricorsione: K categorie", on_click=self._controller.handleOttimo, disabled=True)
        self._page.add(ft.Row([self._txtSeed, self._txtK, self._btnOttimo], alignment=ft.MainAxisAlignment.CENTER))

        self.lst_result = ft.ListView(expand=1, spacing=10, padding=10)
        self._page.add(self.lst_result)
        self._page.update()

    def set_controller(self, c): self._controller = c
    def update_page(self): self._page.update()
