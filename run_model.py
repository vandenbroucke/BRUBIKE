import matplotlib.pyplot as plt
from datetime import datetime as dt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
import tensorflow as tf
import os;
start=dt.now()
def detect_outlier(data_1):
    outliers=[]
    threshold=3
    indexes=[]
    index=0
    mean_1 = np.mean(data_1)
    std_1 =np.std(data_1)

    
    for y in data_1:
        z_score= (y - mean_1)/std_1 
        if np.abs(z_score) > threshold:
            '''print("this is the value ",y)
            print("index",index)'''
            outliers.append(y)
            indexes.append(index)
        index+=1
    
    
    return indexes
def delete_outliers(data):
	liist_outliers_indexes=detect_outlier(data.bike_count)
	for i in range(0,len(liist_outliers_indexes)):
		data=data.drop(liist_outliers_indexes[len(liist_outliers_indexes)-i-1],axis=0)
		
	
	return data


def return_value_given_theta_vector(theta_vector,list_to_evaluate):
	list_to_evaluate.append(1)
	print(theta_vector,list_to_evaluate)
	theta_v=np.asarray(theta_vector)[np.newaxis]
	list_v=np.asarray(list_to_evaluate)[np.newaxis].T
	return theta_v.dot(list_v)


def convert_input_to_list(string):
	list_input=[]
	list_input[:]=(float(value) for value in string.split(','))
	return list_input
def predict_using_scalars(elements_list,model,x_scalar,y_scalar):
	Xnew = np.array([elements_list])
	
	Xnew= x_scalar.transform(Xnew)
	ynew= model.predict(Xnew)
	#invert normalize
	ynew = y_scalar.inverse_transform(ynew) 	
	
	#print("here reescaling a loss of 0.020, that would be around: ",y_scalar.inverse_transform([[0.020]]))

	return float(ynew[0])

def return_list_of_infer_function(num_features,model, x_scalar,y_scalar):
	list_len=num_features+1
	return_list=[0]*list_len		

	return_list[list_len-1]=predict_using_scalars([0]*(list_len-1),model,x_scalar,y_scalar)	
	for i in range(0,list_len-1):
		temp_list=[0]*(list_len-1)
		temp_list[i]=1
		return_list[i]=predict_using_scalars(temp_list,model,x_scalar,y_scalar)-return_list[list_len-1]		
	return return_list
		
def select_data_from_lat(data, latitude):
	#return_data=np.array();
	
	counter=0
	for row in data:
		if str(row[0])==latitude:
			counter+=1
	return_data=np.empty((counter,6))
	counter=0
	for row in data:
		'''print(row[0])
		print(latitude)
		print(type(str(row[0])))
		print(type(latitude))
		input()'''
		if str(row[0])==latitude:
			return_data[counter]=row
			counter+=1

	return return_data
def select_data_from_lat_csv(data,latitude):
	print(data)
	input()
def clean_data(data):
	return_data=data[data.wind_speed.apply(lambda x: x.isnumeric())]
	print(return_data.shape)
	input()
def generate_tuple_n_from_data(data,n):
	string=str(data.loc[n].latitude)+','+str(data.loc[n].longitude)+','+str(data.loc[n].bike_avg_speed)+','+str(data.loc[n].temperature)+','+str(data.loc[n].wind_speed)+','+str(data.loc[n].humidity)+','+str(data.loc[n].barometer)+','+str(data.loc[n].broken_clouds)+','+str(data.loc[n].chilly)+','+str(data.loc[n].clear)+','+str(data.loc[n].cloudy)+','+str(data.loc[n].cool)+','+str(data.loc[n].drizzle)+','+str(data.loc[n].fog)+','+str(data.loc[n].freezing_rain)+','+str(data.loc[n].hail)+','+str(data.loc[n].haze)+','+str(data.loc[n].ice_fog)+','+str(data.loc[n].light_fog)+','+str(data.loc[n].light_freezing_rain)+','+str(data.loc[n].light_rain)+','+str(data.loc[n].light_snow)+','+str(data.loc[n].low_clouds)+','+str(data.loc[n].partly_cloudy)+','+str(data.loc[n].partly_sunny)+','+str(data.loc[n].passing_clouds)+','+str(data.loc[n].quite_cool)+','+str(data.loc[n].rain)+','+str(data.loc[n].rain_showers)+','+str(data.loc[n].scattered_clouds)+','+str(data.loc[n].scattered_showers)+','+str(data.loc[n].sleet)+','+str(data.loc[n].snow)+','+str(data.loc[n].snow_flurries)+','+str(data.loc[n].snow_showers)+','+str(data.loc[n].sprinkles)+','+str(data.loc[n].sunny)+','+str(data.loc[n].thundershowers)+','+str(data.loc[n].thunderstorms)
	print(string)
