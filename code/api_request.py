import requests, json

# API key:
api_key = "33359c4e6ea3af57c064722607c60854"

city_name = input("Enter city name : ")
# base url:
base_url = "http://api.openweathermap.org/data/2.5/weather?"
complete_url = base_url +"q=" + city_name + "&appid=" + api_key 

print(complete_url)
# get method of requests module
# return response object
response = requests.get(complete_url)
data_json = response.json()

print(type(data_json))

for key, value in data_json.items():
    print(f"{key}: {value}")