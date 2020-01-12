import RPi.GPIO as GPIO
from motors2 import motors2
from motors2 import motor_pins
from time import sleep
from speedSensor import speedSensor
#Motor tanımları buradan çıkartıldı.
class carsWith2Motor2:
    def __init__(self, motorRight: motors2, motorLeft: motors2):
        self.motorRight:motors2 = motorRight
        self.motorLeft:motors2 = motorLeft
        self.direction = 1  # Forward
        self.angle = 0  # -100 - 100 arasında
        self.speed = 0
        self.motorRight.motorSet()
        self.motorLeft.motorSet()
        self.stopped = True
        
    def stop(self):
        self.motorRight.stop()
        self.motorLeft.stop()
        self.direction = 0
        
    def forward(self):
        self.motorRight.forward()
        self.motorLeft.forward()
        self.setSpeed(self.speed)
        self.direction = 1

    def backward(self):
        self.motorRight.backward()
        self.motorLeft.backward()
        self.direction = -1

    def setSpeed(self,speed):
        self.motorRight.setSpeed(speed)        
        self.motorLeft.setSpeed(speed)
    
    def setAngle(self, percentage):
        if percentage > 100:
            percentage = 100
            
        speedRight = self.speed
        speedLeft = self.speed
        
        if percentage != 0:         
            change = self.speed * (percentage/100)
            goingRight = True

            if change < 0:
                change = -change
                goingRight = False
                
            if change + self.speed > 100:
                # bir tarafı 100 yapıp, eksik kalanı fazladan öbür tarafa ekle
                goSide = 100
                #speedLeft = self.speed - change - (change + self.speed - 100)          
                otherSide = 100 - (2*change)
                if otherSide < 0:
                    otherSide = 0
            else:
                goSide = self.speed + change
                otherSide = self.speed - change
            
            if goingRight:
                speedRight = goSide
                speedLeft = otherSide
            else:
                speedLeft = goSide
                speedRight = otherSide
                
        self.motorRight.setSpeed(speedRight)
        self.motorLeft.setSpeed(speedLeft)
        
        self.angle = percentage

def getStandartCar2():
    pinsLeft = motor_pins(17,18,23)
    pinsRight = motor_pins(22,27,24)

    # MOTOR1IN1 = 17
    # MOTOR1IN2 = 18
    # MOTOR1EN = 23
    # MOTOR2IN1 = 22
    # MOTOR2IN2 = 27
    # MOTOR2EN = 24

    # MOTOR1IN1 = 17
    # MOTOR1IN2 = 18
    # MOTOR1EN = 23
    # MOTOR2IN1 = 22
    # MOTOR2IN2 = 27
    # MOTOR2EN = 24
    
    # 24 -> P5 (D7)
    # 25- > p6
    # 4 -> p7
    # 8 -> d10 (c0)
    # 10 -> d11 (mosi)
    # 9 -> d12
    # 11  -> d13

    motorRight = motors2.fromPinDefs(pinsRight)
    motorLeft = motors2.fromPinDefs(pinsLeft)
# Sadece sağ motor için hız sensörü denemede    
    speedSensorRight = speedSensor(25,1,20,5)
    motorRight.setSpeedSensor(speedSensorRight)
    motorRight.spS.turnOnDetector()

    myCar = carsWith2Motor2(motorRight, motorLeft)
    
    return myCar

