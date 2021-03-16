import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200)

if ser.isOpen == False:
    ser.open()
try:
    while True:
        size = ser.inWaiting()
        if size != 0:
            print("here")
            response = ser.read(1)
            print(response)
            #ser.flushOutput()
            #ser.write(b"9")
            #time.sleep(0.1)
            #ser.flushInput()
except KeyboardInterrupt:
    ser.close()