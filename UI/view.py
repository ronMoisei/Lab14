# view/view_customers_sim4.py
import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Sim-04 Customers Similarity – Simple Graph"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None

        # UI refs
        self._txtThreshold = None
        self._btnCrea = None

        self._txtIdCustomer = None
        self._btnDettagli = None
        self._btnComp = None

        self._txtIdCustomer2 = None
        self._btnShortest = None

        self._txtK = None
        self._btnTeam = None

        self.txt_result = None

    def load_interface(self):
        # riga 1: creazione grafo
        self._txtThreshold = ft.TextField(label="Soglia T prodotti comuni", width=220)
        self._btnCrea = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        self._page.add(ft.Row([self._txtThreshold, self._btnCrea], alignment=ft.MainAxisAlignment.CENTER))

        # riga 2: customer singolo
        self._txtIdCustomer = ft.TextField(label="customer_id", disabled=True, width=180)
        self._btnDettagli = ft.ElevatedButton(text="Dettagli vicinato", on_click=self._controller.handleDettagli, disabled=True)
        self._btnComp = ft.ElevatedButton(text="Componente connessa", on_click=self._controller.handleComp, disabled=True)
        self._page.add(ft.Row([self._txtIdCustomer, self._btnDettagli, self._btnComp],
                              alignment=ft.MainAxisAlignment.CENTER))

        # riga 3: shortest path tra due clienti
        self._txtIdCustomer2 = ft.TextField(label="customer_id destinazione", disabled=True, width=240)
        self._btnShortest = ft.ElevatedButton(text="Shortest path", on_click=self._controller.handleShortest, disabled=True)
        self._page.add(ft.Row([self._txtIdCustomer2, self._btnShortest], alignment=ft.MainAxisAlignment.CENTER))

        # riga 4: team diversificato
        self._txtK = ft.TextField(label="K", disabled=True, width=120)
        self._btnTeam = ft.ElevatedButton(text="Team diversificato (ricorsione)", on_click=self._controller.handleTeam, disabled=True)
        self._page.add(ft.Row([self._txtK, self._btnTeam], alignment=ft.MainAxisAlignment.CENTER))

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
