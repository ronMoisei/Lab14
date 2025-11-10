from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    customer_id: int
    first_name: str
    last_name: str
    phone: Optional[str]
    email: Optional[str]
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]

    def __hash__(self):
        return hash(self.customer_id)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID {self.customer_id})"