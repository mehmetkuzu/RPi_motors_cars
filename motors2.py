import RPi.GPIO as GPIO
from speedSensor import speedSensor

class motor_pins:
        def __init__(self, in1, in2, en):
                self.in1 = in1
                self.in2 = in2
                self.en = en
                
class motors2:    
    def __init__(self, in1, in2, en):
        self.in1 = in1
        self.in2 = in2
        self.en = en      

        self.temp = 1
        self.direction = 1
        self.stopped = True

        self.speed = 0
        
    @classmethod
    def fromPinDefs (self, pins:motor_pins):
        return self(pins.in1,pins.in2,pins.en,)

    def forward(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        self.direction = 1
        self.stopped = False

    def backward(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        self.direction = 0
        self.stopped = False

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        self.direction = 1
        self.speed = 0
        self.stopped = True        

    def motorSet(self):
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        self.p = GPIO.PWM(self.en, 1000)
        self.p.start(self.speed)

    def setSpeed(self,speed):
        self.p.ChangeDutyCycle(speed)
        self.speed = speed
    
    def setSpeedSensor(self,spS):
        self.spS = spS
                
    def startSpeedSensor(self):
        if self.spS:
                self.spS.turnOnDetector()
    def getSensorSpeed(self):
        if self.spS:
                self.spS.calculate_speed()
    def getSensorSpeedInWindow(self):
        if self.spS:
                self.spS.calculate_speed_inwindow()
