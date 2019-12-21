import RPi.GPIO as GPIO
from speedSensor import speedSensor

class motor_pins:
        def __init__(self, in1, in2, en):
                self.in1 = in1
                self.in2 = in2
                self.en = en
                
class motor_speeds:
    # Motorların hız tanımları için kaç kademe vs. PWM için
    def __init__(self, lowLimitToRun, numberOfGears, turningGearDif):
        self.lowLimitToRun = lowLimitToRun
        self.numberOfGears = numberOfGears
        self.turningGearDif = turningGearDif
        self.gearSteps = (100 - lowLimitToRun) / (self.numberOfGears - 1)

    def gearSpeed(self, gear):
        if gear > self.numberOfGears:
                return 100
        elif gear == self.numberOfGears:
            return 100
        elif gear < 1:
            return self.lowLimitToRun
        else:
            return self.lowLimitToRun + ((gear - 1) * self.gearSteps)


class motors:    
    def __init__(self, in1, in2, en, speedDef: motor_speeds):
        self.in1 = in1
        self.in2 = in2
        self.en = en      

        self.temp = 1
        self.speedDef:speedDef = speedDef
        self.currentGear = 1
        self.direction = 1
        self.stopped = True
        
    @classmethod
    def fromPinDefs (self, pins:motor_pins, speedDef:motor_speeds):
        return self(pins.in1,pins.in2,pins.en,speedDef)

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
        self.currentGear = 1
        self.direction = 1
        self.changeGear(self.currentGear)
        self.stopped = True        

    def motorSet(self):
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        self.p = GPIO.PWM(self.en, 1000)
        self.p.start(self.speedDef.gearSpeed(self.currentGear))

    def changeGear(self, gear):
        if self.stopped:
            return
        if gear > self.speedDef.gearSteps:
            self.currentGear = self.speedDef.gearSteps
        elif gear < 1:
            self.currentGear = 1
        else:
            self.currentGear = gear
        self.p.ChangeDutyCycle(self.speedDef.gearSpeed(self.currentGear))
    
    def gearUp(self,up):
            self.changeGear(self.currentGear+up)
            
    def gearDown(self,down):
            self.changeGear(self.currentGear-down)
            
    def isMaxGear(self):
            return not(self.currentGear < self.speedDef.gearSteps)
            
    def isMinGear(self):
            return (self.currentGear == 1)
            
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
