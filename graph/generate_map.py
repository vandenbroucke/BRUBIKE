# import libraries
import folium
import csv
import pandas as pd
import statistics as st
from datetime import datetime as dt
start=dt.now()
bike_point_list=[]
longitude_list=[]
latitude_list=[]
print('Generating map...')

count=0
with open('../data/combined_data.tsv') as tsvfile:
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
m = folium.Map(location=[st.mean(longitude_list), st.mean(latitude_list)], tiles="OpenStreetMap", zoom_start=11.5)
 
# I can add marker one by one on the map
for i in range(0,len(data)):
    folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']], popup=data.iloc[i]['name'],icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
 
# Save it as html
m.save('bike_Brussels-points-map.html')

print('bike_Brussels-points-map.html file already generated')
print(dt.now()-start)