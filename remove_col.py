import pandas as pd

TO_DELETE = ["sensor_id", 'db_id', 'ALM']
SENSOR = 3

sensors = ['98F4AB39DB50', '98F4AB38C884', '4C11AEE82D80']

data = pd.read_csv(f'./{sensors[SENSOR - 1]}.csv')
print(f'Deleting from sensor {sensors[SENSOR - 1]}: {TO_DELETE} ...')
for item in TO_DELETE:
    data.drop(item, inplace=True, axis=1)

data.to_csv(f'{sensors[SENSOR - 1]}_light.csv', index = False)