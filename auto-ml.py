import tensorflow as tf
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


# region DATA IMPORT AND PROCESSING


def remove_outlier(df_in, col_name):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1  # Interquartile range
    fence_low = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) &
                       (df_in[col_name] < fence_high)]
    return df_out


# PARAMETERS TO USE: latitude, longitude, bike_count, bike_avg_speed, weather_timestamp, temperature, weather_condition, wind_speed
combined_path = "data/combined_data.tsv"

df = pd.read_csv(combined_path,
                 sep='\t',
                 header=0,
                 usecols=[1, 2, 3, 5, 8, 9, 12]
                 )

weather_unique_combinations = df.weather_condition.unique()
true_unique = []
for el in weather_unique_combinations

df_x = remove_outlier(df, "bike_count")

plt.matshow(df_x.corr())
plt.xticks(range(len(df_x.columns)), df_x.columns)
plt.yticks(range(len(df_x.columns)), df_x.columns)
plt.colorbar()
plt.show()

df.set_index('timestamp_from', inplace=True)


# remove rows with empty windspeed
#df_x = df[df.wind_speed.apply(lambda x: x.isnumeric())]


df_x = df.sort_values(by=['timestamp_from'])


# CEK0496  50.82448, 4.393893
#df_x = df_x[df_x.latitude.apply(lambda x: x == 50.82448)]
# remove bike_count outliers


df_y = df_x.bike_count
df_x = df_x.drop(columns="bike_count")


# print(df_x)
# print(df_y)


x = df_x.values
y = df_y.values.reshape(-1, 1)

x_scaler = preprocessing.MinMaxScaler()
x_normalized = x_scaler.fit_transform(x)

y_scaler = preprocessing.MinMaxScaler()
y_normalized = y_scaler.fit_transform(y)


x_in = pd.DataFrame(x_normalized)
y_in = pd.DataFrame(y_normalized)

# print(x_in)
# print(y_in)


test_size = 0.2
total = x_in.shape[0]
train_idx = round((1-test_size) * total)


x_train = x_in[0:train_idx].values
x_train = x_train.reshape(x_train.shape[0], 1, x_train.shape[1])

x_test = x_in[train_idx+1:total-1].values
x_test = x_test.reshape(x_test.shape[0], 1, x_test.shape[1])

y_train = y_in[0:train_idx].values
y_test = y_in[train_idx+1:total-1]


print("x_train shape {}".format(x_train.shape))
print(x_train)
print("y_train shape {}".format(y_train.shape))

# endregion

# region MODEL


def build_model():

    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(21, input_shape=(1, 3), return_sequences=True),
        tf.keras.layers.LSTM(7, activation=tf.nn.relu),
        tf.keras.layers.Dense(1, name="Output"),
    ])

    model.compile(loss='mae',
                  optimizer='adam',
                  metrics=['mean_absolute_error', 'mean_squared_error'])
    return model

# endregion


model = build_model()
model.summary()


model.fit(x_train, y_train, epochs=10)

model.evaluate(x_test, y_test)

# x_test = x_train
# y_test = y_train

y_prediction = model.predict(x_test)
y_pred_scaled = y_scaler.inverse_transform(y_prediction)
y_test_scaled = y_scaler.inverse_transform(y_test)
mse = mean_squared_error(y_pred_scaled, y_test_scaled)
print(mse)


l1, = plt.plot(y_test_scaled, 'g')
l2, = plt.plot(y_pred_scaled, 'r', alpha=0.7)
plt.legend(['Ground truth', 'Predicted'])
plt.show()
