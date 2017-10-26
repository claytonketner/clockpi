import googlemaps
import pyowm
from datetime import datetime

from clockpi.secret import DIRECTIONS_DESTINATION
from clockpi.secret import DIRECTIONS_ORIGIN
from clockpi.secret import GMAPS_DIRECTIONS_API_KEY
from clockpi.secret import OWM_API_KEY
from clockpi.secret import OWM_CITY


def get_weather_temps(last_update_time, weather, cache_minutes=10):
    # Cache_minutes should be >= 1 due to their rate limits
    now = datetime.now()
    passed_minutes = (now - last_update_time).seconds/60
    if not weather or passed_minutes >= cache_minutes:
        new_temps = None
        try:
            owm = pyowm.OWM(OWM_API_KEY)
            city = owm.weather_at_place(OWM_CITY)
            owm_weather = city.get_weather()
            new_temps = owm_weather.get_temperature('fahrenheit')
            sunrise = owm_weather.get_sunrise_time()
            sunset = owm_weather.get_sunset_time()
        except Exception as e:
            print e.message
            weather = {}
        if new_temps:
            weather['low_temp'] = new_temps.get('temp_min')
            weather['high_temp'] = new_temps.get('temp_max')
            weather['current_temp'] = new_temps.get('temp')
            weather['sunrise'] = datetime.fromtimestamp(sunrise)
            weather['sunset'] = datetime.fromtimestamp(sunset)
        last_update_time = now
    return last_update_time, weather


def get_traffic(last_update_time, traffic, cache_minutes=5):
    # Google maps standard API allows 2500 requests/day, which is just over
    # two per minute
    now = datetime.now()
    passed_minutes = (now - last_update_time).seconds/60
    if not traffic or passed_minutes >= cache_minutes:
        directions = None
        try:
            cl = googlemaps.Client(key=GMAPS_DIRECTIONS_API_KEY)
            directions = cl.directions(
                DIRECTIONS_ORIGIN,
                DIRECTIONS_DESTINATION,
                mode='driving',
                departure_time=now)
        except Exception as e:
            print e.message
            traffic = {}
        if directions:
            # Only one destination, so just extract the first leg
            directions = directions[0]['legs'][0]
            duration = directions['duration']['value']
            # Google doesn't always include duration_in_traffic
            if directions.get('duration_in_traffic'):
                dur_in_traffic = directions['duration_in_traffic']['value']
            else:
                dur_in_traffic = duration
            if dur_in_traffic > duration:
                traffic['traffic_delta'] = (
                    dur_in_traffic - directions['duration']['value']) / 60
            else:
                traffic['traffic_delta'] = 0
            traffic['travel_time'] = (
                directions['duration_in_traffic']['value'] / 60)
        last_update_time = now
    return last_update_time, traffic
