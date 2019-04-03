from services.device_service import DeviceService
from services.weather_service import WeatherService
from services.zip_service import ZipService
from datetime import timedelta,date
import json

DEVICES_INPUT_PATH="./data/devices.json"
BIKE_OUTPUT_PATH = './data/bike_data.tsv'
WEATHER_OUTPUT_PATH ='./data/weather_data.tsv'
COMBINED_OUTPUT_PATH ='./data/combined_data.tsv'


if __name__ == "__main__":    
    device_service =  DeviceService(DEVICES_INPUT_PATH,True)
    #Fetch and parse all device measurements
    device_measurements =  device_service.get_measurements_from_all_devices("20180101","20190311")    
    #Store raw device measurements
    with open(BIKE_OUTPUT_PATH, 'w') as file:
        file.write('device_name\tlatitude\tlongitude\ttimestamp_from\ttimestamp_until\tbike_count\tbike_avg_speed\n')
        for m in device_measurements:
            file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(m['device_name'],m['latitude'],m['longitude'],m['timestamp_from'],m['timestamp_until'],m['bike_count'],m["bike_avg_speed"]))
        print("Bike_data.tsv was written")
    
    weather_service = WeatherService(True)
    #Fetch and parse all weather measurements
    weather_measurements = weather_service.get_meteo_for_interval(date(2018,12,6),date(2019,3,11),'brussels')
    
    #Store raw weather measurements
    with open(WEATHER_OUTPUT_PATH, 'w') as file:
        file.write('timestamp\ttemperature\tweather_condition\twind_speed\twind_direction\thumidity\tbarometer\tvisibility\n')
        for m in weather_measurements:
            file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(m['timestamp'],m['temperature'],m['weather_condition'],m['wind_speed'],m['wind_direction'],m['humidity'],m['barometer'],m["visibility"]))

   
    #Combine measurements where the closest matching weather data is attached to a device measurement
    zip_service = ZipService(False)
    combined_measurements = zip_service.combine(device_measurements,weather_measurements)
    with open(COMBINED_OUTPUT_PATH, 'w') as file:
        file.write('device_name\tlatitude\tlongitude\ttimestamp_from\ttimestamp_until\tbike_count\tbike_avg_speed\tweather_timestamp\ttemperature\tweather_condition\twind_speed\twind_direction\thumidity\tbarometer\tvisibility\n')
        for m in combined_measurements:
            file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(m['device_name'],m['latitude'],m['longitude'],m['timestamp_from'],m['timestamp_until'],m['bike_count'],m["bike_avg_speed"],m['weather_timestamp'], m['temperature'],m['weather_condition'],m['wind_speed'],m['wind_direction'],m['humidity'],m['barometer'],m["visibility"]))
