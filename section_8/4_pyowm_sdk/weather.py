# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pyowm


# Docs about the API can be found at: http://openweathermap.org/api
from pyowm.webapi25 import forecaster

if __name__ == '__main__':

    API_KEY = 'your_API_key'

    # Instantiate the OWM API client
    owm = pyowm.OWM(API_KEY)

    # --- Retrieve the city ID corresponding to Tokio, JP ---
    print('Retrieving information about Tokyo')
    city_registry = owm.city_id_registry()
    ids_for_tokyo = city_registry.ids_for('Tokyo', 'JP')
    tokyo = ids_for_tokyo[0]
    tokyo_id = tokyo[0]
    print('Found Tokyo in registry lookup: {}'.format(tokyo))

    # --- Retrieve the current weather in Tokyo ---
    # We want:
    #  - sky status
    #  - current temperature in Celsius
    #  - humidity percentage
    print('\n*** Querying OWM API for current weather in Tokyo...')
    observation = owm.weather_at_id(tokyo_id)  # observation = weather at a location now
    weather = observation.get_weather()
    temperature_celsius= weather.get_temperature('celsius').get('temp', None)
    print('\nWeather now is: {}'.format(weather.get_status()))
    print('Current temperature is: {} celsius'.format(temperature_celsius))
    print('Current humidity is: {} %'.format(weather.get_humidity()))

    # --- But... where is Tokyo on the map? ---
    tokyo_location = observation.get_location()
    print("\nTokyo's geographic coordinates: lat={}, lon={}".format(
        tokyo_location.get_lat(),
        tokyo_location.get_lon()
    ))

    # --- Forecast for tomorrow in Tokyo: will it be rainy tomorrow? ---
    # utility method to get tomorrow's datetime
    tomorrow = pyowm.timeutils.tomorrow()
    print('\n*** Querying OWM API for daily weather forecasts for Tokyo...')
    forecaster = owm.daily_forecast_at_id(tokyo_id)  # daily forecasts for the next few days
    will_be_rainy = forecaster.will_be_rainy_at(tomorrow)
    print('\nWill tomorrow rain in Tokyo? {}'.format(
        'Yes' if will_be_rainy else 'No'
    ))
