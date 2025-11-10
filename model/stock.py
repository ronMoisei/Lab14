from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Stock:
    store_id: int
    product_id: int
    quantity: int

    def __hash__(self):
        return hash((self.store_id, self.product_id))

    def __str__(self):
        return f"Store {self.store_id} – Product {self.product_id}: Qty {self.quantity}"