import cv2
import numpy as np
name = 0
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

ret, frame = cap.read()
rows, cols, channels = frame.shape
print(cols, rows, channels)
while(1):
        ret,frame = cap.read()
        dst = frame
        cv2.imshow('usb camera', dst)

        k = cv2.waitKey(50)
        if (k == ord('q')):
            break
        elif(k == ord('s')):
                #name = input('name:')
                name += 1
                filename = '/home/pi/camera' + str(name) + '.jpg'
                cv2.imwrite(filename, dst)
                print(filename)
                #break
cap.release()
cv2.destroyAllWindows()