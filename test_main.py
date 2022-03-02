from main import app
from fastapi.testclient import TestClient
import helpers, json

client = TestClient(app)

#Test for getting destinations
def test_get_destinations():
  #send the get request
  response = client.get('/api/destinations')

  #check that the returned status code and data is correct
  assert response.status_code == 200
  assert type(response.json()) == dict

#Test for booking a trip
def test_book_trip():

  #test trip matching the BaseModel
  trip = {
    'passangers'  : ['Luukas'],
    'items'       : 'handbag',
    'destination' : 'mars'
  }

  response = client.post('/api/trips', json=trip)

  assert response.status_code == 200
  assert type(response.json()) == dict

def test_edit_trip():

  #find an existing trip id
  trips = json.load(open('trips.json'))
  existing_tripId = trips[0]['id']
  
  trip_edit = {
    'passangers' : ['Luukas', 'Esa'],
    'items'      : '2 handbags'
  }

  #uuid must match an existing trips id
  response = client.put(f'/api/trips/{existing_tripId}', json=trip_edit)

  assert response.status_code == 200
  assert type(response.json()) == dict

def test_delete_trip():

  #find an existing trip id
  trips = json.load(open('trips.json'))
  existing_tripId = trips[0]['id']

  response = client.delete(f'/api/trips/{existing_tripId}')

  assert response.status_code == 200
  assert type(response.json()) == dict