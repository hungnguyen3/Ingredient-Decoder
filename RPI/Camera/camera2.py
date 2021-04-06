import numpy as np
import os
import RPi.GPIO as GPIO
import time
import serial
import multiprocessing as mp

# RS232 serial connection
ser = serial.Serial('/dev/ttyAMA0', 115200)
if ser.isOpen == False:
    ser.open()

# path of the current working directory
path = os.path.dirname(os.path.abspath(__file__))
imgPath = os.path.dirname(path) + "/images"

# this function receives the customer Id from the DE1-SoC board
def bluetoothLogin():
    username = []
    while(1):
        size = ser.inWaiting()
        if size != 0:
            response = ser.read(1)
            username.append(response)
            print(response)
            if response == b"1" or response == b"2":
                break

    str1 = ""
    for element in username:
        str1 += element.decode("utf-8")
    return str1

# this function updates the customer signin functionality of the touchscreen app
# this is a process running along side with the touchscreen app
def run(customerIdQueue, loginSuccessQueue):
    while(1):
        str1 = bluetoothLogin()
        loginSuccessQueue.put(True)
        customerIdQueue.put(str1)