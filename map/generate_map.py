# import libraries
import folium
import csv
import pandas as pd
import statistics as st
from datetime import datetime as dt
import numpy as np
from folium import plugins
def defining_heat_map_list():
	number_of_points=1
	latitude=50.82448
	longitude=4.393893
	return (
    np.random.normal(size=(number_of_points, 3)) *
    np.array([[1, 1, 1]]) +
    np.array([[latitude, longitude, 1]])
    ).tolist()
def GENERATE_MAP_MAIN_FUNCTION(path='./data/combined_data.tsv'):
	start=dt.now()
	bike_point_list=[]
	longitude_list=[]
	latitude_list=[]
	print('Generating map...')

	count=0
	with open(path) as tsvfile:
	  reader = csv.reader(tsvfile, delimiter='\t')
	  for row in reader:
	    if count !=0:
	      if not row[0] in bike_point_list:
	        bike_point_list.append(row[0])
	        longitude_list.append(float(row[1]))
	        latitude_list.append(float(row[2]))
	    count+=1
	        
	# Make a data frame with dots to show on the map
	data = pd.DataFrame({
	'lat':latitude_list,
	'lon':longitude_list,
	'name':bike_point_list
	})


	# Make an empty map
	m = folium.Map(location=[st.mean(longitude_list), st.mean(latitude_list)], tiles="OpenStreetMap", zoom_start=11.5,control_scale=True)
	plugins.Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',
    force_separate_button=True
	).add_to(m)
	#Including some plugins to map
	#plugins.HeatMap(defining_heat_map_list()).add_to(m)
	plugins.LocateControl().add_to(m)

	# I can add marker one by one on the map
	for i in range(0,len(data)):
	    folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']], popup=data.iloc[i]['name'],icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
	 
	# Save it as html
	m.save('./map/bike_Brussels-points-map.html')

	print('The bike_Brussels-points-map.html file was already generated')
	print(dt.now()-start)
def GENERATE_HEAT_MAP(data, predicted_num_bikes):
    import folium
    import random
    
    import statistics as st
    from folium.plugins import HeatMap   
    data_information=[]
    latitudes_list=[]
    longitudes_list=[]
    rand_limits=0.0001
    for row in data.latitude:
        latitudes_list.append(row+random.uniform(-rand_limits,rand_limits))
    for row in data.longitude:
        longitudes_list.append(row+random.uniform(-rand_limits,rand_limits))
  
    for i in range(0,len(latitudes_list)):
        data_information.append([latitudes_list[i],longitudes_list[i],float(predicted_num_bikes[i])])


    m = folium.Map([st.mean(latitudes_list), st.mean(longitudes_list)], tiles='OpenStreetMap', zoom_start=11.5)

    HeatMap(data_information,max_opacity=0.4).add_to(m)

    m.save('./map/forecasting_ap.html')