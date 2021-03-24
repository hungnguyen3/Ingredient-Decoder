import cv2
import numpy as np
import os
import RPi.GPIO as GPIO
import time
import serial
from crop import cropImage

ser = serial.Serial('/dev/ttyAMA0', 115200)
if ser.isOpen == False:
    ser.open()

blueSer = serial.Serial('/dev/rfcomm0', 115200)
if blueSer.isOpen == False:
    blueSer.open()

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

ret, frame = cap.read()
rows, cols, channels = frame.shape

def takeImage(factor, imageName):
    cap.set(3,160*factor)
    cap.set(4,90*factor)
    ret,frame = cap.read()
    dst = frame
    filename = imgPath + imageName
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
        time.sleep(0.5)
        dist = int(distance())
        if dist >= 128:
            dist = 127
        data = bytes(str(chr(dist)), 'ascii')
        print("data is" + str(data))
        ser.write(data)
        if dist < 15:
            print(dist)
            #time.sleep(5)
            takeImage(1, '/small.jpg')
            takeImage(9, '/big.jpg')
            # send signal to stop
            ser.write(bytes(str(chr(0)), 'ascii'))
            ser.write(bytes(str(chr(0)), 'ascii'))
            ser.write(bytes(str(chr(0)), 'ascii'))
            ser.write(bytes(str(chr(0)), 'ascii'))
            ser.write(bytes(str(chr(0)), 'ascii'))
            ser.write(bytes(str(chr(0)), 'ascii'))
            break
        else:
            print(dist)

def bluetoothLogin():
    username = []
    while(1):
        size = ser.inWaiting()
        if size != 0:
            response = ser.read(1)
            username.append(response)
            print(response)

def sendImageToDe1():
    img = cv2.imread(imgPath + "/small.jpg")
    rows,cols,rgb = img.shape
    count = 0
    for i in range(rows-1, -1, -1):
        for j in range(cols):
            for k in range(rgb):
                #time.sleep(0.00001)
                value = int(img[i,j,k]/2)
                ser.write(bytes(str(chr(value)), 'ascii'))
                count = count + 1
                #print(value)
    print(img)
    print(count)

while(1):
    # generate picture
    waitForItem()
    time.sleep(0.5)

    # send image to DE1
    sendImageToDe1()

    #receive boundingBox
    boxCounter = 0
    box = []
    while(1):
        size = blueSer.inWaiting()
        if size != 0:
            print("here")
            response = blueSer.read(1)
            box.append(response)
            boxCounter = boxCounter + 1
            print(response)
            blueSer.write(bytes(str(chr(0)), 'ascii'))
            if boxCounter == 4:
                break

    print(box)
    # crop image
    xMin = int.from_bytes(box[3], "big")
    xMax = int.from_bytes(box[2], "big")
    yMin = int.from_bytes(box[1], "big")
    yMax = int.from_bytes(box[0], "big")
    print(xMin)
    print(xMax)
    print(yMin)
    print(yMax)
    cropImage('/small.jpg', xMin, xMax, yMin, yMax)
    # hacky fix
    if yMin > 10:
        yMin = yMin - 10
    if xMin > 10:
        xMin = xMin - 10
    cropImage('/big.jpg', xMin*9, xMax*9, yMin*9, yMax*9)

cap.release()
cv2.destroyAllWindows()