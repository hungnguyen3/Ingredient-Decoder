import numpy as np
import os
import RPi.GPIO as GPIO
import time
import serial

ser = serial.Serial('/dev/ttyAMA0', 115200)
if ser.isOpen == False:
    ser.open()

path = os.path.dirname(os.path.abspath(__file__))
imgPath = os.path.dirname(path) + "/images"

def bluetoothLogin():
    username = []
    while(1):
        size = ser.inWaiting()
        if size != 0:
            response = ser.read(1)
            username.append(response)
            #print(response)
            if response == b"1" or response == b"2":
                #print("yes, it is 1 end or 2 end")
                break
                #print("really break")
    #print("here")
    str1 = ""
    for element in username:
        str1 += element
    return str1

def run(customerIdQueue, loginSuccessQueue):
    while(1):
        loginSuccessQueue.put(True)
        customerIdQueue.put("customer2")
        time.sleep(15)
        loginSuccessQueue.put(True)
        customerIdQueue.put("customer1")
        time.sleep(15)


#run(customerId, loginSuccess)
#bluetoothLogin()
#cap.release()