# -*- coding: utf-8 -*-
"""IRIS Tracker.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-bZF9ZfBf6CRXPAFNVqUAJmb99dHxcmX

# Track Near Earth Object s

Fetching near earth object information using python and NASA NEO API. 


url : [NASA NeoWS docs](https://api.nasa.gov/#:~:text=NeoWs%20(Near%20Earth%20Object%20Web,browse%20the%20overall%20data%2Dset.)

![not actual image](https://www.gannett-cdn.com/presto/2020/06/04/USAT/a19efbc5-8b9f-4f60-9256-97252d62db75-VPC_ASTEROID_FLY-BY_SAT_wide.jpg?width=660&height=371&fit=crop&format=pjpg&auto=webp)
"""

# importing modules

import requests
from pprint import pprint

"""An api key isrequired to access the neo api. Get yourself a api key from here.

url : [Generate api key](https://api.nasa.gov/#:~:text=NeoWs%20(Near%20Earth%20Object%20Web,browse%20the%20overall%20data%2Dset)
"""

api_key = 'Mwi8JIeKHaMGPC0UO3M80cbMRc5hmoQ0hGs9iDIO'

"""Here, the api gives data for the given range of dates. I will be tracking the asteroids for between 6 and 7 decembers because at this date, asteroid 163348 (2002 NN4), a potentialy hazardous asteroid made a close approach to planet Earth."""

# url
#max limit 7 days
start_date = '2020-06-06'
end_date = '2020-06-07'
url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'
url

# making a request and getting data

r = requests.get(url)
data = r.json()
data

total = data['element_count']
neo = data['near_earth_objects']
print('Total asteroids :',total)
neo

for near in neo[start_date]:
    print(near['id'], near['name'], near['absolute_magnitude_h'])

"""You can also extract information of any particular one by passing the correct index"""

# asteroids by index in the list

first = neo[start_date][0]
first

"""## Searching About Asteroid : 163348 (2002 NN4)"""

# finding info by name

all_asteroids = neo[start_date]
for asteroid in all_asteroids:
    if asteroid['name'] == '163348 (2002 NN4)':
        pprint(asteroid)
        break

# asteroid name

asteroid['name']

# asteroid id

asteroid['id']

# nasa url

asteroid['nasa_jpl_url']

# Absolute magnitude : luminosity

asteroid['absolute_magnitude_h']

# diameter

dia = asteroid['estimated_diameter']
dia

# average diameter

avg_dia_m = (dia['meters']['estimated_diameter_min'] + dia['meters']['estimated_diameter_max']) / 2
avg_dia_m

# is potentially hazardous

asteroid['is_potentially_hazardous_asteroid']

# close approach date

close_data = asteroid['close_approach_data']
pprint(close_data)

"""Asteroids making close approach

url : [Earth Close approaches](https://cneos.jpl.nasa.gov/ca/)
"""

from time import ctime

date = close_data[0]['epoch_date_close_approach']
ctime(date)

# miss distance

miss_distance = close_data[0]['miss_distance']
miss_distance

# relative_velocity

rel_vel = close_data[0]['relative_velocity']
rel_vel

# is sentry object

asteroid['is_sentry_object']