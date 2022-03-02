from datetime import datetime
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling 
PARAM = "PM25"

sensors = ['98F4AB39DB50', '98F4AB38C884', '4C11AEE82D80']
params = ['CO2', 'VOC', 'RH', 'TEM', 'PM25']

# Make a data frame
s1 = pd.read_csv(f'./{sensors[0]}_light.csv')
s2 = pd.read_csv(f'./{sensors[1]}_light.csv')
s3 = pd.read_csv(f'./{sensors[2]}_light.csv')

sns.boxplot(s1['PM25'])

# zs = stats.zscore(s1)
# abs_z_scores = np.abs(zs)
# filtered_entries = (abs_z_scores < 3).all()
# new_s1 = s1[filtered_entries]
# print(new_s1.describe())

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

print('start diff end diff')
diff_2_1_start = abs(round((s1_start - s2_start)))
diff_2_1_end = abs(round((s1_end - s2_end)))
print('1 vs 2', diff_2_1_start, diff_2_1_end)
diff_3_2_start = abs(round((s2_start - s3_start)))
diff_3_2_end = abs(round((s2_end - s3_end)))
print('2 vs 3', diff_3_2_start, diff_3_2_end)
diff_3_1_start = abs(round((s1_start - s3_start)))
diff_3_1_end = abs(round((s1_end - s3_end)))
print('1 vs 3', diff_3_1_start, diff_3_1_end)

# 3 sensors, same param
df = pd.DataFrame({
    "x": range(1, ss_min),
    sensors[0]: s1[s1.index < ss_min-1][PARAM],
    sensors[1]: s2[s2.index < ss_min-1][PARAM],
    # sensors[2]: s3[s3.index < ss_min-1][PARAM],
})

# same sensor, 3 values
# df = pd.DataFrame({
#     "x": range(1, ss_min),
#     "PM25": s1[s1 < s1[ss_min]]['PM25'],
#     "TEM": s1[s1 < s1[ss_min]]['TEM'],
#     "RH": s1[s1 < s1[ss_min]]['RH'],
# })

# Change the style of plot
plt.style.use('seaborn-darkgrid')
 
# Create a color palette
palette = plt.get_cmap('Set1')

# Plot multiple lines
num = 0
for column in df.drop('x', axis=1):
    num+=1
    plt.plot(df['x'], df[column], marker='', color = palette(num), linewidth = 1, alpha = 0.9, label = column)


# Add legend
plt.legend(loc = 2, ncol = 2)
 
# Add titles
plt.title("PM2.5 Comparison Among Sensors", loc = 'center', fontsize = 20, fontweight = 0, color = 'black')
plt.xlabel("Time")
plt.ylabel("PM2.5 Index")

# Show the graph
plt.show()