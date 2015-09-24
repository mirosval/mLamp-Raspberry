from __future__ import print_function, division
import urllib.request
import json
import logging
import sys

logging.basicConfig(filename="weather.log", level=logging.DEBUG, format='%(asctime)s %(message)s')

# here you can actually configure the location for which you want to retrieve the weather data
base_url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Prague,cz&mode=json&units=metric&cnt=1"

try:
    response = urllib.request.urlopen(base_url)
    weather_forecast = json.loads(response.read().decode())
except:
    logging.error("Failed to connect to the weather server")
    sys.exit(1)

forecast_temp = weather_forecast['list'][0]['temp']['day']

logging.info("Forecast Temp: {}".format(forecast_temp))

with open("daily_temp.txt", 'w') as f:
    f.write(str(forecast_temp))
