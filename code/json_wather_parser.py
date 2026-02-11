import json
import numpy as np
import math

print(math.inf, type(math.inf), math.inf == math.inf, np.nan, type(np.nan))

class OpenWeatherMapParser:
    def __init__(self, data_raw:dict):
        self.data_raw = data_raw
        self.missing_data = 0
        self.wher_missing_data = []

    def _get_coords(self) -> dict:
        """
        Parsing the Open-Weather-Map's coodinates information
        
        :return: {lon:value, lat:value}
        """
        k1 = self.data_raw.get('coord', 0)

        if k1 != 0 and isinstance(k1, dict):
            lon = k1.get('lon', 404)
            lat = k1.get('lat', 404)

            # checking if lat, lon are reliable:
             
            if  lon > 180 or lon < -180:
                lon = np.nan
                self.missing_data += 1
                self.wher_missing_data.append('coord.lon')

            if lat > 90 or lat < -90:
                lat = np.nan
                self.missing_data += 1
                self.wher_missing_data.append('coord.lat')
            
            return {'lon':lon, 'lat':lat}
        
        # missing entire coodinates
        else: 
            self.missing_data += 2
            self.wher_missing_data.extend(['coord.lon', 'coord.lat'])
            return {'lon':np.nan, 'lat':np.nan}
        
    # def _get_wather(self):

    #     k1 = self.data_raw.get('weather', 0)

    #     # if k1 != 0 and isinstance(k1, dict):


