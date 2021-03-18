import cv2
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

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

cap = cv2.VideoCapture(0)

cap.set(3,1920)
cap.set(4,1080)

ret, frame = cap.read()
rows, cols, channels = frame.shape
print(cols, rows, channels)

def takeImage():
    ret,frame = cap.read()
    dst = frame
    filename = imgPath + '/output.jpg'
    cv2.imwrite(filename, dst)
    print("image generated")

def distance():
    # send a trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

def waitForItem():
    while(1):
        time.sleep(1)
        dist = int(distance())
        if dist > 128:
            dist = 127
        data = bytes(str(chr(dist)), 'ascii')
        print("data is" + str(data))
        ser.write(data)
        if dist < 20:
            print(dist)
            time.sleep(5)
            takeImage()
        else:
            print(dist)

waitForItem()
cap.release()
cv2.destroyAllWindows()