import json

#contains all the helper functions

async def load_data(path):
  data = json.load(open(path))
  return data