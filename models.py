from pydantic import BaseModel
from typing import Optional

#Model for trips
class Trip(BaseModel):
  passangers  : list
  items       : Optional[str] = ''
  destination : str

class EditTrip(BaseModel):
  passangers : list
  items      : str