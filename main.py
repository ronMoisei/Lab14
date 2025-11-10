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
SIMULATION 5 — Product Co-Purchase Weighted Graph + Max-Affinity Bundle (category-diverse)
Branch: sim-05_products-copurchase_weighted-graph_max-bundle_diverse-category

TYPE:
    Simple undirected weighted graph.

GRAPH:
    - Nodes: products.
    - Edge {p1, p2}: weight = number of distinct orders where p1 and p2 appear together.
    - Threshold parameter filters edges by minimum weight.

GRAPH EXERCISES:
    1) Incident volume for a product (sum of incident edge weights).
    2) Connected component size.
    3) Unweighted shortest path between two products.
    4) Neighborhood sorted by edge weight.

RECURSION (didactic pattern):
    getOttimo(seed, K) → maximize total internal co-purchase weight of a K-product bundle
                         within the seed’s connected component, enforcing category diversity
                         (at most one product per category).
    _ricorsione(parziale, K, candidates, used_cat) → explores subsets honoring the constraint.
    getScore(bundle) → sum of 'weight' over internal edges of the bundle.

FILES:
    - DAO: database/dao_products_sim5.py
    - Model: model/model_products_sim5.py
    - Controller: controller/controller_products_sim5.py
    - View: view/view_products_sim5.py
"""



