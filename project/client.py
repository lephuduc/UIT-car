# Import socket module
import socket
import cv2
import numpy as np
import math
import time
import sys

global sendBack_angle, sendBack_Speed, current_speed, current_angle
sendBack_angle = 0
sendBack_Speed = 0
current_speed = 0
current_angle = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 54321
s.connect(('127.0.0.1', PORT))

def Control( speed,angle):
    global sendBack_angle, sendBack_Speed
    sendBack_angle = angle
    sendBack_Speed = speed

if __name__ == "__main__":
    try:
        while True:
            message_getState = bytes("0", "utf-8")
            s.sendall(message_getState)
            state_date = s.recv(100)

            try:
                current_speed, current_angle = state_date.decode("utf-8").split(' ')
            except Exception as er:
                print(er)
                pass

            message = bytes(f"1 {sendBack_angle} {sendBack_Speed}", "utf-8")
            s.sendall(message)
            data = s.recv(100000)

            try:
                image = cv2.imdecode(np.frombuffer(data,np.uint8), -1)
                print(current_speed, current_angle)
                print(image.shape)
                # your process here
                image=image[200:,:,:]
                gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
                img=cv2.Canny(gray,122,255)
                arr=[]
                lineRow=img[50,:]
                for x,y in enumerate(lineRow):
                    if y==255:
                        arr.append(x)
                arrmax=max(arr)
                arrmin=min(arr)
                center=int((arrmax+arrmin)/2)

                angle=math.degrees(math.atan((center-img.shape[1]/2)/(img.shape[0]-50)))
                print(angle)
                
                cv2.circle(img,(arrmin,50),5,(255,255,255),5)
                cv2.circle(img,(arrmax,50),5,(255,255,255),5)
                cv2.line(img,(center,50),(int(img.shape[1]/2),img.shape[0]),(255,255,255),(5))
                cv2.imshow("IMG",img)
                cv2.imshow("IMG", img)
                cv2.waitKey(1)

                # Control(angle, speed)
                if angle >=-10 and angle <=10:
                    Control(75, 0)
                elif angle >=-70 and angle<=-60:
                    Control(28, 9)
                elif angle <=70 and angle >=60:
                    Control(28, -9)
                elif angle >-60 and angle<-10:
                    Control(10,25)
                elif angle <60 and angle>10:
                    Control(10,-25)

            except Exception as er:
                print(er)
                pass

    finally:
        print('closing socket')
        s.close()
