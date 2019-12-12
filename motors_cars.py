import RPi.GPIO as GPIO
from motors import motors
from motors import motor_speeds
from motors import motor_pins
from time import sleep
#Motor tanımları buradan çıkartıldı.
class carsWith2Motor:
    def __init__(self, motorRight: motors, motorLeft: motors):
        self.motorRight:motors = motorRight
        self.motorLeft:motors = motorLeft
        self.direction = 1  # Forward
        self.angle = 0  # -1 sola bir vites fazla +sağa bir vites fazla
        self.gear = 1
        self.motorRight.motorSet()
        self.motorLeft.motorSet()
        self.stopped = True
        
    def turnRight(self, stepMore):
        if self.motorLeft.currentGear < self.motorLeft.speedDef.numberOfGears:
            self.motorLeft.changeGear(self.motorLeft.currentGear + stepMore)
        

    def turnLeft(self, stepMore):
        if self.motorRight.currentGear < self.motorRight.speedDef.numberOfGears:
            self.motorRight.changeGear(self.motorRight.currentGear + stepMore)

    def stop(self):
        self.motorRight.stop()
        self.motorLeft.stop()
        pass
        
    def changeGear(self,gear):
        self.motorRight.changeGear(gear)
        self.motorLeft.changeGear(gear)
        self.gear = gear
        

    def forward(self):
        self.changeGear(self.gear)
        self.motorRight.forward()
        self.motorLeft.forward()

    def backward(self):
        self.changeGear(self.gear)
        self.motorRight.backward()
        self.motorLeft.backward()

def getStandartCar():
    pinsLeft = motor_pins(23,24,25)
    pinsRight = motor_pins(22,27,26)

    GPIO.setmode(GPIO.BCM)

    theSpeeds = motor_speeds(50,4,1)
    motorRight = motors.fromPinDefs(pinsRight, theSpeeds)
    motorLeft = motors.fromPinDefs(pinsLeft, theSpeeds)

    myCar = carsWith2Motor(motorRight, motorLeft)
    
    return myCar

def carTest():
    pinsLeft = motor_pins(23,24,25)
    pinsRight = motor_pins(22,27,26)
    # MOTOR1IN2 = 24
    # MOTOR1IN1 = 23
    # MOTOR1EN = 25
    # MOTOR2IN2 = 27
    # MOTOR2IN1 = 22
    # MOTOR2EN = 26

    GPIO.setmode(GPIO.BCM)

    theSpeeds = motor_speeds(50,4,1)
    motorRight = motors.fromPinDefs(pinsRight, theSpeeds)
    motorLeft = motors.fromPinDefs(pinsLeft, theSpeeds)

    myCar = carsWith2Motor(motorRight, motorLeft)
    myCar.forward()
    myCar.changeGear(2)
    sleep(2)
    myCar.turnRight(1)
    sleep(2)
    myCar.backward()
    sleep(1)
    myCar.stop()

    #GPIO.cleanup()
        
    #carTest()
