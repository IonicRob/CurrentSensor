# CurrentSensor Python Code
# by Robert J Scales March 2021
#
# This is the most optimised code to run in terms of acquisition rate, as it stores the data from the com port into a
# CSV and then it analyses and reads off that CSV file after acquiring the data. On my personal laptop this gave
# frequencies close to that which the Arduino is set to ouput, e.g. Arduino around 10 Hz max and this recorded at
# around 9.5 Hz. This is considerably faster than the Live Plot Python code which was around 3 Hz.
#
# One does not need to specify an exact duration time, as the CSV is appended constantly in each loop,
# so cancelling the code should stop recording. However, a graph will not automatically be produced at the end, and the
# CurrentSensorAnalysis code will be needed to plot the results.
#
# CurrentSensorAnalysis is recommended to make prettier graphs for reports, as it has been designed to do this.
#
# This is meant to work with my Arduino code after that code is uploaded to the Arduino board itself, keeping it
# powered on.

import serial  # Communicates with the com port to which the Arduino current logger is plugged in.
import datetime as dt  # This deals with time in the code.
import matplotlib.pyplot as plt  # This is what I use to plot the results
import easygui  # This how I achieve a GUI for the "I vs t" or "I vs V" plotting.
import pandas as pd  # Ths is used for accessing the CSV file after creation for data analysis.

# User Settings
session_name = "Log Current Main Test"  # This is the ID for your recording session. Extra details are auto added.
arduino_port = "COM4"  # Serial port of the Arduino in your PC
baud = 115200  # Arduino uno runs at 9600 or 115200 baud
RecordingDuration = 0.5  # In minutes the length for which the code will record data for.

# GUI interface for selecting final mode to plot. Useful to have here so that it's added into the file name of the csv.
print('Select mode...')
TF_IV = easygui.buttonbox('Choose analysis mode:', 'Analysis Mode', ['I vs t', 'I vs V'])
print(TF_IV)

# This is the name of the CSV file which will be automatically created and saved.
fileName = session_name + "_" + TF_IV + "_" + dt.datetime.now().strftime("_%H-%M-%S") + ".csv"

# This section initialises the CSV file with the correct headers.
print('Creating csv file ...')
with open(fileName, 'w') as csv_file_1:
    headers = "Time (s):,Bus Voltage (V):,Shunt Voltage (mV):,Load Voltage (V):,Current (mA):,Power (mW):"
    csv_file_1.write(headers + "\n")  # Write data with a newline
    print(headers)

# This connects the code with the com port stated earlier.
ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)

# This defines when the code "starts" recording, and from this defines a time at which the while loop below will end at.
codeStartTime = dt.datetime.now()
endTime = dt.datetime.now() + dt.timedelta(minutes=RecordingDuration)

line = 0  # Start at 0 because our header is 0 (not real data)
while dt.datetime.now() <= endTime:
    getData = str(ser.readline())  # This accesses the serial port information which the Arduino is outputting.
    elapsed_time = (dt.datetime.now()-codeStartTime).total_seconds()  # Records acquisition time.
    # The below lines just convert the Arduino "csv" output into an actual "csv" style output.
    data = getData[0:][:-2]
    final_data = data.replace("b'", '')
    final_data = final_data.replace('\\r\\', '')

    # This "if" statement is done because the code can read the serial port mid-line, and this creates issues logging
    # data, and so this condition waits until a whole line has been printed and then records it.
    if final_data.count(',') == 4:
        with open(fileName, 'a') as csv_file:
            # The below line just adds the elapsed time into the csv file along with the Arduino data.
            line2print = str(elapsed_time) + ',' + final_data
            csv_file.write(line2print + "\n")  # Write data with a newline in the CSV file.
            print(line2print)

print("\n Data collection complete!")

# Initialises the important variables for plotting
x_values = []
y_values = []
time_values = []

# Using Pandas, the data from the CSV file is read.
data = pd.read_csv(fileName)

# The following is just plot aesthetics and changing the x-axis variable.
if TF_IV == 'I vs V':
    x_values = data['Load Voltage (V):']
    plt.xlabel('Load Voltage (V)')
else:
    x_values = data['Time (s):']
    plt.xlabel('Time (s)')

# In all methods cases, the y-axis is current, and we need the time values to calculate the average acquisition rate.
y_values = data['Current (mA):']
time_values = data['Time (s):']

# Below calculates the average mean acquisition frequency.
time_difference = [time_values[i + 1] - time_values[i] for i in range(len(time_values)-1)]
mean_frequency = 1/(sum(time_difference) / len(time_difference))

# This plots the data
plt.scatter(x_values, y_values)

# Labels the y-axis
plt.ylabel('Current (mA)')

# Giving a title to the graph that includes the acquisition frequency
plt.title(f"Mean Acquisition Rate = {round(mean_frequency, 2)} Hz")

print("Code Completed")

# function to show the plot
plt.show()
