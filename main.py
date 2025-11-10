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
SIMULATION 4 — Customers Similarity Graph + Diversified Team (min internal overlap)
Branch: sim-04_customers-similarity_simple-graph_diversified-team

TYPE:
    Simple undirected graph with an 'overlap' edge attribute.

GRAPH:
    - Nodes: customers.
    - Edge {u,v}: exists if u and v share at least T distinct products.
    - Edge attribute 'overlap' = number of shared distinct products.

GRAPH EXERCISES:
    1) Neighborhood details for a customer (degree and neighbors sorted by overlap).
    2) Connected component size for a customer.
    3) Unweighted shortest path between two customers.

RECURSION (didactic pattern):
    getOttimo(seed, K) → selects a team of K customers from the component of seed.
    _ricorsione(parziale, K, candidates) → explores subsets including 'seed'.
    getScore(team) → sum of 'overlap' on internal edges (to minimize for diversification).

FILES:
    - DAO: database/dao_customers_sim4.py
    - Model: model/model_customers_sim4.py
    - Controller: controller/controller_customers_sim4.py
    - View: view/view_customers_sim4.py
"""


