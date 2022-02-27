from email.policy import HTTP
from fastapi import FastAPI, HTTPException, status
from typing import Optional
from models import Trip, EditTrip
import helpers, uuid

#initializes the app
app = FastAPI()

#API endpoints
#Get all destinations
@app.get('/api/destinations')
async def get_destinations(maxTemp: Optional[int] = None, minTemp: Optional[int] = None, type: Optional[str] = None):

  #get destination data
  try:
    destinations = await helpers.load_data('planets.json')
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'Error getting destinations'})

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

#Endpoint for getting booked trips
@app.get('/api/trips')
async def get_booked_trips():

  #get booked trips
  try:
    booked_trips = await helpers.load_data('trips.json')
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'Could not get booked trips'})
  
  raise HTTPException(status_code=status.HTTP_200_OK, detail={'Booked trips': booked_trips})

#Endpoint for booking trips
@app.post('/api/trips')
async def add_trip(trip: Trip):

  #Generates the universally unique identifier for the trip
  gID = str(uuid.uuid1())
  
  #get destination price and name
  trip_info = await helpers.get_info(trip.destination)
  trip_price = round(len(trip.passangers) * float(trip_info['price']), 2)

  booked_trip = {
    'id'            : gID,
    'passangers'    : trip.passangers,
    'items'         : trip.items,
    'destinationId' : trip.destination,
    'destination'   : trip_info['name'],
    'price'         : trip_price
  }

  #Book the trip
  try:
    await helpers.add_trip(booked_trip)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'Failed to book the trip'})
  
  raise HTTPException(status_code=status.HTTP_200_OK, detail={'Trip booked successfully': {'passangers': trip.passangers, 'items': trip.items, 'destinationId': trip.destination}})

#Get individual trip info
@app.get('/api/trips/{uuid}')
async def get_trip(uuid: str):

  #try to the get trip info
  try:
    trip = await helpers.get_one_trip(uuid)
  except:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Trip not found'})
  
  if not trip:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Trip not found'})
  
  raise HTTPException(status_code=status.HTTP_200_OK, detail={'Trip': trip})

#Edits trip's passangers and recalculates price
@app.put('/api/trips/{uuid}')
async def edit_passangers(uuid: str, editTrip: EditTrip):

  #Get the booked trip to be edited
  try:
    trip = await helpers.get_one_trip(uuid)
  except:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Trip not found'})  

  if not trip:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Trip not found'})

  #Changes to the trip
  trip['passangers'] = editTrip.passangers
  trip['items'] = editTrip.items
  trip['price'] = float(trip['price'])  * len(editTrip.passangers)

  #Edit the existing booked trip
  try:
    await helpers.edit_trip(trip)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'failed to edit the trip'})

  raise HTTPException(status_code=status.HTTP_200_OK, detail={'success': 'trip edited successfully'})
  
#Deletes a booked trip based on id
@app.delete('/api/trips/{uuid}')
async def delete_trip(uuid):

  #Delete the trip from JSON file
  try:
    await helpers.delete_trip(uuid)
  except:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'description': 'Trip not found'})
  
  raise HTTPException(status_code=status.HTTP_200_OK, detail={'Description': 'Successful deletion'})