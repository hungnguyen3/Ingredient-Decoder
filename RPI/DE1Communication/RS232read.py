import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200)

# Reading signals from DE1-SoC using RS232 serial connection
if ser.isOpen == False:
    ser.open()
try:
    while True:
        size = ser.inWaiting()
        if size != 0:
            print("here")
            response = ser.read(1)
            print(response)
except KeyboardInterrupt:
    ser.close()