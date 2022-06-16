# aqdata
Prepared by Jacky Sin, HKU IMSE, 15 June 2022
## Machine Learning Estimation Service for Indoor Air Quality Index
---
source = 'https://www.emqx.com/en/blog/how-to-use-mqtt-in-python'

---
this is a python based machine learning (ML) service for estimating indoor air quality (IAQ) with the following parameters provided by IoT sensors:
- CO2 - Carbon Dioxide in ppm
- VOC - Volatile Organic Compounds in μg/m³
- RH - Relative Humidity in %
- TEM - Temperature in 'C
- PM25 - PM2.5 particles in μg/m³

An integer score shall be returned upon request after calculation on a scale of **1 to 13**, with a larger number indicating a less desirable condition of IAQ.

There are 3 major sections, or modules in this system, namely:
1. IAQ historial data retrival and preparation
2. ML with Deep Neural Network and modelling
3. Estimation request and network interfaces

---
### 1 Data Retrieval and Preparation
Data shall be extracted from database into csv, like below:
```
"id","dateCreated","topic","payload"
61,2021-12-03 15:37:09.000,hku/sensor/98F4AB38C884/data,{"CO2":562,"VOC":0,"RH":29,"TEM":27.9,"PM25":6,"ALM":0,"TIME":1638517028}
81,2021-12-03 15:37:17.000,hku/sensor/4C11AEE82D80/data,{"CO2":485,"VOC":0,"RH":30.5,"TEM":24.2,"PM25":535,"ALM":0,"TIME":1638517035}
183,2021-12-03 15:49:13.000,hku/sensor/98F4AB38C884/data,{"CO2":537,"VOC":0,"RH":28.9,"TEM":27.9,"PM25":6,"ALM":0,"TIME":1638517752}
... 
```
Operation shall be done to obtain the following format to begin with
```
db_id,sensor_id,CO2,VOC,RH,TEM,PM25,ALM,TIME
61,98F4AB38C884,562,0,29,27.9,6,0,1638517028
81,4C11AEE82D80,485,0,30.5,24.2,535,0,1638517035
183,98F4AB38C884,537,0,28.9,27.9,6,0,1638517752
...
```
Hence, use `_remove_col.py` to get rid of rows `["sensor_id", 'db_id', 'ALM']`, retainning the essential rows CO2,VOC,RH,TEM,PM25,TIME in  `{sensor}_light.csv`.

Next, use `_add_score.py` to add  custom scoring to each row of data with reference to `score_standards.json`, which is cited from several onnlie sources. Currently, the score matrix is as follow:
```
CO2_SCORES =    [ 1 , 2 , 3 ]
VOC_SCORES =    [ 1 , 2 , 3 ] # sensor value is directly used atm
PM25_SCORES =   [ 1 , 3 , 5 ]
```
WIth the cuurent conditio of sesors, VOC sensor are onnly returning discrete values [1, 2, 3], therefore it's origial value is used.

The current DNN model is trained with the above settinng and distributio of **score** of different sensors are as follow:
1. Sensor 1 [98F4AB39DB50] : {2: 67084, 3: 868, 5: 155, 4: 145})
2. Sensor 2 [98F4AB38C884] : {2: 61890, 3: 1889, 4: 589, 5: 391}
3. SENSOR 3 [4C11AEE82D80] : {2: 65406, 3: 3198, 4: 767, 5: 505}

This operation shall be doe one by oe for each sensor, changing the `SENSOR_ID` variable

Score is appended to each row of data and `{sensor}-processed.csv` is produced and ready for trainning

---
### 2 ML with Deep Neural Network and modelling
Use `train.ipynb` to perform ML and generate DNN model

Operation is done one by onne for each sensor, by changinng `sensor` parameter to be [1, 2, 3], upon completion of running the entire script, a tf model will be generated under name `dnn_model_sensor_{sensor}`.

---
### 3 Estimation request and network interfaces
`run.py` runs a mqtt service subscribing, getting an estimation of IAQ, hence replying (publishing) to mq. Details are as follow:
- Subscribe: `hku/sensor/{sensor_id}/data` for 3 sensors
- Publish: `hku/sensor/{sensor_id}/rank`
- MQ Message Spec: can be found in `mq_spec.json`