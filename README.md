# Trip-Booking-API for Oura backend developer intern

Created a trip booking API for space traveling using the FastAPI framework. </br>

# How to use?:
  1. Download the repository to your machine
  2. Check the requirements.txt and install the required packages (in project folder type: <b>pip install -r requirements.txt</b>)
  3. cd into the folder and run: <b>uvicorn main:app</b> / <b>uvicorn main:app --reload</b> (for developement mode)
  4. If step 2 doesn't work run: <b>python -m uvicorn main:app --reload</b>
  5. After the server is running open http://localhost:8000/docs on your browser (Chrome is reccomended)
  6. Here you can see all the API endpoints and send test requests to them by opening one of the routes and clicking "Try it out" and then execute
  7. You can also view the BaseModel schemas created for trips
  8. Now if you want to run the tests i've created cd into the folder and run: <b>pytest</b>
  9. For edit and delete trip tests you will need to provide a valid uuid for the trip manually (sorry)

# I went with FastAPI for the following reasons: </br>
  1. To challenge myself and learn a new amazing framework companies actually use in production
  2. FastAPI is the fastest python web framework
  3. Simple and fast to code out
  4. Asynchronous function support
  5. Automatic documentation and data validation
  6. Can be hooked up to a React frontend easily (for my future personal projects this is a nice feature)

# What did I learn?:
  1. Creating API's with Python
  2. Testing API's with python
  3. Handling JSON data with Python (A bit messier than with JS)
  4. What query parameters are
  5. What a uuid is
  6. Creating DB models with pydantic
  7. Making DB fielads and parameters optional with Python

# What did I succeed in?:
  1. Writing clean readable and functioning code
  2. Seperating the code in multiple functions and files
  3. Commenting out what every non self explainatory piece of code does

# What could be improved on?:
  1. I feel like every application can be more optimized
  2. If the project was larger, then the folder structure would be different aswell
  3. At some places theres repetitive code
