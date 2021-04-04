import numpy as np
import os
import RPi.GPIO as GPIO
import time
import serial
import multiprocessing as mp

ser = serial.Serial('/dev/ttyAMA0', 115200)
#ser = serial.Serial('/dev/rfcomm0', 115200)
if ser.isOpen == False:
    ser.open()

path = os.path.dirname(os.path.abspath(__file__))
imgPath = os.path.dirname(path) + "/images"

#customerIdQueue = mp.Queue()
#loginSuccessQueue = mp.Queue()

def bluetoothLogin():
    username = []
    while(1):
        size = ser.inWaiting()
        if size != 0:
            response = ser.read(1)
            username.append(response)
            print(response)
            if response == b"1" or response == b"2":
                #print("yes, it is 1 end or 2 end")
                break
                #print("really break")
    #print("here")
    str1 = ""
    for element in username:
        str1 += element.decode("utf-8")
    return str1

def run(customerIdQueue, loginSuccessQueue):
    while(1):
        str1 = bluetoothLogin()
        loginSuccessQueue.put(True)
        customerIdQueue.put(str1)


#run(customerIdQueue, loginSuccessQueue)
#bluetoothLogin()
#cap.release()