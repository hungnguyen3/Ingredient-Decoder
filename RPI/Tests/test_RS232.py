from unittest import TestCase
import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200)

#test cases for read and write using RS232 serial connection
class RS232(TestCase):
    def RS232read(self):
        received = []
        expected = [1,2,3,4,5,6,7,8,9]
        if ser.isOpen == False:
            ser.open()
        try:
            while True:
                size = ser.inWaiting()
                if size != 0:
                    response = ser.read(1)
                    received.append(response)
                    print(response)
                    if response == b"9":
                        break
        except KeyboardInterrupt:
            ser.close()
        
        # received characters is equal to the expected characters
        assert received == expected

    def RS232write(self):
        # Transmitting signals to DE1-SoC using RS232 serial connection
        # transmit 1 to 10
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

        received = []
        expected = [1,2,3,4,5,6,7,8,9,10]

        # receive the same signals back from DE1
        # receive from 1 to 10
        if ser.isOpen == False:
            ser.open()
        try:
            while True:
                size = ser.inWaiting()
                if size != 0:
                    response = ser.read(1)
                    received.append(response)
                    print(response)
                    if response == b"10":
                        break
        except KeyboardInterrupt:
            ser.close()
        
        # received characters is equal to the expected characters
        assert received == expected