import json

from numpy import tri

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

  trips = await load_data('trips.json')
  
  for trip in trips:
    if trip['id'] == tripId:
      return trip
  return False