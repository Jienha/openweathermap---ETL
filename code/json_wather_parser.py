import json
import numpy as np
import math

# print(math.inf, type(math.inf), math.inf == math.inf, np.nan, type(np.nan))

class OpenWeatherMapParser:
    def __init__(self, data_raw:dict):
        self.data_raw = data_raw
        self.missing_data = 0
        self.where_missing_data = []
        self._return_vals = {}

    def get_first_level_items(self, root_name:str, fields:dict, error_value=None):

        k1 = self.data_raw.get(root_name, error_value)

        max_errors = len(fields.keys())

        if k1 != 0 and isinstance(k1, dict):

            for field, field_type in fields.items():

                if isinstance(k1.get(field), field_type):
                    self._return_vals[root_name + '_' + field] = k1.get(field)
                else:
                    self.missing_data += 1
                    self.where_missing_data.append(root_name+'.'+field)
                    self._return_vals[root_name + '_' + field] = np.nan
        else:
            self.missing_data += max_errors
            for field, field_type in fields.items():
                self.where_missing_data.append(root_name+'.'+field)
                self._return_vals[root_name + '_' + field] = np.nan
        
        return self._return_vals
        
    def get_first_level_items_customlist(self, root_name, fields:dict, error_value=None):
        """
        Docstring for _get_wather
        
        :param self: ---
        :param root_name: Name of weather root
        :param error_value: Default value used for check the filds values
        """

        k1 = self.data_raw.get(root_name, error_value)

        max_errors = len(fields.keys())

        if k1 != 0 and isinstance(k1, list): # usually weather has list

            if len(k1) == 1 and isinstance(k1[0], dict):
                
                k2 = k1[0]

                for field in k2.keys():
                    print(field)
                    if k2.get(field, error_value) != error_value:
                        self._return_vals[root_name + '_' + field] = k2.get(field)
                    else:
                        self.missing_data += 1
                        self.where_missing_data.append(root_name+'.'+field)
                        self._return_vals[root_name + '_' + field] = np.nan
                return self._return_vals
            else:
                self.missing_data += max_errors
                for field, field_type in fields.items():
                    self.where_missing_data.append(root_name+'.'+field)
                    self._return_vals[root_name + '_' + field] = np.nan
        else:
            self.missing_data += max_errors
            for field, field_type in fields.items():
                self.where_missing_data.append(root_name+'.'+field)

                if field_type in (float, int): 
                    self._return_vals[root_name + '_' + field] = np.nan
                else:
                    self._return_vals[root_name + '_' + field] = ''
        return self._return_vals
        
    def get_zero_level_item(self, root_name, error_value=None):

        k1 = self.data_raw.get(root_name, error_value)

        if isinstance(k1, str):
            self._return_vals[root_name] = k1
            return self._return_vals
        else:
            self.missing_data += 1
            self.where_missing_data.append(root_name)
            self._return_vals = k1
            return self._return_vals

    def ingestion(self, data_sourse='Openweathermap'):
        cols = {
            'coord':1, 
            'weather': -1, 
            'base': 0, 
            'main': 1, 
            'visibility': 0, 
            'wind': 1, 
            'clouds': 1,
            "sys": 1,
            'timezone': 0, 
            'id': 0, 
            'name': 0,
        }

        fields = [
            {'lon': float, 'lat': float},
            {'id': int, 'main': str, 'description': str, 'icon': str},
            {
                'temp': float, 'feels_like': float, 'temp_min': float, 
                'temp_max': float, 'pressure': int, 'humidity': int, 
                'sea_level': int, 'grnd_level': int
            },
            {'speed': float, 'deg': int},
            {'all': int},
            {'type': int, 'id': int, 'country': str, 'sunrise': int, 'sunset': int}
        ]

        counter = 0
        for col, method in cols.items():
            if method == 1:
                field = fields[counter]
                self.get_first_level_items(root_name=col, fields=field)
                counter += 1

            elif method == -1:
                field = fields[counter]
                self.get_first_level_items_customlist(root_name=col, fields=field)
                counter += 1
            
            else:
                field = fields[counter]
                self.get_zero_level_item(root_name=col)
                counter += 1

        return self._return_vals


if __name__ == '__main__':
    pass

        # FILDS = {
        #     'temp':float,
        #     'feels_like':float,
        #     'temp_min':float, 
        #     'temp_max':float,
        #     'pressure':float,
        #     'humidity':float,
        #     'sea_level':float, 
        #     'grnd_level':float
        # }

        # main_vals = {}


        