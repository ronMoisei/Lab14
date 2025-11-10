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
SIMULATION 7 — Brand → Product Supply Graph + Min-Cost Path of Brands
Branch: sim-07_brands-products_directed-weighted-graph_min-cost_supply_path

TYPE
  Directed weighted graph.

GRAPH
  Nodes:
      brands + products.
  Edges:
      brand → product  (peso = list_price)
      product → brand₂  (peso = media list_price dei prodotti venduti nello stesso store)
  Represents supply and cross-brand relations.

EXERCISES
  1) Verifica raggiungibilità tra due brand.
  2) Shortest path min cost tra due brand.
  3) Successori ordinati per costo crescente.

RECURSION
  getOttimo(seed, K): trova un cammino di K nodi minimizzando il costo medio dei passaggi.
  _ricorsione(): esplora i successori diretti, mantiene il costo totale corrente.
  getScore(): ritorna il costo medio.

FILES
  - database/dao_brands_sim7.py  
  - model/model_brands_sim7.py  
  - controller/controller_brands_sim7.py  
  - view/view_brands_sim7.py
"""

