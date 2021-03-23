# CurrentSensor Python Code
# by Robert J Scales March 2021
#
# Meant to work with my Arduino code after that code is uploaded to the Arduino board itself, keeping it powered on.

import serial
import datetime
import matplotlib.pyplot as plt

codeStartTime = datetime.datetime.now()

# Editable Inputs
fileName = "analog-data" + codeStartTime.strftime("_%y-%H-%M-%S") + ".csv"  # Name of the CSV file generated. I added
# the date time to avoid it overwriting the file of a same name.
arduino_port = "COM3"  # Serial port of the Arduino in your PC
baud = 9600  # Arduino uno runs at 9600 baud
RecordingDuration = 0.5  # In minutes.

endTime = datetime.datetime.now() + datetime.timedelta(minutes=RecordingDuration)
print('Started CurrentSensorV3 @ ' + codeStartTime.strftime("%H:%M:%S") + '\n' + 'Made by Robert J Scales - March 2021')

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "w")
print("Created file\n")

headers = "Time (m:s:mu_s):,Bus Voltage (V):,Shunt Voltage (mV):,Load Voltage (V):,Current (mA):,Power (mW):"
file.write(headers + "\n")  # Write data with a newline
print(headers)

ArrayTime = []
ArrayCurrent = []
line = 0  # Start at 0 because our header is 0 (not real data)
while datetime.datetime.now() <= endTime:  # Alternative while line <= samples:
    getData = str(ser.readline())
    CurrentTime = datetime.datetime.now()
    if line == 0:
        StartTime = CurrentTime
    ElapsedTime = CurrentTime-StartTime
    data = getData[0:][:-2]
    final_data = data.replace("b'", '')
    final_data = final_data.replace('\\r\\', '')

    NumOfCommas = final_data.count(',')
    if NumOfCommas == 4:
        # line2print = CurrentTime.strftime("%M:%S:%f") + ',' + final_data
        line2print = str(ElapsedTime.total_seconds()) + ',' + final_data
        file.write(line2print + "\n")  # Write data with a newline
        print(line2print)
        line = line+1
        ArrayTime.append(ElapsedTime.total_seconds())
        SplitFinalData = final_data.split(',')
        ArrayCurrent.append(float(SplitFinalData[3]))

file.close()
print("\n Data collection complete!")

print(ArrayTime)
print(ArrayCurrent)

# plotting the points
plt.plot(ArrayTime, ArrayCurrent)

# naming the x axis
plt.xlabel('Time (s)')
# naming the y axis
plt.ylabel('Current (mA)')

# giving a title to my graph
plt.title(fileName)

# function to show the plot
plt.show()

