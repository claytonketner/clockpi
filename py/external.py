import pyowm
from datetime import datetime

from secret import OWM_API_KEY
from secret import OWM_CITY


TIME_FORMAT = "%Y %m %d %H %M %S"


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
            temps['low_temp'] = int(new_temps['temp_min'])
            temps['high_temp'] = int(new_temps['temp_max'])
            temps['current_temp'] = int(new_temps['temp'])
        except:
            # owm api is probably down
            pass
        finally:
            # If the api call failed, the service is probably just temporarily
            # down
            last_update_time = datetime.now()
    return last_update_time, temps
