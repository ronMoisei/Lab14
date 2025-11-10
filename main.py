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
SIMULATION 1 — Products Co-Purchase Graph + Best Fixed-Length Path (Same Category)
Branch: sim-01_products-copurchase_weighted_graph_fixedlen_path

TYPE:
    Simple undirected weighted graph.

GRAPH DEFINITION:
    - Vertices: products.
    - Edge(u, v): exists if products u and v appear together in at least one order.
    - Weight: number of orders in which the two products co-occur.

GRAPH EXERCISES:
    1. Edge Volume — sum of the weights of all edges incident to a selected product.
    2. Max Connected Component — size of the largest connected component.

RECURSION PROBLEM:
    Function getOttimo(source, L)
    Finds a simple path of exact length L consisting only of products 
    belonging to the same category as 'source'.
    The objective is to maximize the sum of the edge weights.

RECURSION STRUCTURE:
    getOttimo(source, L)
        → initializes global best variables and calls _ricorsione()
    _ricorsione(parziale, L, cat)
        → explores all neighbors with the same category, without repetition
    getScore(path)
        → computes total weight of the path

FILES:
    - DAO: dao_products_sim1.py
    - Model: model_products_sim1.py
    - Controller: controller_products_sim1.py
    - View: view_products_sim1.py

EXAM FOCUS:
    Weighted graph creation, component analysis, 
    path search with constraints and recursion.
"""
