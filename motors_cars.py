import RPi.GPIO as GPIO
import motors
from time import sleep
#Motor tanımları buradan çıkartıldı.
class carsWith2Motor:
    def __init__(self, motorRight: motors, motorLeft: motors):
        self.motorRight = motorRight
        self.motorLeft = motorLeft
        self.direction = 1  # Forward
        self.angle = 0  # -1 sola bir vites fazla +sağa bir vites fazla
        self.gear = 1
        self.motorRight.motorSet()
        self.motorLeft.motorSet()
        self.stopped = True
		
    def turnRight(self, stepMore):
        pass

    def turnLeft(self, stepMore):
        pass

    def stop(self):
        pass
    def changeGear():
        

    def forward(self):
        motorRight.forward()
        motorLeft.forward()

    def backward(self):
        motorRight.backward()
        motorLeft.backward()


def carTest():
    RIGHTIN1 = 24
    RIGHTIN2 = 23
    RIGHTEN = 25
    LEFTIN1 = 27
    LEFTIN2 = 22
    LEFTEN = 26

    GPIO.setmode(GPIO.BCM)

    theSpeeds = motor_speeds(30,6,1)
    motorRight = motor(RIGHTIN1, RIGHTIN2, RIGHTEN, theSpeeds)
    motorLeft = motor(LEFTIN1, LEFTIN2, LEFTEN, theSpeeds)
    
    myCar = carsWith2Motor(motorRight, motorLeft)
    
    myCar.forward()
    time.sleep(1)
    myCar.backward()
    time.sleep(1)
    
carTest()
