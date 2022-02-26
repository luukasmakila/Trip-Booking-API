from fastapi import FastAPI
import helpers

#initializes the app
app = FastAPI()

#API endpoints
@app.get('/api/destinations')
async def get_destinations():
  destinations = await helpers.load_data('planets.json')
  return {'destinations': destinations}