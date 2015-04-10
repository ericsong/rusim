from pymongo import MongoClient
import requests
import datetime
import json

response = requests.get('http://runextbus.heroku.com/active')
active_data = response.json()
client = MongoClient()
db = client.rusim
bus_data = {}

#record predictions for every route
for route in active_data['routes']:
  response = requests.get('http://runextbus.heroku.com/route/' + route['tag'])
  data = response.json()  

  bus_data['routes'] = data

#record predictions for every stop
for stop in active_data['stops']:
  response = requests.get('http://runextbus.heroku.com/stop/' + stop['title'])
  data = response.json()
  
  bus_data['stops'] = data

#record locations data
response = requests.get('http://runextbus.heroku.com/locations')
data = response.json()
bus_data['locations'] = data

#record current time
bus_data['time'] = str(datetime.datetime.now())

db.bus_data.insert_one(bus_data)
