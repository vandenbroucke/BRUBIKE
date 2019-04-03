class ZipService():
    '''
    This class is able combine weather and device measurements dependent on their closest related timestamps
      
    Agrs: 
        is_logging_enabled (boolean): Indicates if console output should be printed
    '''
    def __init__(self,is_logging_enabled):
        ''' 
        The constructor for ZipService class.
        '''
        self.is_logging_enabled = is_logging_enabled

    def combine(self,input_dm,input_wm):
        ''' 
        Given two lists of measurements, one with interval timestamps and one with an individual timestamp, combine them to the closest fitting.

        Args:
            input_dm (list): List of device measurements
            input_wm (list): List of weather measurements

        Returns:
            List of combined weather & device measurements
        '''

        len_wm = len(input_wm)
        for dm_idx in range(len(input_dm)):
            ts_from = input_dm[dm_idx].get("timestamp_from")
            ts_until = input_dm[dm_idx].get("timestamp_until")          
            

            for wm_idx in range(len(input_wm)):
                ts_wm = input_wm[wm_idx].get("timestamp")
                ts_midpoint= (ts_from + ts_until)/2
                if(
                    (ts_from <= ts_wm and ts_wm < ts_until) or
                    ((wm_idx+1 < len_wm) and (abs(ts_midpoint-ts_wm) < abs(ts_midpoint - input_wm[wm_idx+1].get("timestamp")))) or
                    (wm_idx+1 == len_wm)
                ):
                    if(self.is_logging_enabled):print("Closest fit for dm[{} {}] was wm[{}]".format(ts_from,ts_until,input_wm[wm_idx]['timestamp']))
                    input_dm[dm_idx]['weather_timestamp']= input_wm[wm_idx]['timestamp']
                    input_dm[dm_idx]['temperature']= input_wm[wm_idx]['temperature']
                    input_dm[dm_idx]['weather_condition']= input_wm[wm_idx]['weather_condition']
                    input_dm[dm_idx]['wind_speed']= input_wm[wm_idx]['wind_speed']
                    input_dm[dm_idx]['wind_direction']= input_wm[wm_idx]['wind_direction']
                    input_dm[dm_idx]['humidity']= input_wm[wm_idx]['humidity']
                    input_dm[dm_idx]['barometer']= input_wm[wm_idx]['barometer']
                    input_dm[dm_idx]['visibility']= input_wm[wm_idx]['visibility']
                    break

        return input_dm
        



