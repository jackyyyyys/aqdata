from tabnanny import verbose
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
np.set_printoptions(precision=3, suppress=True)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#################################################################
sensor = 3
test_row = 33333
#################################################################

sensors = ['98F4AB39DB50', '98F4AB38C884', '4C11AEE82D80']
csv = f"../{sensors[sensor -1]}-processed.csv"
raw_dataset = pd.read_csv(csv)
dataset = raw_dataset.copy()
dataset = dataset.drop('TIME', axis=1)

original_score = dataset.iloc[test_row]['SCORE']
input = dataset.loc[[test_row]]
input = input.drop('SCORE', axis=1)

model = tf.keras.models.load_model(f'dnn_model_sensor_{sensor}')
prediction = model.predict(input, verbose=0)[0][0]

print(input)
print(f'{test_row}: {original_score} | {prediction}')

# Regression using a DNN and multiple inputs