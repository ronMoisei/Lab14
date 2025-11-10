import flet as ft

from model.model import Model
from UI.view import View
from UI.controller import Controller


def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    my_view.load_interface()


ft.app(target=main)

"""
SIMULATION 3 — Orders–Products Bipartite MultiGraph + Alternating Best Path
Branch: sim-03_orders-products_bipartite_multigraph_altpath_decqty

TYPE:
    Undirected bipartite MultiGraph with weights.

GRAPH:
    - Partitions: U=orders, V=products.
    - Edge (o, p): exists for each order_items row; weight = SUM(quantity) for that (order, product).

GRAPH EXERCISES:
    1) Incident volume for a product (sum of incident edge weights).
    2) Largest connected component size.
    3) Shortest alternating path between two products (via orders).

RECURSION (didactic pattern):
    getOttimo(p_start, L) → initializes best and seeds first hop to an Order.
    _ricorsione(parziale, L, last_w) → expands alternating Product/Order with strictly decreasing weights.
    getScore(path) → sum of edge weights along the path (summing parallel edges in MultiGraph).

FILES:
    - DAO: database/dao_orders_products_sim3.py
    - Model: model/model_orders_products_sim3.py
    - Controller: controller/controller_orders_products_sim3.py
    - View: view/view_orders_products_sim3.py
"""

