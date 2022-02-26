from pydantic import BaseModel
from typing import Optional

#Model for trips
class Trip(BaseModel):
  passangers  : list
  items       : Optional[int] = None
  destination : str