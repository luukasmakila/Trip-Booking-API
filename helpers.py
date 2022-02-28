import json, requests, os

#Contains all the helper functions

#check if destinations.json has been made
async def json_exists(fileName):
  return os.path.exists(fileName)

#fetch all data
async def fetch_all(url: str):
  return requests.get(url)

#fetch one pice of data
async def fetch_one(url):
  return requests.get(url)

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
  destinations = await load_data('destinations.json')

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
async def edit_trip(editedTrip: dict):
  trips = await load_data('trips.json')
  for trip in trips:
    if trip['id'] == editedTrip['id']:
      trips.remove(trip)
      trips.append(editedTrip)
  
  with open('trips.json', 'w') as file:
    json.dump(trips, file)
    file.close()

#calculates the price for non moons
async def calculate_planet(planet):
  distance = (planet['perihelion'] + planet['aphelion']) / 2
  
  if planet['moons'] == None:
    number_of_moons = 0
  else:
    number_of_moons = len(planet['moons'])
  
  price = distance * planet['avgTemp']
  final_price = (price + (number_of_moons * (price * 0.072))) / 100000000
  return round(final_price, 2)

#calculates price for moon bookings
async def calculate_moon(moon):
  orbits = moon['aroundPlanet']

  #get the planet that the moo is orbitings
  response = await fetch_one(orbits['rel'])
  planet = response.json()

  distance = (planet['perihelion'] + planet['aphelion']) / 2
  
  if planet['moons'] == None:
    number_of_moons = 0
  else:
    number_of_moons = len(planet['moons'])
  
  price = distance * moon['avgTemp']
  final_price = (price + (number_of_moons * (price * 0.072))) / 100000000
  return round(final_price, 2)

#calculate prices for all destinations
async def calculate_all(destinations):
  #holds the price and other info for destinations
  destinations_info = []

  #Stores the price for a moon orbiting a certain planet
  #Saves computing power after the price is calculated once
  moon_price_for = {}

  for destination in destinations['bodies']:
    #if avgTemp == 0 change it to 50
    if destination['avgTemp'] == 0:
      destination['avgTemp'] = 50

    if destination['isPlanet'] == False and destination['aroundPlanet'] != None:
      #Is a moon and a planet can have many moons so theres no reason to calculate the moon price multiple times
      #so lets keep track of the price for a moon for a certain planet and use that
      #number every time we see a moon for that planet
      if destination['aroundPlanet']['planet'] not in moon_price_for:
        price = await calculate_moon(destination)
        moon_price_for[destination['aroundPlanet']['planet']] = price
      else:
        price = moon_price_for[destination['aroundPlanet']['planet']]
    else:
      #Not a moon so we do a normal calculation
      price = await calculate_planet(destination)
    
    destinations_info.append({'id': destination['id'], 'name': destination['name'], 'price': price, 'isPlanet': destination['isPlanet'], 'avgTemp': destination['avgTemp']})
  
  return destinations_info

#Functions to initialize json files are here
async def write_destinations(destinations_info):
  with open('destinations.json', 'w') as file:
    json.dump(destinations_info, file)
    file.close()

async def write_trips():
  with open('trips.json', 'w') as file:
    #We want to be able to book new trips so i will initialize trips.json with an empty list
    json.dump([], file)
    file.close()