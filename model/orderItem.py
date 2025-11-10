from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrderItem:
    order_id: int
    item_id: int
    product_id: int
    quantity: int
    list_price: float
    discount: float

    def __hash__(self):
        return hash((self.order_id, self.item_id))

    def __str__(self):
        return f"Order {self.order_id} Item {self.item_id} – Product {self.product_id}"