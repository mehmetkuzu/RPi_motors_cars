import RPi.GPIO as GPIO
#Buradan deneme
#Bir de rpiden
#Bir de pcden
class motor_speeds:
    # Motorların hız tanımları için kaç kademe vs. PWM için
    def __init__(self, lowLimitToRun, numberOfGears, turningGearDif):
        self.lowLimitToRun = lowLimitToRun
        self.numberOfGears = numberOfGears
        self.turningGearDif = turningGearDif
        self.gearSteps = (100 - lowLimitToRun) / (self.numberOfGears - 1)

    def gearSpeed(self, gear):
        if gear > self.numberOfGears:
            # exception handling eklenecek şimdilik en üst vitese al
            pass
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
        self.speedDef = speedDef
        self.currentGear = 1
        self.direction = 1
        self.stopped = True

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
        self.stopped = True
        self.currentGear = 1

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

        self.p.changeDutyCycle(self.speedDef.gearSpeed(self.currentGear))
