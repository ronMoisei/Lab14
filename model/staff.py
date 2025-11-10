from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Staff:
    staff_id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    active: bool
    store_id: int
    manager_id: Optional[int]

    def __hash__(self):
        return hash(self.staff_id)

    def __str__(self):
        return f"{self.first_name} {self.last_name} [Staff ID {self.staff_id}]"