class carsWith4Motor:
    def __init__(self, motorRight: motors2, motorLeft: motors2, motorRight2: motors2, motorLeft2: motors2):
        self.motorRight:motors2 = motorRight
        self.motorLeft:motors2 = motorLeft
        self.motorRight2:motors2 = motorRight2
        self.motorLeft2:motors2 = motorLeft2

        self.direction = 1  # Forward
        self.angle = 0  # -100 - 100 arasında
        self.speed = 0
        self.motorRight.motorSet()
        self.motorLeft.motorSet()
        self.motorRight2.motorSet()
        self.motorLeft2.motorSet()

        self.stopped = True
        
    def stop(self):
        self.motorRight.stop()
        self.motorLeft.stop()
        self.motorRight2.stop()
        self.motorLeft2.stop()        
        self.direction = 0
        
    def forward(self):
        self.motorRight.forward()
        self.motorLeft.forward()
        self.motorRight2.forward()
        self.motorLeft2.forward()

        self.setSpeed(self.speed)
        self.direction = 1

    def backward(self):
        self.motorRight.backward()
        self.motorLeft.backward()
        self.motorRight2.backward()
        self.motorLeft2.backward()
        
        self.direction = -1

    def setSpeed(self,speed):
        self.motorRight.setSpeed(speed)        
        self.motorLeft.setSpeed(speed)
        self.motorRight2.setSpeed(speed)        
        self.motorLeft2.setSpeed(speed)
        self.speed = speed

    
    def setAngle(self, percentage):
        breakpoint()
        if percentage > 100:
            percentage = 100
            
        speedRight = self.speed
        speedLeft = self.speed
        
        if percentage != 0:         
            change = self.speed * (percentage/100)
            goingRight = True

            if change < 0:
                change = -change
                goingRight = False
                
            if change + self.speed > 100:
                # bir tarafı 100 yapıp, eksik kalanı fazladan öbür tarafa ekle
                goSide = 100
                #speedLeft = self.speed - change - (change + self.speed - 100)          
                otherSide = 100 - (2*change)
                if otherSide < 0:
                    otherSide = 0
            else:
                goSide = self.speed + change
                otherSide = self.speed - change
            
            if goingRight:
                speedRight = goSide
                speedLeft = otherSide
            else:
                speedLeft = goSide
                speedRight = otherSide
                
        self.motorRight.setSpeed(speedRight)
        self.motorLeft.setSpeed(speedLeft)
        self.motorRight2.setSpeed(speedRight)
        self.motorLeft2.setSpeed(speedLeft)

        
        self.angle = percentage

def getStandart4WheelCar2():
    pinsLeft = motor_pins(17,18,23)
    pinsRight = motor_pins(22,27,24)

    pinsLeft2 = motor_pins(25,4,8)
    pinsRight2 = motor_pins(10,9,11)

    # MOTOR1IN1 = 17
    # MOTOR1IN2 = 18
    # MOTOR1EN = 23
    # MOTOR2IN1 = 22
    # MOTOR2IN2 = 27
    # MOTOR2EN = 24

    # MOTOR1IN1 = 17
    # MOTOR1IN2 = 18
    # MOTOR1EN = 23
    # MOTOR2IN1 = 22
    # MOTOR2IN2 = 27
    # MOTOR2EN = 24
    
    # 24 -> P5 (D7)
    # 25- > p6
    # 4 -> p7
    # 8 -> d10 (c0)
    # 10 -> d11 (mosi)
    # 9 -> d12
    # 11  -> d13

    motorRight = motors2.fromPinDefs(pinsRight)
    motorLeft = motors2.fromPinDefs(pinsLeft)
    motorRight2 = motors2.fromPinDefs(pinsRight2)
    motorLeft2 = motors2.fromPinDefs(pinsLeft2)

# Sadece sağ motor için hız sensörü denemede    
    speedSensorRight = speedSensor(25,1,20,5)
    motorRight.setSpeedSensor(speedSensorRight)
    motorRight.spS.turnOnDetector()

    myCar = carsWith4Motor(motorRight, motorLeft, motorRight2, motorLeft2)
    
    return myCar

def carTest():
    testCar = getStandartCar()
    testCar.forward()
    testCar.setSpeed(40)
    sleep(2)
    myCar.backward()
    sleep(1)
    testCar.forward()
    testCar.setAngle(30)
    sleep(2)
    testCar.setAngle(-30)
    sleep(2)
    myCar.stop()
    
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    runCar()
    GPIO.cleanup()

