from matplotlib.pyplot import axis
import numpy as np
import pandas as pd
import tensorflow as tf

#################################################################
sensor = 3
test_row = 33333
#################################################################
# Regression using DNN with multiple inputs

def quality(sensor, CO2, VOC, RH, TEM, PM25):
    model = tf.keras.models.load_model(f'dnn_model_sensor_{int(sensor)}')
    prediction = model.predict([(CO2, VOC, RH, TEM, PM25)], verbose = 0)[0][0]
    return prediction

def test():
    sensors = ['98F4AB39DB50', '98F4AB38C884', '4C11AEE82D80']
    csv = f"../resources/{sensors[sensor -1]}-processed.csv"
    raw_dataset = pd.read_csv(csv)
    dataset = raw_dataset.copy()
    dataset = dataset.drop('TIME', axis=1)

    original_score = dataset.iloc[test_row]['SCORE']
    input = dataset.loc[[test_row]]
    input = input.drop('SCORE', axis=1)

    model = tf.keras.models.load_model(f'dnn_model_sensor_{sensor}')
    prediction = model.predict(input, verbose = 0)[0][0]

    print(input)
    print(f'{test_row}: {original_score} | {prediction}')

# test()
# /quality/3,417,0,68.6,23.8,518