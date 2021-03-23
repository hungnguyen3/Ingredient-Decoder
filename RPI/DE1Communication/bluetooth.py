import serial
import time

ser = serial.Serial('/dev/rfcomm0', 115200)
if ser.isOpen == False:
    ser.open()

while(1):
    for count in range(0,51):
        #time.sleep(0.02)
        dist = int(count)
        data = bytes(str(chr(dist)), 'ascii')
        #print("data is" + str(data))
        ser.write(data)

while(1):
    size = ser.inWaiting()
    if size != 0:
        print("here")
        response = ser.read(1)
        print(response)