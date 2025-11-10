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
SIMULATION 2 — Stores 'customer-flow' Transition Graph + Best Decreasing-Weights Path
Branch: sim-02_stores-transition_digraph_decreasing-weights-path

TYPE:
    Directed weighted graph.

GRAPH:
    - Nodes: stores.
    - Edge u -> v: exists if, for the same customer, an order at store u is followed by the next
      chronological order at store v (with u != v).
    - Weight: number of such u->v transitions across all customers.

GRAPH EXERCISES:
    1) Out-volume: sum of outgoing edge weights for a selected store.
    2) Reachable set (BFS): nodes reachable from the selected store following edge direction.

RECURSION (didactic pattern):
    getOttimo(start, L) → initializes best solution and explores first hop.
    _ricorsione(parziale, L) → expands only with strictly decreasing edge weights,
                               avoids repeated nodes.
    getScore(path) → sum of weights along the directed path.

FILES:
    - DAO: database/dao_stores_sim2.py
    - Model: model/model_stores_sim2.py
    - Controller: controller/controller_stores_sim2.py
    - View: view/view_stores_sim2.py
"""
