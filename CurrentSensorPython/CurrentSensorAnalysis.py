# CurrentSensor Python Code
# by Robert J Scales March 2021
#
# Meant to work with my Arduino code after that code is uploaded to the Arduino board itself, keeping it powered on.

import matplotlib.pyplot as plt
import numpy
import easygui
import pandas as pd  # Ths is used for accessing the CSV file after creation for data analysis.


def moving_average(x_input, w):
    return numpy.convolve(x_input, numpy.ones(w)/w, 'same')


print('Loading csv files...')
Load_filetypes = ["*.csv"]
# Load_filetypes = ["*.css", ["*.htm", "*.html", "HTML files"] ]
files = easygui.fileopenbox(msg='Message', title='Title', default='*', filetypes=Load_filetypes, multiple=False)
print(files)

print('Select mode...')
TF_IV = easygui.buttonbox('Choose analysis mode:', 'Analysis Mode', ['I vs t', 'I vs V'])
print(TF_IV)

headers = ("Time (s):", "Bus Voltage (V):", "Shunt Voltage (mV):", "Load Voltage (V):", "Current (mA):",
           "Power (mW):")

# columns = defaultdict(list)  # each value in each column is appended to a list

print('Main part...')
# with open(files) as f:
#     reader = csv.DictReader(f)  # read rows into a dictionary format
#     for row in reader:  # read a row as {column1: value1, column2: value2,...}
#         for (k, v) in row.items():  # go over each column name and value
#             columns[k].append(float(v))  # append the value into the appropriate list based on column name k
# f.close()


# Using Pandas, the data from the CSV file is read.
data = pd.read_csv(files)

# In all methods cases, the y-axis is current, and we need the time values to calculate the average acquisition rate.
y_values = data['Current (mA):']

try:
    time_values = data['Time (s):']
except Exception as ex:
    print(ex)
    print("File used old header!")
    time_values = data['Time (m:s:mu_s):']

# Below calculates the average mean acquisition frequency.
time_difference = [time_values[i + 1] - time_values[i] for i in range(len(time_values)-1)]
mean_frequency = 1/(sum(time_difference) / len(time_difference))

# The following is just plot aesthetics and changing the x-axis variable.
if TF_IV == 'I vs V':
    x_values = data['Load Voltage (V):']
    plt.xlabel('Load Voltage (V)')
    window = 5
    y_values = list(moving_average(y_values, w=window))
    plt.title(f"Current vs Voltage (window = {window} & f={round(mean_frequency, 2)} Hz)")
else:
    x_values = data['Time (s):']
    plt.xlabel('Time (s)')
    plt.title(f"Current vs Time (f={mean_frequency})")


Number_of_Points = len(x_values)
Colors = list(range(0, Number_of_Points))
plt.scatter(x_values, y_values, c=Colors, s=6, cmap='cool')  # , marker='x', markerfacecolor='red', markersize=12
color_bar = plt.colorbar()
color_bar.set_label('Time of Recording (s)', loc='center')

print("Code Complete!")

plt.show()  # function to show the plot

