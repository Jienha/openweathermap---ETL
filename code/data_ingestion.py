import polars as pl
from api_openweathermap import ApiOpenWeatherMap
import os 
import time
import datetime as dt
from json_weather_parser import OpenWeatherMapParser
from pathlib import Path
import yaml
import sqlite3

# db_path="db/flow_openweathermap.db"
# conn_path = 'sqlite:///'+ db_path,

# base dir:
BASE_DIR = Path(__file__).resolve().parent.parent

# path:
config_path = BASE_DIR / "config" / "params.yaml"
db_path= os.path.join(BASE_DIR ,"db/flow_openweathermap.db")
print(db_path)
conn_path = 'sqlite:///'+ db_path



# config file informations:
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

ingestion_config = config['ingestion']
CITIES = ingestion_config['cities']
KEY = ingestion_config['key']
TIMEOUT_SECONDS = ingestion_config['timeout_seconds']


N = 0
while N < 3:
    data = []
    timestamp = dt.datetime.now()
    for city in CITIES:
        api = ApiOpenWeatherMap(api_key=KEY)
        api_response, api_data = api.get(city_name=city)

        parser = OpenWeatherMapParser(api_data)
        data.append(parser.ingestion())

    df = pl.DataFrame(data)
    df = df.with_columns(pl.lit(timestamp).alias("ingestion_datetime"))

    df.write_database(
        table_name="ingestion_weather",
        connection= 'sqlite:///'+ db_path,
        if_table_exists="append"  # Crea la tabella se non esiste
    )

    print(N)
    print(df)
    N += 1

    time.sleep(TIMEOUT_SECONDS)







# df = pl.read_database_uri(query='select * from meteo_table', uri=db_path)
# print(df)
