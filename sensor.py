from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sensors = ['98F4AB39DB50', '98F4AB38C884', '4C11AEE82D80']
params = ['CO2', 'VOC', 'RH', 'TEM', 'PM25']

day = 1574
eg_day = [9926, 11580]

# Make a data frame
s1 = pd.read_csv(f'./{sensors[0]}.csv')
s2 = pd.read_csv(f'./{sensors[1]}.csv')
s3 = pd.read_csv(f'./{sensors[2]}.csv')
print("s1", s1.describe())
print("s2", s2.describe())
print("s3", s3.describe())

ss_min = min(len(s1), len(s2), len(s3))
ss_max = max(len(s1), len(s2), len(s3))

# compare timestamps...
s1_start, s1_end, s1_last = (s1.iloc[0]['TIME'], s1.iloc[ss_min]['TIME'], s1.iloc[-1]['TIME'])
s2_start, s2_end, s2_last = (s2.iloc[0]['TIME'], s1.iloc[ss_min]['TIME'], s2.iloc[-1]['TIME'])
s3_start, s3_end, s3_last = (s3.iloc[0]['TIME'], s1.iloc[ss_min]['TIME'], s3.iloc[-1]['TIME'])

print("length: ", ss_min)
print("start\t\t\t\tend\t\tupdates\t\tinterval (sec)")
print(s1_start, datetime.fromtimestamp(s1_start),'\t', s1_end, datetime.fromtimestamp(s1_end), '\t', len(s1), '\t', (s1_end - s1_start)/ss_min)
print(s2_start, datetime.fromtimestamp(s2_start),'\t', s2_end, datetime.fromtimestamp(s2_end), '\t', len(s2), '\t', (s2_end - s2_start)/ss_min)
print(s3_start, datetime.fromtimestamp(s3_start),'\t', s3_end, datetime.fromtimestamp(s3_end), '\t', len(s3), '\t', (s3_end - s3_start)/ss_min)

d = s1.loc[9926]
t = datetime.fromtimestamp(d['TIME'])
print(d, t)
d2 = s1.loc[11580]
t2 = datetime.fromtimestamp(d2['TIME'])
print(d2, t2)