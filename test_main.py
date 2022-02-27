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
    "passangers"  : ["Luukas"],
    "items"       : "handbag",
    "destination" : "mars"
  }

  response = client.post('/api/trips', json=trip)

  assert response.status_code == 200