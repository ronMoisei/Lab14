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
SIMULATION 6 — Customer Similarity Weighted Graph + Max Brand-Coverage K-Team
Branch: sim-06_customers-similarity_weighted-graph_max-brand-coverage_k-team

TYPE:
    Simple undirected weighted graph.

GRAPH:
    - Nodes: customers with at least 'min_orders' orders.
    - Edge {c1,c2}: weight = number of distinct brands both have purchased.
    - Edges filtered by 'min_shared' (minimum shared brands).

GRAPH EXERCISES:
    1) Connected component size of a customer.
    2) Unweighted shortest path between two customers.
    3) Neighbors of a customer sorted by edge weight (shared brands).

RECURSION (didactic pattern):
    getOttimo(seed, K) → select K customers from seed’s connected component
                         maximizing brand coverage: |⋃ brands(customer)|.
    _ricorsione(parziale, K, candidates, current_brands) → explores team subsets,
                                                           updating union of brands and rolling back.
    getScore(current_brands) → cardinality of union set.

FILES:
    - DAO: database/dao_customers_sim6.py
    - Model: model/model_customers_sim6.py
    - Controller: controller/controller_customers_sim6.py
    - View: view/view_customers_sim6.py
"""
