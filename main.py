from fastapi import FastAPI, HTTPException, status
from typing import Optional
from models import Trip
import helpers, uuid

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
async def add_trip(trip: Trip):

  #Generates the universally unique identifier for the trip
  gID = str(uuid.uuid1())
  
  booked_trip = {
    'id'          : gID,
    'passangers'  : trip.passangers,
    'items'       : trip.items,
    'destination' : trip.destination
  }

  print(booked_trip)

  #Book the trip
  try:
    await helpers.add_trip(booked_trip)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'Failed to book the trip'})
  
  raise HTTPException(status_code=status.HTTP_200_OK, detail={'Trip booked successfully': f'Trip id: {gID}'})