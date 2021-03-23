# CurrentSensor Python Code
# by Robert J Scales March 2021
#
# Meant to work with my Arduino code after that code is uploaded to the Arduino board itself, keeping it powered on.

import serial
import datetime

x = datetime.datetime.now()
print(x)


arduino_port = "COM3"  # Serial port of Arduino
baud = 9600  # Arduino uno runs at 9600 baud
fileName = "analog-data.csv"  # Name of the CSV file generated

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "w")
print("Created file")

# # Display the data to the terminal
# getData = str(ser.readline())
# data = getData[0:][:-2]
# print(data)
#
# # Add the data to the file
# f = open(fileName, "a")  # Append the data to the file
# f.write(data + "\\n")  # Write data with a newline
#
# # Close out the file
# file.close()

samples = 10  # How many samples to collect
print_labels = False
line = 0  # Start at 0 because our header is 0 (not real data)
while line <= samples:
    # incoming = ser.read(9999)
    # if len(incoming) > 0:
    if print_labels:
        if line == 0:
            print("Printing Column Headers")
        else:
            print("Line " + str(line) + ": writing...")
    getData = str(ser.readline())
    data = getData[0:][:-2]
    final_data = data.replace("b'", '')
    final_data = final_data.replace('\\r\\', '')
    print(final_data)

    file = open(fileName, "a")
    file.write(final_data + "\n")  # Write data with a newline
    line = line+1

print("Data collection complete!")
file.close()

y = datetime.datetime.now()

time_delta = (y - x)
total_seconds = time_delta.total_seconds()
print(total_seconds)
