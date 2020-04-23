# 🚲 BRUBIKE

In order to create and evaluate bicycle traffic flow models, bike traffic information from all cities around the world is required. External features such as weather data can be exploited to improve models or develop new models. For that purpose, BRUBIKE aims to make Brussels' historical bike count and weather data more accessible to other researchers.

## Data Description

As time passes, more historical data becomes available and new potential features can be added to the BRUBIKE dataset. The following table will provide an identifier for each of the existing datasets that can be used for the development and evaluation of traffic models. **/data** acts as the root directory for the published datasets.

### Datasets

| Name            | Filename                                                                                                       | Records | Description                                                                                                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BRUBIKE_V1_1819 | [BRUBIKE_V1_1819.tsv](https://raw.githubusercontent.com/vandenbroucke/BRUBIKE/master/data/BRUBIKE_V1_1819.tsv) | 102,310 | Initial version of BRUBIKE, containing historical bike count & weather data of Brussels. The data spans over a period of 193 days from the 6th of December 2018 until the 16th of June 2019. |

The following table provides overlapping descriptions for the features presented in the aforementioned datasets.

### Features

| Feature           | Description                                                                       | Used in         |
| ----------------- | --------------------------------------------------------------------------------- | --------------- |
| device_name       | unique identifier for a bike counting pole                                        | BRUBIKE_V1_1819 |
| latitude          | angular distance north or south of the earth’s equator                            | BRUBIKE_V1_1819 |
| longitude         | angular distance east or west of the Greenwich meridian                           | BRUBIKE_V1_1819 |
| timestamp_from    | start of counting interval in Unix epoch seconds                                  | BRUBIKE_V1_1819 |
| bike_count        | number of bicycles counting during the count-                                     | BRUBIKE_V1_1819 |
| bike_avg_speed    | average speed of all counted bicycles during the counting interval in km per hour | BRUBIKE_V1_1819 |
| weather_timestamp | time of weather measurement in Unix epoch seconds                                 | BRUBIKE_V1_1819 |
| temperature       | temperature in degrees Celcius                                                    | BRUBIKE_V1_1819 |
| weather_condition | type of weather (Sunny, Fog, Partly cloudy ,...)                                  | BRUBIKE_V1_1819 |
| wind_speed        | speed of wind in km per hour                                                      | BRUBIKE_V1_1819 |
| wind_direction    | direction of the wind                                                             | BRUBIKE_V1_1819 |
| humidity          | percentage of water vapour present in the air                                     | BRUBIKE_V1_1819 |
| barometer         | atmospheric pressure indicated in mbar                                            | BRUBIKE_V1_1819 |
| visibility        | distance of visibility indicated in km                                            | BRUBIKE_V1_1819 |



### Citation
Please consider citing our work when using BRUBIKE:
~~~~
@INPROCEEDINGS{9071764, author={S. V. {Broucke} and L. M. V. {Piña} and T. H. {Do} and N. {Deligiannis}}, booktitle={2019 IEEE International Smart Cities Conference (ISC2)}, title={BRUBIKE: A Dataset of Bicycle Traffic and Weather Conditions for Predicting Cycling Flow}, year={2019}, volume={}, number={}, pages={432-437},}

S. V. Broucke, L. M. V. Piña, T. H. Do and N. Deligiannis, "BRUBIKE: A Dataset of Bicycle Traffic and Weather Conditions for Predicting Cycling Flow," 2019 IEEE International Smart Cities Conference (ISC2), Casablanca, Morocco, 2019, pp. 432-437.
~~~~
