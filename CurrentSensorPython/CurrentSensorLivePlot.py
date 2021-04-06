# CurrentSensor Python Code Live
# by Robert J Scales April 2021
#
# This is the Live Plotting version of CurrentSensorMain. The live plotting causes the acquisition rate to be slower
# than seen for CurrentSensorMain (e.g. 3 Hz compared to 9.5 Hz). However, it does have the benefit of plotting the
# data live so that the user can see visually what has been done. It also has the other added benefit in that the user
# chooses when to finish the code rather than giving a predefined time.
#
# CurrentSensorAnalysis is recommended to make prettier graphs for reports, as it has been designed to do this.
#
# This is meant to work with my Arduino code after that code is uploaded to the Arduino board itself, keeping it
# powered on.

import serial
import matplotlib.pyplot as plt
import easygui

import datetime as dt
import matplotlib.animation as animation


print('Started: Current Sensor Live Plot')
# User Settings
session_name = "Log Current LivePlot Test"
arduino_port = "COM4"  # Serial port of the Arduino in your PC
baud = 115200  # Arduino uno runs at 9600 baud, or can set it to 115200
frequency = 50  # Time in milliseconds until it refreshes the graph (+ read com port) i.e. 100 = 10Hz.
SaveCSV = True  # Having this ON will save the data as a CSV as the code operates, but it will slow it down slightly.
SavePlotImage = False  # Having this ON will save the live plot as a png image the code operates, but it will
ShowFrequency = True
# significantly slow down the code.


print('Select mode...')
TF_IV = easygui.buttonbox('Choose analysis mode:', 'Analysis Mode', ['I vs t', 'I vs V'])
print(TF_IV)


fileName = session_name + "_" + TF_IV + "_" + dt.datetime.now().strftime("_%H-%M-%S") + ".csv"


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
array_elapsed_time = []


# This function is called periodically from FuncAnimation
def animate(i, xs, ys, array_elapsed_time, codeStartTime, ser, fileName, TF_IV, SaveCSV, SavePlotImage, ShowFrequency):

    get_data = str(ser.readline())
    elapsed_time = (dt.datetime.now()-codeStartTime).total_seconds()
    array_elapsed_time.append(elapsed_time)
    data = get_data[0:][:-2]
    final_data = data.replace("b'", '')
    final_data = final_data.replace('\\r\\', '')

    ax.clear()

    n_o_c = final_data.count(',')
    if n_o_c == 4:

        split_final_data = final_data.split(',')
        if TF_IV == 'I vs V':
            xs.append(float(split_final_data[2]))
            plt.ylabel('Current (mA)')
            plt.xlabel('Voltage (V)')
        else:
            xs = array_elapsed_time
            plt.ylabel('Current (mA)')
            plt.xlabel('Elapsed Time (s)')

        ys.append(float(split_final_data[3]))

        ax.scatter(xs, ys)

        length_time = len(array_elapsed_time)

        if length_time >= 2+5 and ShowFrequency:
            time_difference = [array_elapsed_time[i + 1] - array_elapsed_time[i] for i in range(length_time-1-5, length_time-1)]
            mean_frequency = 1 / (sum(time_difference) / len(time_difference))
            plt.title(f"Recent Avg. Acquisition Rate = {round(mean_frequency, 2)} Hz")
            # print(f"Mean Acquisition Rate = {round(mean_frequency, 2)} Hz")

        if SaveCSV:
            with open(fileName, 'a') as csv_file:
                line2print = str(elapsed_time) + ',' + final_data
                csv_file.write(line2print + "\n")  # Write data with a newline
                # print(line2print)
        if SavePlotImage:
            plt.savefig(fileName[:-4] + ".png")


print('Creating csv file ...')
with open(fileName, 'w') as csv_file_1:
    headers = "Time (s):,Bus Voltage (V):,Shunt Voltage (mV):,Load Voltage (V):,Current (mA):,Power (mW):"
    csv_file_1.write(headers + "\n")  # Write data with a newline


codeStartTime = dt.datetime.now()


ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)


# Set up plot to call animate() function periodically
print("Running plotting code...")
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, array_elapsed_time, codeStartTime, ser, fileName, TF_IV, SaveCSV, SavePlotImage, ShowFrequency), interval=frequency)
plt.show()
