import polars as pl
from api_openwathermap import ApiOpenWatherMap
import json
import time
import datetime as dt
from json_wather_parser import OpenWeatherMapParser

city_name = input("Enter city name : ")
api_key = input("Enter api-key : ")

api = ApiOpenWatherMap(api_key=api_key)
api_response, api_data = api.get(city_name=city_name)

# api_data['coord']['lon'] = 90.
# api_data['coord']['lat'] = 10.
# api_data.pop('weather')
# api_data['weather'][0]['main'] = 10 
# api_data['weather'][0]['description'] = 200
# api_data['weather'][0]['icon'] = 200

jdata = json.dumps(api_data, indent=4) # only for visualizzation:
print(jdata)

# parser:
parser = OpenWeatherMapParser(api_data)

# print('coordinate:', parser._get_coords())

# print('meteo data:', parser._get_wather())

# print(parser.missing_data)
# print(parser.where_missing_data)


# ## get data:
# #  coord:
# lon = api_data.get('coord').get('lon')
# lat = api_data.get('coord').get('lat')
# # wather:
# id = api_data.get('weather')[0].get('id')
# main = api_data.get('weather')[0].get('main')
# description = api_data.get('weather')[0].get('description')
# icon = api_data.get('weather')[0].get('icon')
# base information:
base = api_data.get('base')
# main temperature:
temp = api_data.get('main').get('temp')
feels_like = api_data.get('main').get('feels_like')
temp_min = api_data.get('main').get('temp_min')
temp_max = api_data.get('main').get('temp_max')
pressure = api_data.get('main').get('pressure')
humidity = api_data.get('main').get('humidity')
sea_level = api_data.get('main').get('sea_level')
grnd_level = api_data.get('main').get('grnd_level')
# visibility:
visibility = api_data.get('visibility')
# wind:
speed = api_data.get('wind').get('speed')
deg = api_data.get('wind').get('deg')
gust = api_data.get('wind').get('gust')
# clouds:
clouds_all = api_data.get('clouds').get('all')
# dt: 
time_data_calculation = api_data.get('dt')
# sys:
country_code = api_data.get('sys').get('country')
sunrise = api_data.get('sys').get('sunrise')
sunset = api_data.get('sys').get('sunset')
# timezone:
timezone = api_data.get('timezone')
city_id = api_data.get('id')
city_name = api_data.get('name')
api_code_response = api_data.get('cod')
