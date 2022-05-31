# aqdata
## Machine Learning Estimation Service for Indoor Air Quality Index
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
Hence
