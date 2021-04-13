from unittest import TestCase
import serial
import time

ser = serial.Serial('/dev/rfcomm0', 115200)

#test cases for read and write using bluetooth serial connection
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
        # Transmitting signals to DE1-SoC using bluetooth serial connection
        # transmit 0 to 50
        if ser.isOpen == False:
            ser.open()
        try:
            for count in range(0,51):
                dist = int(count)
                data = bytes(str(chr(dist)), 'ascii')
                ser.write(data)
        except KeyboardInterrupt:
            ser.close()

        received = []
        expected = []
        for count in range(0,51):
            expected.append(count)

        # receive the same signals back from DE1
        # receive from 0 to 50
        if ser.isOpen == False:
            ser.open()
        try:
            while True:
                size = ser.inWaiting()
                if size != 0:
                    response = ser.read(1)
                    received.append(response)
                    print(response)
                    if response == b"50":
                        break
        except KeyboardInterrupt:
            ser.close()
        
        # received characters is equal to the expected characters
        assert received == expected