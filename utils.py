import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
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