import json

#contains all the helper functions

#loads data from a JSON file (could be a db in production)
async def load_data(path: str):
  try:
    data = json.load(open(path))
    return data
  except:
    return False

#books a trip
async def add_trip(booked_trip: dict):
  try:
    with open('trips.json', 'r') as file:
      data = json.load(file)
    
    data.append(booked_trip)

    with open('trips.json', 'w') as file:
      json.dump(data, file)
      file.close()
  except:
    return False

async def get_one_trip(tripId: str):
  try:
    #Load all trip info
    trips = await load_data('trips.json')
    
    #Query for uuid
    for trip in trips:
      if trip['id'] == tripId:
        return trip

    return False
  except:
    return False

async def get_info(destinationId: str):
  try:
    #Get all destinations
    destinations = await load_data('planets.json')

    #Query for price
    for destination in destinations:
      if destination['id'] == destinationId:
        return {'price': destination['price'], 'name': destination['name']}
  except:
    return False

async def delete_trip(tripId: str):
  try:
    with open('trips.json', 'r') as file:
      trips = json.load(file)
    
    for trip in trips:
      if trip['id'] == tripId:
        trips.remove(trip)
    
    with open('trips.json', 'w') as file:
        json.dump(trips, file)
        file.close()
    
    return True
  except:
    return False