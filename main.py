from fastapi import FastAPI, HTTPException, status
from typing import Optional
from models import Trip
import helpers

#initializes the app
app = FastAPI()

#API endpoints

#Get all destinations
@app.get('/api/destinations')
async def get_destinations(maxTemp: Optional[int] = None, minTemp: Optional[int] = None, type: Optional[str] = None):

  #get destination data
  destinations = await helpers.load_data('planets.json')

  #query based on if parameters are given
  if maxTemp:
    destinations = [destination for destination in destinations if destination['avgTemp'] <= maxTemp]
  if minTemp:
    destinations = [destination for destination in destinations if destination['avgTemp'] >= minTemp]
  if type and type == 'planet':
    destinations = [destination for destination in destinations if destination['isPlanet'] == True]
  if type and type == 'moon':
    destinations = [destination for destination in destinations if destination['isPlanet'] == False]

  if destinations == []:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'No destinations match your criteria'})

  raise HTTPException(status_code=status.HTTP_200_OK, detail={'Destinations': destinations})

@app.post('/api/trips')
async def add_trip():
  pass