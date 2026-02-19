import polars as pl
from api_openweathermap import ApiOpenWeatherMap
import json
# import pandas as pd
import time
import datetime as dt
from json_wather_parser import OpenWeatherMapParser

city_name = [city.strip() for city in input("Enter city name : ").split(',')]
api_key = input("Enter api-key : ")


print(city_name)
N = 0
data = []
while N < 5:
    for city in city_name:
        api = ApiOpenWeatherMap(api_key=api_key)
        api_response, api_data = api.get(city_name=city)

        parser = OpenWeatherMapParser(api_data)
        data.append(parser.ingestion())
    N += 1
    time.sleep(10)

df = pl.DataFrame(data)
print(df)
