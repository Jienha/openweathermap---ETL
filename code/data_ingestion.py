import polars as pl
from api_openweathermap import ApiOpenWeatherMap
import json
import time
import datetime as dt
from json_wather_parser import OpenWeatherMapParser

city_name = input("Enter city name : ")
api_key = input("Enter api-key : ")

api = ApiOpenWeatherMap(api_key=api_key)
api_response, api_data = api.get(city_name=city_name)

print(api_data)
# jdata = json.dumps(api_data, indent=4) # only for visualizzation:
# print(jdata)

# parser:
parser = OpenWeatherMapParser(api_data)
print()
print(parser.ingestion())
# print(parser._get_first_level_items(root_name=NAME, fields=FIELDS))