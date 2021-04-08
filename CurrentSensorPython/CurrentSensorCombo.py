from threading import Thread
import csv
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial  # Communicates with the com port to which the Arduino current logger is plugged in.
import datetime as dt  # This deals with time in the code.
import matplotlib.pyplot as plt  # This is what I use to plot the results
import easygui  # This how I achieve a GUI for the "I vs t" or "I vs V" plotting.
import pandas as pd  # Ths is used for accessing the CSV file after creation for data analysis.
import serial.tools.list_ports as tool_port
from warnings import warn


def connect_2_arduino(serial_number=None, baud=115200):
    # Inspired from https://stackoverflow.com/a/40531041
    # ports = list(tool_port.comports())  # serial.tools.list_ports.comports() .grep('Arduino')
    if serial_number is None:
        arduino_ports = list(tool_port.grep('Arduino'))
        if not arduino_ports:
            print_list_of_ports()
            raise IOError("No Arduino found")
        if len(arduino_ports) > 1:
            print_list_of_ports()
            warn('Multiple Arduinos found - using the first')
        arduino_port = arduino_ports[0]
        out_ser = serial.Serial(arduino_port, baud)
        print("Connected to Arduino port:" + arduino_port)
        return out_ser
    else:
        for p_info in serial.tools.list_ports.comports():
            if p_info.serial_number == serial_number:
                out_ser = serial.Serial(p_info.device, baud)
                print("Connected to Arduino port:" + p_info.device)
                return out_ser
        print_list_of_ports()
        raise IOError("Could not find an arduino - is it plugged in?")


def print_list_of_ports():
    port_list = list(tool_port.comports())
    print("\nList of current ports:")
    print("------------------------------")
    for p in port_list:
        print(p)  # p.description
    print("------------------------------")


def func_generate():
    print(f"Adding to CSV file names {fileName}")
    while True:
        get_data = str(ser.readline())  # This accesses the serial port information which the Arduino is outputting.
        elapsed_time = (dt.datetime.now() - codeStartTime).total_seconds()  # Records acquisition time.
        data = get_data[0:][:-2]
        final_data = data.replace("b'", '')
        final_data = final_data.replace('\\r\\', '')

        if final_data.count(',') == 4:
            with open(fileName, 'a') as csv_file:
                # The below line just adds the elapsed time into the csv file along with the Arduino data.
                line2print = str(elapsed_time) + ',' + final_data
                csv_file.write(line2print + "\n")  # Write data with a newline in the CSV file.
                print(line2print)


def func_live_plot():
    def animate(i):
        data = pd.read_csv(fileName)
        values_time = data['Time (s):']
        values_current = data['Current (mA):']
        values_voltage = data['Load Voltage (V):']

        plt.cla()

        if TF_IV == 'I vs V':
            plt.plot(values_voltage, values_current, label='Current')
        else:
            plt.plot(values_time, values_current, label='Current')

        plt.legend(loc='upper left')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.tight_layout()
    plt.show()


# User Settings
session_name = "Log Current Combo"  # This is the ID for your recording session. Extra details are auto added.

ser = connect_2_arduino(serial_number=None, baud=115200)

# GUI interface for selecting final mode to plot. Useful to have here so that it's added into the file name of the csv.
print('Select mode...')
TF_IV = easygui.buttonbox('Choose analysis mode:', 'Analysis Mode', ['I vs t', 'I vs V'])
print(TF_IV)

# This is the name of the CSV file which will be automatically created and saved.
fileName = session_name + "_" + TF_IV + "_" + dt.datetime.now().strftime("%H-%M-%S") + ".csv"

# This section initialises the CSV file with the correct headers.
print('Creating csv file ...')
with open(fileName, 'w') as csv_file_1:
    headers = "Time (s):,Bus Voltage (V):,Shunt Voltage (mV):,Load Voltage (V):,Current (mA):,Power (mW):"
    csv_file_1.write(headers + "\n")  # Write data with a newline
    print(headers)

# This defines when the code "starts" recording, and from this defines a time at which the while loop below will end at.
codeStartTime = dt.datetime.now()


t1 = Thread(target=func_generate)
t2 = Thread(target=func_live_plot)

t1.start()
t2.start()
