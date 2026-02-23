import polars as pl
from api_openweathermap import ApiOpenWeatherMap
import os 
import time
import datetime as dt
from json_weather_parser import OpenWeatherMapParser
from pathlib import Path
import yaml
import sqlite3


# base dir:
BASE_DIR = Path(__file__).resolve().parent.parent

# path:
config_path = BASE_DIR / "config" / "params.yaml"
db_path= os.path.join(BASE_DIR ,"db/flow_openweathermap.db")
print(db_path)
conn_path = 'sqlite:///'+ db_path

# DATABASE.TABLES:
INGESTION_TABLE = 'ingestion_weather'


df = pl.read_database_uri(query=f'select * from ingestion_weather', uri=conn_path)
print(df)