from connect_to_wifi import *
import urequests
import json


connect_to_internet('ala247', 'coolfinch947')

API_KEY = '2701fdbfb6418b9d28951a50f1cf3cda'
CITY = 'Iowa+City'
URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}'

def get_weather_forecast(url):
    response = urequests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        print("Failed to fetch data")
        return None
    
def process_forecast_data(forecast_data):
    daily_data = {}
    # Organize data by date
    for each_reading in forecast_data['list']:
        date = each_reading['dt_txt'].split()[0]
        temp = each_reading['main']['temp']
        weather = each_reading['weather'][0]['description']
        
        if date not in daily_data:
            daily_data[date] = {'temps': [], 'weathers': []}
        
        daily_data[date]['temps'].append(temp)
        daily_data[date]['weathers'].append(weather)
    
    # Sort dates and calculate average temperatures and find the most common weather description
    aggregated_daily_data = []
    for date in sorted(daily_data.keys()):
        data = daily_data[date]
        avg_temp = sum(data['temps']) / len(data['temps'])
        most_common_weather = max(set(data['weathers']), key=data['weathers'].count)
        
        aggregated_data = {}
        aggregated_data['Date'] = date
        aggregated_data['Temp'] = round(avg_temp, 2)
        aggregated_data['Description'] = most_common_weather
        aggregated_daily_data.append(aggregated_data)
    return aggregated_daily_data