import json

#contains all the helper functions

#loads data from a JSON file (could be a db in production)
async def load_data(path: str):
  data = json.load(open(path))
  return data

#books a trip
async def add_trip(booked_trip: dict):
  with open('trips.json', 'r') as file:
    data = json.load(file)
  
  data.append(booked_trip)

  with open('trips.json', 'w') as file:
    json.dump(data, file)
    file.close()

async def get_one_trip(tripId: str):

  #Load all trip info
  trips = await load_data('trips.json')
  
  #Query for uuid
  for trip in trips:
    if trip['id'] == tripId:
      return trip

  return False

async def get_info(destinationId: str):
  #Get all destinations
  destinations = await load_data('planets.json')

  #Query for price
  for destination in destinations:
    if destination['id'] == destinationId:
      return {'price': destination['price'], 'name': destination['name']}

#Deletes a booked trip based on id
async def delete_trip(tripId: str):
  with open('trips.json', 'r') as file:
    trips = json.load(file)
  
  for trip in trips:
    if trip['id'] == tripId:
      trips.remove(trip)
  
  with open('trips.json', 'w') as file:
      json.dump(trips, file)
      file.close()

#helper function for trip editing
async def edit_trip(editedTrip):
  trips = await load_data('trips.json')
  for trip in trips:
    if trip['id'] == editedTrip['id']:
      trips.remove(trip)
      trips.append(editedTrip)
  
  with open('trips.json', 'w') as file:
    json.dump(trips, file)
    file.close()