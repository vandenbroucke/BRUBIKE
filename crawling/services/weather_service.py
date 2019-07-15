from datetime import datetime,timedelta, date
from time import mktime,sleep
import demjson,requests

class WeatherService():
    '''
    This class is able to load in historical weather information on city level 
      
    Agrs: 
        is_logging_enabled (boolean): Indicates if console output should be printed 
    Attributes:
    '''

    API_WEATHER_HISTORY = "https://www.timeanddate.com/scripts/cityajax.php?n=belgium/{}&mode=historic&hd={}&month={}&year={}&json=1"


    def __init__(self,is_logging_enabled):
        ''' 
        The constructor for WeatherService class. 
        '''
        self.is_logging_enabled =  is_logging_enabled
        pass




    def daterange(self,start_date, end_date):
        ''' 
        Generator function for dates between interval

        Args:
            start_date (datetime): Date as start of interval
            end_date (datetime): Date as end of interval
        '''  
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def __get_meteo_day(self,input_city_name,input_date):  
        ''' 
        Retrieves all historic weather measurements for a given date and city name

        Args:
            input_city_name (string): Name of the city of which to recieve weather data
            input_date (datetime): Date object for which day to receive historic data

        Returns:
            A list of weather measurements of a city for a specific day
        '''  
        meteo_URL = self.API_WEATHER_HISTORY.format(input_city_name,input_date.strftime('%Y%m%d'),input_date.month,input_date.year)
        response = demjson.decode((requests.get(meteo_URL).text))
        datapoints =[]

        for dp in response:
            hour_string = dp['c'][0]['h'].split('<br>')[0].strip()
            timestamp = datetime.strptime("{} {}".format(str(input_date),hour_string), "%Y-%m-%d %H:%M").timestamp()

            temperature = dp['c'][2]['h'].split('&')[0].strip()

            weather_condition = dp['c'][3]['h']

            wind_speed = dp['c'][4]['h'].split(' ')[0].strip()

            wind_direction = dp['c'][5]['h'].split('"')[3]

            humidity = dp['c'][6]['h'][:-1]

            barometer = dp['c'][7]['h'].split(' ')[0].strip()

            visibility = dp['c'][8]['h'].split('&')[0].strip()

            datapoints.append({
                'timestamp':round(timestamp),
                'temperature':temperature,
                'weather_condition':weather_condition,
                'wind_speed':wind_speed,
                'wind_direction':wind_direction,
                'humidity':humidity,
                'barometer':barometer,
                'visibility':visibility
            })
        return datapoints


    def get_meteo_for_interval(self,start_date,end_date,city_name):
        ''' 
        Retrieves all historic weather measurements for a given datespan and city name

        Args:
            start_date (datetime): Date object as start of interval
            end_date (datetime): Date object as end of interval
            city_name (string): Name of the city of which to recieve weather data
            

        Returns:
            A list of weather measurements of a city for a specific day
        '''  
        weather_measurements=[]

        for single_date in self.daterange(start_date, end_date):
            if(self.is_logging_enabled):print('Retrieving meteo data for {}'.format(single_date))
            weather_measurements.extend(self.__get_meteo_day(city_name,single_date))     
            sleep(.5)
        return weather_measurements
