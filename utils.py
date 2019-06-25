import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import json
import requests
from datetime import datetime as dt
def check_if_the_tsv_hot_file_already_has_processed_columns(csv_file_path):
	df = pd.read_csv(csv_file_path,delimiter="\t")
	try:
		total_rows=len(df.Sunny)
		return True
	except Exception as e:
		return False	
def remove_features(df):
    return df.drop(columns=[        
    'device_name',
    'timestamp_until',
    'bike_avg_speed',
    'weather_timestamp',
    'wind_direction',
    'wind_speed',
    'barometer',
    'visibility',
    'Ice fog',
    'Thundershowers',
    'Sprinkles',
    'Broken clouds',
    'Rain showers',
    'Snow flurries',
    'Light fog',
    'Sleet',
    'Cloudy',
    'Quite cool'    
])
def remove_outlier(df_in, col_name):
    """Removes all outliers on a specific column from a given dataframe.

    Args:
        df_in (pandas.DataFrame): Iput pandas dataframe containing outliers
        col_name (str): Column name on which to search outliers

    Returns:
        pandas.DataFrame: DataFrame without outliers
    """         
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1  # Interquartile range
    fence_low = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    return df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)] 
def update_one_hot_data(combined_path,weather_combined_path):
    if not check_if_the_tsv_hot_file_already_has_processed_columns(weather_combined_path):
        df = pd.read_csv(combined_path,
                         sep='\t',
                         header=0) 
        weather_unique_combinations = df.weather_condition.unique()

        #Get list of all unique weather types
        types = []
        for el in weather_unique_combinations:
            for wc in el.split('.'):
                if(wc != ''):            
                    types.append(wc.strip())
        true_unique =  set(types)

        #Add columns with default value 0 for all unique weather types
        for unique_weather_type in true_unique:
            df[unique_weather_type]=0

        #Loop over all records and set value to 1 for their corresponding weather_types
        for index, row in df.iterrows():
            row_types = []
            for wc in row["weather_condition"].split('.'):
                if(wc != ''):            
                    row_types.append(wc.strip())
            for t in row_types:
                df.at[index,t]=1


        #remove empty windspeeds
        df = df[df.wind_speed.apply(lambda x: str(x).isnumeric())]

        #remove original weather_condition column and store, to avoid rerun
        df =  df.drop(columns="weather_condition")
        df.to_csv(weather_combined_path,
                  sep='\t',
                  index=False,
                  header=True)    
    else:
        print("File already processed.")
def evaluate_model_and_show_graph(x_test,y_test,model,y_scaler):
    model.evaluate(x_test, y_test)

    #x_test = x_train
    #y_test = y_train

    #x_test = x_test[14500:]
    #print(x_test)
    #y_test = y_test[14500:]


    y_prediction = model.predict(x_test)
    print(y_prediction)

    y_pred_scaled = y_scaler.inverse_transform(y_prediction)



    y_test_scaled = y_scaler.inverse_transform(y_test)
    mse = mean_squared_error(y_pred_scaled, y_test_scaled)
    mae=mean_absolute_error(y_pred_scaled, y_test_scaled)
    print("MSE: "+str(mse))
    print("MAE: "+str(mae))

    plt.rcParams['figure.figsize'] = [18, 18]
    l1, = plt.plot(y_test_scaled, 'g')
    l2, = plt.plot(y_pred_scaled, 'r', alpha=0.7)
    plt.legend(['Ground truth', 'Predicted'])
    plt.show()

def return_time_slice_column_value(timestamp,time_slice_day):
	
	date=dt.fromtimestamp(timestamp)
	seconds_day=(date - date.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()	
	window_time=86400/time_slice_day	
	return int(seconds_day/window_time)
def return_proper_weather_condition(weather_cond):
	
	return_string='Clear.'
	if weather_cond=='Mostly Sunny':
		return_string='Sunny.'
	if weather_cond=='Cloudy':
		return_string='Cloudy.'
	if weather_cond=='Mostly Cloudy':
		return_string='Cloudy.'
	if weather_cond=='Partly Cloudy':
		return_string='Partly cloudy.'
	if weather_cond=='Mostly Clear':
		return_string='Clear.'
	
	return return_string
def obtain_latitudes_long_list(path='./data/devices.json'):	
	lat_long_list=[]
	with open(path) as json_file:
		data=json.load(json_file)
		for row in data:
			lat_long_list.append(row['geo'])			
	return lat_long_list
def add_lost_columns(path,columns_name_list):
	df = pd.read_csv(path,delimiter="\t")
	total_rows=len(df.timestamp_from)
	for col in columns_name_list:			
		new_list=[]
		for i in range(0,total_rows):
			new_list.append(0)
		
		df[col] = new_list
		df.to_csv(path,sep='\t',index=False)
def create_on_hot_next_dates_file(path, new_path):	
	add_lost_columns(path,['Ice fog', 'Snow flurries', 'Light fog' ,'Quite cool','Rain','Sleet','Haze','Freezing rain','Cool','Fog','Light rain','Light freezing rain','Cloudy','Light snow','Chilly','Drizzle','Low clouds','Rain showers','Snow','Scattered showers','Snow showers','Hail','Thundershowers','Sprinkles','Thunderstorms','Partly sunny','Partly cloudy','Scattered clouds','Broken clouds','Passing clouds'])    
	from shutil import copyfile	
	copyfile(path, new_path)


def obtain_next_dates_data(start_date,end_date):    
    combined_start_time=int(dt.timestamp(dt.combine(start_date,dt.min.time())))
    combined_end_time=int(dt.timestamp(dt.combine(end_date,dt.min.time())))   
    device="N"    
    Next_dates_PATH = './data/next_dates_data.tsv'
    with open(Next_dates_PATH, 'w') as file:
        file.write('device_name\tlatitude\tlongitude\ttimestamp_from\ttimestamp_until\tbike_count\tbike_avg_speed\tweather_timestamp\ttemperature\tweather_condition\twind_speed\twind_direction\thumidity\tbarometer\tvisibility\ttime_window\n')
        lat_long_list=obtain_latitudes_long_list()
        for lat_long_row in lat_long_list:
            latitude=lat_long_row[0] 
            longitude=lat_long_row[1] 
            time=24 
            #https://api.aerisapi.com/forecasts/50.82448,4.393893?from=1561672800&to=1561755600&filter=1hr&
            api_url='https://api.aerisapi.com/forecasts/'+str(latitude)+','+str(longitude)+'?from='+str(combined_start_time)+'&to='+str(combined_end_time)+'&filter=1hr&client_id=6mzRG6y1n6A6Dy3lQXRPT&client_secret=UP3GNV20hMBGP5CLnzyO8SSt51HpX0qSKeNEuEBx'
            print(api_url)
            data = requests.get(api_url).json()['response'][0]['periods']
            for row in data:
	            file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(device,latitude,longitude,row['timestamp'],row['timestamp'],10,15,row['timestamp'],row['avgTempC'],return_proper_weather_condition(row['weather']),row['windSpeedKPH'],row['windDir'],row['humidity'],row['pressureMB'],0,return_time_slice_column_value(int(row['timestamp']),24)))
	            #print(row)
    create_on_hot_next_dates_file('./data/next_dates_data.tsv','./data/next_dates_data_one_hot_data.tsv')

