import pandas as pd
from datetime import datetime as dt

def check_if_the_csv_file_already_has_the_columns(csv_file_path):
	df = pd.read_csv(csv_file_path,delimiter="\t")
	try:
		total_rows=len(df.sunny)
		return True
	except Exception as e:
		return False
def check_if_the_csv_file_already_has_the_FE_columns(csv_file_path):
	df = pd.read_csv(csv_file_path,delimiter="\t")
	try:
		total_rows=len(df.clouds_FE)
		return True
	except Exception as e:
		return False	
def convert_to_proper_header_name(string):
	return string.replace(' ','_').lower()
def exist_weather_condition(string, weather_condition):
	if string in weather_condition:
		return 1
	return 0
def add_row_to_csv_file(csv_file_path,column_name):
	df = pd.read_csv(csv_file_path,delimiter="\t")
	total_rows=len(df.weather_condition)
	weather_conditions_binary_list=[]
	for i in range(0,total_rows):
		weather_conditions_binary_list.append(exist_weather_condition(column_name,df.weather_condition[i]))
	
	df[convert_to_proper_header_name(column_name)] = weather_conditions_binary_list
	df.to_csv(csv_file_path,sep='\t',index=False)
	
def return_list_labels_given_string(string):
	return string.split('. ')
def remove_dots_from_list(weather_labels_list):
	return_list=[]
	for row in weather_labels_list:
		return_list.append(row.replace('.',''))
	return return_list

def define_amount_different_labels(data):
	labels_list=[]
	print("Looking for labels...")
	for row in data:
		for label in return_list_labels_given_string(row):
			if label not in labels_list:
				labels_list.append(label)
				print(label)	
	labels_list.sort()
	labels_list=remove_dots_from_list(labels_list)
	
	print("We found: "+str(len(labels_list))+" different labels.")
	return labels_list
def return_related_column_list_features_engineering(column_name):		
	if column_name=="bad_FE":
		return ['ice_fog','freezing_rain','hail','rain','rain_showers','snow_showers','thundershowers','thunderstorms','snow_showers','sleet','snow_flurries','snow_showers']
	

	
def match_weather_conditions_features_eng(df,related_columns_list,row):	
	for column_name in related_columns_list:
		try:
			if df[column_name][row]==1:
				return 1
		except Exception as e:
			pass
		
	return 0


def add_new_feature_engineering_column(path,column_name):
	print("creating column: "+str(column_name)+'...')
	df = pd.read_csv('combined_data.tsv',delimiter="\t")
	total_rows=len(df.weather_condition)
	new_column_binary_list=[]
	related_columns_list=return_related_column_list_features_engineering(column_name)
	for row in range(0,total_rows):
		new_column_binary_list.append(match_weather_conditions_features_eng(df,related_columns_list,row))
	print("adding binary list to "+str(column_name)+" column...")	
	df_new_file = pd.read_csv(path,delimiter="\t")
	df_new_file[column_name]=new_column_binary_list
	df_new_file.to_csv(path,sep='\t',index=False)

def weather_conditions_features_engineering(path):
	print("weather_conditions_features_engineering, reading .tsv file...")
	dataset=pd.read_csv('combined_data.tsv', delimiter="\t",header=0)
	new_labels_list=['bad_FE']
	for label in new_labels_list:
		add_new_feature_engineering_column(path,label)
def return_time_slice_column_value(timestamp,time_slice_day):
	date=dt.fromtimestamp(timestamp)
	seconds_day=(date - date.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
	#print(date)
	#print(seconds_day)
	window_time=86400/time_slice_day
	#print(int(seconds_day/window_time))

	return int(seconds_day/window_time)

def add_row_time_series_column_to_csv_file(csv_file_path,column_name,time_slice_day):

	df = pd.read_csv(csv_file_path,delimiter="\t")
	total_rows=len(df.timestamp_from)
	time_list=[]
	for i in range(0,total_rows):
		time_list.append(return_time_slice_column_value(df.timestamp_from[i],time_slice_day))
	
	df[column_name] = time_list
	df.to_csv(csv_file_path,sep='\t',index=False)
def return_time_slice_day_of_week_column_value(timestamp,time_slice_day):
	date=dt.fromtimestamp(timestamp)
	
	return date.weekday()
def add_row_day_of_week_time_series_column_to_csv_file(csv_file_path,column_name,time_slice_day):
	

	df = pd.read_csv(csv_file_path,delimiter="\t")
	total_rows=len(df.timestamp_from)
	time_list=[]
	for i in range(0,total_rows):
		time_list.append(return_time_slice_day_of_week_column_value(df.timestamp_from[i],time_slice_day))
	
	df[column_name] = time_list
	df.to_csv(csv_file_path,sep='\t',index=False)
def WEATHER_CONDITIONS_FEATURES_ENG():

	start=dt.now()
	csv_file_path="combined_data.tsv"
	if not check_if_the_csv_file_already_has_the_columns(csv_file_path):	
		dataset=pd.read_csv(csv_file_path, delimiter="\t",header=0)

		#dataset=select_data_from_lat_csv(dataset,'50.88185')
		weather_conditions_row=dataset.weather_condition
		labels_list=define_amount_different_labels(weather_conditions_row)

		print("Creating new columns...")
		for i in range(0,len(labels_list)):
			add_row_to_csv_file("combined_data.tsv",labels_list[i])
			print(convert_to_proper_header_name(labels_list[i])+" column created...")
		print("New columns process finished in ",dt.now()-start)
	else:
		print("The file already has the weather columns")
	if not check_if_the_csv_file_already_has_the_FE_columns(csv_file_path):
		print("Creating features engineering columns...")
		weather_conditions_features_engineering('../selection_techniques/combined_data.tsv')
	else:
		print("The file already has the features engineering columns")
def TIME_SERIES_FEATURES_ENGINEERING(csv_file_path="combined_data.tsv"):
	time_slice_day=24	
	print(csv_file_path)
	add_row_time_series_column_to_csv_file(csv_file_path,"time_window",time_slice_day)
	add_row_day_of_week_time_series_column_to_csv_file(csv_file_path,"time_day_of_week_window",time_slice_day)

#WEATHER_CONDITIONS_FEATURES_ENG()
#TIME_SERIES_FEATURES_ENGINEERING()
