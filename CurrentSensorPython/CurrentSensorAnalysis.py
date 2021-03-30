# CurrentSensor Python Code
# by Robert J Scales March 2021
#
# Meant to work with my Arduino code after that code is uploaded to the Arduino board itself, keeping it powered on.

import matplotlib.pyplot as plt
import easygui
import csv
from collections import defaultdict

Load_filetypes = ["*.csv"]
# Load_filetypes = ["*.css", ["*.htm", "*.html", "HTML files"] ]
files = easygui.fileopenbox(msg='Message', title='Title', default='*', filetypes=Load_filetypes, multiple=False)
print(files)

TF_IV = easygui.buttonbox('Choose analysis mode:', 'Analysis Mode', ['I vs t', 'I vs V'])
print(TF_IV)

headers = ("Time (m:s:mu_s):", "Bus Voltage (V):", "Shunt Voltage (mV):", "Load Voltage (V):", "Current (mA):",
           "Power (mW):")

columns = defaultdict(list)  # each value in each column is appended to a list

with open(files) as f:
    reader = csv.DictReader(f)  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(float(v))  # append the value into the appropriate list based on column name k
f.close()

if TF_IV is None:
    print(f'Value of TF_IV = {TF_IV}')
else:
    if TF_IV == 'I vs t':
        x: list = columns["Time (m:s:mu_s):"]
        y: list = columns["Current (mA):"]
        x_label = 'Time (s)'
        y_label = 'Current (mA)'
        title = "Current vs Time"
    else:
        x: list = columns["Load Voltage (V):"]
        y: list = columns["Current (mA):"]
        x_label = 'Load Voltage (V):'
        y_label = 'Current (mA)'
        title = "Current vs Time"
    plt.plot(x, y, 'x', color='black', markersize=6)  # , marker='x', markerfacecolor='red', markersize=12
    plt.xlabel(x_label)  # naming the x axis
    plt.ylabel(y_label)  # naming the y axis
    plt.title(title)  # giving a title to my graph
    plt.show()  # function to show the plot

