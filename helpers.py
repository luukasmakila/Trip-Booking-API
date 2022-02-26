import json

#contains all the helper functions

#loads data from a JSON file (could be a db in production)
async def load_data(path):
  data = json.load(open(path))
  return data