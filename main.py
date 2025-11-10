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
SIMULATION 8 — Category Co-Purchase Weighted Graph + Max Customer-Coverage K-Set
Branch: sim-08_categories-copurchase_weighted-graph_max-customer-coverage_k-set

TYPE
  Simple undirected weighted graph.

GRAPH
  Nodes: categories.
  Edge {c1,c2}: weight = #ordini distinti che contengono prodotti di entrambe le categorie,
                 filtrato con min_shared_orders.

EXERCISES
  1) Longest component size dalla categoria A.
  2) Shortest path non pesato tra due categorie A→B.
  3) Vicini di A ordinati per peso decrescente.

RECURSION
  getOttimo(seed, K): seleziona K categorie nella componente di seed massimizzando
                      la copertura di clienti distinti.
  _ricorsione(parziale, K, candidates, current_customers): unione insiemi clienti con snapshot/rollback.
  getScore(customers_union): cardinalità dell’unione.

FILES
  - database/dao_categories_sim8.py
  - model/model_categories_sim8.py
  - controller/controller_categories_sim8.py
  - view/view_categories_sim8.py
"""
