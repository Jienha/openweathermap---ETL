import json
import numpy as np
import math

# print(math.inf, type(math.inf), math.inf == math.inf, np.nan, type(np.nan))

class OpenWeatherMapParser:
    def __init__(self, data_raw:dict):
        self.data_raw = data_raw
        self.missing_data = 0
        self.where_missing_data = []

    def _get_coords(self, root_name='coord', error_value=404) -> dict:
        """
        Parsing the Open-Weather-Map's coodinates information.
        Geocoords (lat, lon) can't be exist outside determinate values (-90<=lat<=90, -180<=lon<=180).

        Dive into the steps:
            - check if Coord root exist: if yes ok, otherwise return lat, lon null
            - if Coord exist check the lat and lon reliable
        
        :return: {lon:value, lat:value}
        """
        k1 = self.data_raw.get(root_name, 0)

        if k1 != 0 and isinstance(k1, dict):
            lon = k1.get('lon', error_value)
            lat = k1.get('lat', error_value)

            # checking if lat, lon are reliable:
             
            if  isinstance(lon, float) == False or (lon > 180 or lon < -180):
                lon = np.nan
                self.missing_data += 1
                self.where_missing_data.append(root_name+'.lon')

            if isinstance(lat, float) == False or (lat > 90 or lat < -90):
                lat = np.nan
                self.missing_data += 1
                self.where_missing_data.append(root_name+'.lat')
            
            return {'lon':lon, 'lat':lat}
        
        # missing entire coodinates
        else: 
            self.missing_data += 2
            self.where_missing_data.extend([root_name+'.lon', root_name+'.lat'])
            return {'lon':np.nan, 'lat':np.nan}
        

    def _get_wather(self, root_name='weather', error_value=404):
        """
        Docstring for _get_wather
        
        :param self: ---
        :param root_name: Name of weather root
        :param error_value: Default value used for check the filds values
        """

        k1 = self.data_raw.get(root_name, 0)

        FILDS = {'id':int, 'main':str, 'description':str, 'icon':str}

        weather_vals = {}

        if k1 != 0 and isinstance(k1, list): # usually weather has list

            if len(k1) == 1 and isinstance(k1[0], dict):
                
                weather = k1[0]

                for field, field_type in FILDS.items():

                    if weather.get(field, error_value) != error_value and isinstance(weather.get(field), field_type):
                        weather_vals[root_name + '_' + field] = weather.get(field)
                    else:
                        self.missing_data += 1
                        self.where_missing_data.append(root_name+'.'+field)
                        weather_vals[root_name + '_' + field] = np.nan
                return weather_vals
            else:
                
                self.missing_data += 4
                self.where_missing_data.extend([
                    root_name+'.id', 
                    root_name+'.main', 
                    root_name+'.description', 
                    root_name+'.icon'
                ])
                return {
                    root_name + '_id': np.nan,
                    root_name + '_main': np.nan,
                    root_name + '_description': np.nan,
                    root_name + '_icon': np.nan
                }
        else:
            self.missing_data += 4
            self.where_missing_data.extend([
                root_name+'.id', 
                root_name+'.main', 
                root_name+'.description', 
                root_name+'.icon'
            ])
            return {
                root_name + '_id': np.nan,
                root_name + '_main': np.nan,
                root_name + '_description': np.nan,
                root_name + '_icon': np.nan
            }
    
    def _get_base(self, root_name='base', error_value=404):

        k1 = self.data_raw.get(root_name, error_value)

        if isinstance(k1, str):
            return {'base':k1}
        else:
            self.missing_data += 1
            self.where_missing_data.append(root_name)
            return {'base':k1}
        
    def _get_main(self, root_name="main", error_value=False):

        k1 = self.data_raw.get(root_name, error_value)

        