from main import app
from fastapi.testclient import TestClient

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
  
  trip_edit = {
    'passangers' : ['Luukas', 'Esa'],
    'items'      : '2 handbags'
  }

  #uuid must match an existing trips id
  response = client.put('/api/trips/d70dc76b-98b3-11ec-bc8a-b07d64f3b131', json=trip_edit)

  assert response.status_code == 200
  assert type(response.json()) == dict

def test_delete_trip():
  response = client.delete('/api/trips/d70dc76b-98b3-11ec-bc8a-b07d64f3b131')

  assert response.status_code == 200
  assert type(response.json()) == dict