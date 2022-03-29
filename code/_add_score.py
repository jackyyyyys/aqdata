import json
from collections import Counter
import pandas as pd
import seaborn as sns; sns.set()  # for plot styling 

SENSOR_ID =     1
CO2_SCORES =    [ 1 , 2 , 3 ]
VOC_SCORES =    [ 1 , 3 , 5 ] # sensor value is directly used atm
PM25_SCORES =   [ 1 , 3 , 5 ]

sensors = ['98F4AB39DB50', '98F4AB38C884', '4C11AEE82D80']
params = ['CO2', 'VOC', 'RH', 'TEM', 'PM25']
standards = json.load(open('../standards.json'))
sensor = pd.read_csv(f'../resources/{sensors[SENSOR_ID-1]}.csv')
light = pd.read_csv(f'../resources/{sensors[SENSOR_ID-1]}_light.csv')

def score_co2(co2):
    if (co2 >= standards['CO2'][0]['from'] & co2 <= standards['CO2'][0]['to']):
        return CO2_SCORES[0]
    elif (co2 >= standards['CO2'][1]['from'] & co2 <= standards['CO2'][1]['to']):
        return CO2_SCORES[1]
    elif (co2 >= standards['CO2'][2]['from'] & co2 <= standards['CO2'][2]['to']):
        return CO2_SCORES[2]
        
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
        return PM25_SCORES[0]
    elif (pm25 >= standards['PM25'][1]['from'] & pm25 <= standards['PM25'][1]['to']):
        return PM25_SCORES[1]
    elif (pm25 >= standards['PM25'][2]['from'] & pm25 <= standards['PM25'][2]['to']):
        return PM25_SCORES[2]

def score_total(co2, voc, pm25):
    # not specific enough
    grade = score_co2(co2) + score_voc(voc) + score_pm25(pm25)
    return grade

grades = []
for i in range(1, len(sensor)):
    grade = score_total(sensor.loc[i]['CO2'], sensor.loc[i]['VOC'], sensor.loc[i]['PM25'])
    grades.append(grade)
    print(' ', i, " / ", len(sensor), end='\r')
# print(grades, end=" ")

print(sensors[SENSOR_ID-1])
# df = pd.DataFrame(grades)
# print(df.describe())
print("CO2: ", CO2_SCORES)
print("VOC: ", VOC_SCORES)
print("PM2.5: ", PM25_SCORES)
print (Counter(grades))

# append score to end
# with ASSIGN
# ValueError: Length of values (68251) does not match length of index (68252)
light['SCORE'] = grades
light.to_csv(f'{sensors[SENSOR_ID-1]}-processed.csv')