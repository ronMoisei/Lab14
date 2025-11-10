from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Category:
    category_id: int
    category_name: str

    def __hash__(self):
        return hash(self.category_id)

    def __str__(self):
        return f"{self.category_name} (CatID {self.category_id})"