def higuest_value_of_y(y):
	higuest_value=y[0]
	iterator=0
	index=0
	for i in y:
		if i>higuest_value:
			higuest_value=i
			index=iterator
		iterator+=1
	return higuest_value,index



path="data/"
os.chdir(path)
os.getcwd()
#Variables
dataset=pd.read_csv("combined_data.tsv", delimiter="\t",header=0)

#dataset=select_data_from_lat_csv(dataset,'50.88185')


x=dataset.drop(columns=["device_name","weather_condition","wind_direction", "visibility","timestamp_from","timestamp_until","weather_timestamp"])
print(x.shape)
#print(x.iloc[44392,:])
x=delete_outliers(x)

print(x.shape)
x=x[x['wind_speed']!='No']


y=x.bike_count
print(higuest_value_of_y(y))
print(generate_tuple_n_from_data(x,2302))

x=x.drop(columns='bike_count')
#dataset=clean_data(dataset)
print("x.shape without outliers, without wind_speed error values",x.shape)

y=y.values.reshape(-1,1)

scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

x_scaler = MinMaxScaler()

x_normalized = x_scaler.fit_transform(x)

y_scaler = MinMaxScaler()

y_normalized = y_scaler.fit_transform(y)

x_in = pd.DataFrame(x_normalized)

y_in = pd.DataFrame(y_normalized)


X_train, X_test, y_train, y_test = train_test_split(x_in, y_in)

def build_model():
	model = Sequential()
	model.add(Dense(39, input_dim=39, kernel_initializer='normal', activation='relu'))
	model.add(Dense(39, activation='relu'))
	model.add(Dense(1, activation='linear'))
	model.compile(loss='mse', optimizer='adam', metrics=['mse','mae'])
	model.summary()
	return model
def build_model2():

	model = Sequential([

	tf.keras.layers.Dense(39,activation=tf.nn.relu,input_shape=(39,)),
	tf.keras.layers.Dense(78,activation=tf.nn.relu),
	tf.keras.layers.Dense(39,activation=tf.nn.relu),
	tf.keras.layers.Dense(1,name="Output"),
	])

	optimizer = tf.keras.optimizers.RMSprop(0.001)

	model.compile(loss='mean_squared_error',
	optimizer=optimizer,
	metrics=['mean_absolute_error','mean_squared_error'])

	return model
model=build_model()

history = model.fit(X_train, y_train, epochs=150, batch_size=50,  verbose=1, validation_split=0.2)


print(history.history.keys())


print("model created on : ",dt.now()-start)
#print(history.history)
# "Loss"
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

#list_theta_values=return_list_of_infer_function(3,model,scaler_x,scaler_y)


generate_tuple_n_from_data(x,0)
generate_tuple_n_from_data(x,10)
generate_tuple_n_from_data(x,100)




'''Xnew = np.array([[50.82448,4.393893,24,11,24,94,1014,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]])
Xnew= x_scaler.transform(Xnew)
ynew= model.predict(Xnew)
#invert normalize
ynew = y_scaler.inverse_transform(ynew) 
Xnew = x_scaler.inverse_transform(Xnew)'''
#print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))
while True:
	print("Set the values to analize")
	string=input()
	
	result=convert_input_to_list(string)
	'''print("line 162")
	Xnew = np.array([result])
	Xnew= x_scaler.transform(Xnew)
	ynew= model.predict(Xnew)
	#invert normalize
	ynew = y_scaler.inverse_transform(ynew) 
	Xnew = x_scaler.inverse_transform(Xnew)
	print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))	'''
	print("predict_using_scalars fuction ", predict_using_scalars(result,model,x_scaler,y_scaler))
	#print("according to the implemented inference the value is: ")
	#print(return_value_given_theta_vector(list_theta_values,result))
print("Saving model...")
print(type(model))
model.save('my_own_model.bin')
print("Finished...")
