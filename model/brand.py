from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Brand:
    brand_id: int
    brand_name: str

    def __hash__(self):
        return hash(self.brand_id)

    def __str__(self):
        return f"{self.brand_name} (BrandID {self.brand_id})"