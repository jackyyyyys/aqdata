from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sensors = ['98F4AB39DB50', '98F4AB38C884', '4C11AEE82D80']
params = ['CO2', 'VOC', 'RH', 'TEM', 'PM25']

# Make a data frame
s1 = pd.read_csv(f'./{sensors[0]}.csv')

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
z = s1["PM25"]
x = s1["TEM"]
y = s1["RH"]
ax.scatter3D(x, y, z, c=z, cmap='Greens')
ax.show()

# plt.scatter(s1["CO2"], s1["PM25"])
# plt.show()