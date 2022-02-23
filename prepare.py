from datetime import datetime
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling 

SENSOR_ID = 3

sensors = ['98F4AB39DB50', '98F4AB38C884', '4C11AEE82D80']
params = ['CO2', 'VOC', 'RH', 'TEM', 'PM25']
standards = json.load(open('standards.json'))
sensor = pd.read_csv(f'./{sensors[SENSOR_ID-1]}.csv')

def score_co2(co2):
    if (co2 >= standards['CO2'][0]['from'] & co2 <= standards['CO2'][0]['to']):
        return 1
    elif (co2 >= standards['CO2'][1]['from'] & co2 <= standards['CO2'][1]['to']):
        return 2
    elif (co2 >= standards['CO2'][2]['from'] & co2 <= standards['CO2'][2]['to']):
        return 3

def score_voc(voc):
    # if (voc >= standards['VOC'][0]['from'] & voc <= standards['VOC'][0]['to']):
    #     return 1
    # elif (voc >= standards['VOC'][1]['from'] & voc <= standards['VOC'][1]['to']):
    #     return 2
    # elif (voc >= standards['VOC'][2]['from'] & voc <= standards['VOC'][2]['to']):
    #     return 3
    return voc

def score_pm25(pm25):
    if (pm25 >= standards['PM25'][0]['from'] & pm25 <= standards['PM25'][0]['to']):
        return 1
    elif (pm25 >= standards['PM25'][1]['from'] & pm25 <= standards['PM25'][1]['to']):
        return 2
    elif (pm25 >= standards['PM25'][2]['from'] & pm25 <= standards['PM25'][2]['to']):
        return 3

def score_total(co2, voc, pm25):
    grade = score_co2(co2) + score_voc(voc) + score_pm25(pm25)
    return grade

grades = []
for i in range(len(sensor)):
    grade = score_total(sensor.loc[i]['CO2'], sensor.loc[i]['VOC'], sensor.loc[i]['PM25'])
    grades.append(grade)
    print(' ', i, " / ", len(sensor), end='\r')
# print(grades, end=" ")

print(sensors[SENSOR_ID-1])
df = pd.DataFrame(grades)
print(df.describe())