import json, requests
from datetime import datetime

class DeviceService():
    '''
    This class is able to load in bike_counting devices from the Brussels Mobility API
      
    Agrs: 
        devices_path (string): Path to a JSON file containing devices names with their corresponding geo location ([lat long])
        is_logging_enabled (boolean): Indicates if console output should be printed

    Attributes:
        devices_path (string): Path to a JSON file containing devices names with their corresponding geo location ([lat long])
        API_DEVICE_HISTORY (string): Unformatted URL for retrieving device history, accepts featureID, startdate & enddate
    '''

    API_DEVICE_HISTORY = "https://data-mobility.brussels/bike/api/counts/?request=history&featureID={}&startDate={}&endDate={}&outputFormat=json"


    def __init__(self,devices_path,is_logging_enabled):
        ''' 
        The constructor for deviceService class. Loads in devices from given path to a list of devices. 
        '''
        self.devices_path = devices_path
        self.devices=[]
        self.is_logging_enabled = is_logging_enabled
        self.load_devices()


    def load_devices(self):
        ''' 
        Loads in JSON formatted devices as list of devices
        '''    
        with open(self.devices_path) as devices_files:     
            try:
                self.devices = json.load(devices_files)
            except Exception as ex:
                print("ERROR:[{}] loading path {}".format(ex,self.devices_path))


    def get_device_history(self,d_id,d_geo,s_date,e_date):
        ''' 
        Retrieves all the history measurements for a given device name and interval

        Args:
            d_id (string): Device name
            d_geo (list): [0] Latitude & [1] Longitude of the device
            s_date (string): Start from interval formatted as YYYYMMDD
            e_date (string): End from interval formatted as YYYYMMDD

        Returns:
            A formatted list of measurements containing device name, location and obtained metrics per measurement.
        '''
        history =[]
        time_gap_dictionary ={}
        try:
            response = json.loads(requests.get(self.API_DEVICE_HISTORY.format(d_id,s_date,e_date)).text)

            #gap: [0=index, 1=startTime, 2=endTime]     
            for gap in response['timeGaps']:
                time_gap_dictionary[gap[0]] = [gap[1],gap[2]]       
               
            #m: measurement (count_date, time_gap)
            for m in response['data']:

                time_gap = time_gap_dictionary[m.get('time_gap')]      
                #fix negative interval        
                if(time_gap[1] == '00:00:00'):time_gap[1] = '23:59:59' 
                
                #POSIX timestamps for timegap interval
                posix_from = round(datetime.strptime("{} {}".format(m.get('count_date'),time_gap[0]),"%Y/%m/%d %H:%M:%S").timestamp())
                posix_until = round(datetime.strptime("{} {}".format(m.get('count_date'),time_gap[1]),"%Y/%m/%d %H:%M:%S").timestamp())

                history.append({
                    "device_name":d_id,
                    "latitude":d_geo[0],
                    "longitude":d_geo[1],
                    "timestamp_from":posix_from,
                    "timestamp_until":posix_until,
                    "bike_count":m.get('count'),
                    "bike_avg_speed":m.get('average_speed')
                })

        except Exception as ex:
            print(ex)
        return history

    def get_measurements_from_all_devices(self,s_date,e_date):
        ''' 
        For all loaded devices, retrieve their history and combine them as a set of measurements

        Args:
            s_date (string): Start from interval formatted as YYYYMMDD
            e_date (string): End from interval formatted as YYYYMMDD

        Returns:
            A formatted list of measurements containing device names, locations and obtained metrics per measurement.
        '''
        measurements = []
        for d in self.devices:
            if(self.is_logging_enabled):print("FETCHING_HISTORY:{}".format(d.get('name')))
            measurements.extend(
                self.get_device_history(d.get('name'),d.get('geo'),s_date,e_date))
        return measurements




