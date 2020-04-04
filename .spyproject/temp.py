# -*- coding: utf-8 -*


import pandas as pd 
import requests
from flask import Flask,render_template
import random
import time

latitude = 12.9716
longitude = 77.5946
file_name = 'data.csv'

def generate_random_data(lat, lon, num_rows, file_name):
	with open(file_name,'a') as output:
         output.write('timestamp,latitude,longitude\n')
         for _ in range(num_rows):
            time_stamp = time.time()
            generated_lat = random.random()/100
            generated_lon = random.random()/100
            output.write("{},{},{}\n".format(time_stamp, lat+generated_lat, lon+generated_lon))

generate_random_data(latitude,longitude, 10, file_name)

#---------Reading CSV to get latitude and Longitude---------
data = pd.read_csv("data.csv",skiprows=5,nrows=1) 

list_value = data.values.tolist()
#print(list_value[0])

#Latitude and Longitude
latitude = list_value[0][1]
longitude = list_value[0][2]

#---------Making API call and JSON Parsing---------
# api-endpoint
URL = "https://revgeocode.search.hereapi.com/v1/revgeocode"

#API key
api_key = 'oFSeZuYphZxrcwHnSv8-m-GpQGGsNSJkBoQB9yhOsic'

URLB = 'https://api.breezometer.com/air-quality/v2/current-conditions'
api_key_b = '04e5e54fbb994b3da64dd2634c0a5f8c'
PARAMSB = {
            'at': '{},{}'.format(latitude,longitude),
            'apikey':api_key_b
          }

# defining a params dict for the parameters to be sent to the API 
PARAMS = {
			'at': '{},{}'.format(latitude,longitude),
			'apikey': api_key
         }

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
rb = requests.get(url = URLB, params = PARAMSB)
# extracting data in json format 
data = r.json() 
datab = rb.json()
address = data['items'][0]['title'] 
color = datab['data']['baqi']['color']
#---------Flask Code for creating Map--------- 
app = Flask(__name__)
@app.route('/')

def map_func():
	return render_template('map.html',apikey=api_key,latitude=latitude,longitude=longitude,address=address)

if __name__ == '__main__':
	app.run(debug = False)
