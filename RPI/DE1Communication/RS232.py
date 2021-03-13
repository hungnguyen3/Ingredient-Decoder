import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200)
if ser.isOpen == False:
    ser.open()

ser.write(b"1")
count = b"0"
odd = 1
try:
    while True:
        if odd%2 == 1:
            ser.write(b"1")
            odd = odd + 1
        else:
            ser.write(b"2")
            odd = odd + 1
        #count = count + count
        #print(response)
        #ser.flushOutput()
        #ser.write(b"9")
        #ser.flushInput()
except KeyboardInterrupt:
    ser.close()