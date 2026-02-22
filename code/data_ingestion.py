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
# while N < 5:
for city in city_name:
    api = ApiOpenWeatherMap(api_key=api_key)
    api_response, api_data = api.get(city_name=city)

    parser = OpenWeatherMapParser(api_data)
    data.append(parser.ingestion())
    N += 1
    # time.sleep(1)

df = pl.DataFrame(data)

print(df)

import sqlite3

db_path="db/flow_openweathermap.db"
# conn = sqlite3.connect(db_path)
conn_path = 'sqlite:///'+ db_path,
# print(conn)
# Carica il DataFrame sulla tabella specificata
df.write_database(
    table_name="meteo_table",
    connection= 'sqlite:///'+ db_path,
    if_table_exists="append"  # Crea la tabella se non esiste
)



df = pl.read_database_uri(query='select * from meteo_table', uri=db_path)
print(df)
