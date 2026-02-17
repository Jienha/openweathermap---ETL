import requests
import json


class ApiOpenWeatherMap():
    def __init__(self, api_key, base_url="http://api.openweathermap.org/data/2.5/weather?", metric="metric"):
        self.key = api_key
        self.base_url = base_url
        self.metric = metric

    def _url(self, city_name):
        return (
            self.base_url +
            f"q=" + city_name + # City 
            "&units=" + self.metric + # Read documentation for more infomations
            "&appid=" + self.key
            )

    def get(self, city_name):
        url_call = self._url(city_name)
        response = requests.get(url_call)
        return response, response.json()

if __name__ == "__main__":
    
    city_name = input("Enter city name : ")
    api_key = input("Enter api-key : ")

    api_owm = ApiOpenWeatherMap(api_key=api_key)
    response, data = api_owm.get(city_name=city_name)
    
    for key, value in data.items():
        print(f"{key}: {value}")