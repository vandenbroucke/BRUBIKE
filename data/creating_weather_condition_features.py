import pandas as pd
from datetime import datetime as dt
start=dt.now()
def check_if_the_csv_file_already_has_the_columns(csv_file_path):
	df = pd.read_csv(csv_file_path,delimiter="\t")
	try:
		total_rows=len(df.sunny)
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
