import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200)

# Transmitting signals to DE1-SoC using RS232 serial connection
if ser.isOpen == False:
    ser.open()
try:
    while True:
        ser.write(b"1")
        time.sleep(1)
        ser.write(b"2")
        time.sleep(1)
        ser.write(b"3")
        time.sleep(1)
        ser.write(b"4")
        time.sleep(1)
        ser.write(b"5")
        time.sleep(1)
        ser.write(b"6")
        time.sleep(1)
        ser.write(b"7")
        time.sleep(1)
        ser.write(b"8")
        time.sleep(1)
        ser.write(b"9")
        time.sleep(1)
        ser.write(b"10")
        time.sleep(1)
except KeyboardInterrupt:
    ser.close()