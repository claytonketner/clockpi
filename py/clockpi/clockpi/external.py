import pyowm
from datetime import datetime

from clockpi.secret import OWM_API_KEY
from clockpi.secret import OWM_CITY


def get_weather_temps(last_update_time, temps, cache_minutes=30):
    # Cache_minutes should be >= 1 due to their rate limits
    now = datetime.now()
    passed_minutes = (now - last_update_time).seconds/60
    if not temps or passed_minutes >= cache_minutes:
        try:
            owm = pyowm.OWM(OWM_API_KEY)
            city = owm.weather_at_place(OWM_CITY)
            weather = city.get_weather()
            new_temps = weather.get_temperature('fahrenheit')
            temps['low_temp'] = new_temps.get('temp_min')
            temps['high_temp'] = new_temps.get('temp_max')
            temps['current_temp'] = new_temps.get('temp')
        except:
            # API is probably down
            temps['current_temp'] = None
            last_update_time = datetime.now()
    return last_update_time, temps
