import keyboard  # using module keyboard
import RPi.GPIO as GPIO
from time import sleep


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


class carsWith2Motor:
    def __init__(self, motorRight: motors, motorLeft: motors):
        self.motorRight = motorRight
        self.motorLeft = motorLeft
        self.direction = 1  # Forward
        self.angle = 0  # -1 sola bir vites fazla +sağa bir vites fazla
        self.gear = 1
        self.stopped = True

    def turnRight(self, stepMore):
        pass

    def turnLeft(self, stepMore):
        pass

    def stop(self):
        pass

    def forward(self):
        pass

    def backward(self):
        pass


def carTest():
    RIGHTIN1 = 24
    RIGHTIN2 = 23
    RIGHTEN = 25
    LEFTIN1 = 27
    LEFTIN2 = 22
    LEFTEN = 26

    motorRight = motor(RIGHTIN1, RIGHTIN2, RIGHTEN)
    motorLeft = motor(LEFTIN1, LEFTIN2, LEFTEN)

    GPIO.setmode(GPIO.BCM)
    motorRight.motorSet()
    motorLeft.motorSet()
    print("\n")
    print("The default speed & direction of motor is LOW & Forward.....")
    print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
    print("\n")
    while (1):
        x = raw_input()

        if x == 'rr':
            print("run")
            if (motorRight.temp == 1):
                motorRight.forward()
            else:
                motorRight.backward()
            x = 'z'
        elif x == 'sr':
            motorRight.stop()
            x = 'z'

        elif x == 'fr':
            motorRight.forward()
            motorRight.temp = 1
            x = 'z'

        elif x == 'br':
            motorRight.backward()
            motorRight.temp = 0
            x = 'z'

        elif x == 'lr':
            print("low")
            motorRight.p.ChangeDutyCycle(25)
            x = 'z'

        elif x == 'mr':
            print("medium")
            motorRight.p.ChangeDutyCycle(50)
            x = 'z'

        elif x == 'hr':
            print("high")
            motorRight.p.ChangeDutyCycle(75)
            x = 'z'

        elif x == 'rl':
            print("run")
            if (motorLeft.temp == 1):
                motorLeft.forward()
            else:
                motorLeft.backward()
            x = 'z'
        elif x == 'sl':
            motorLeft.stop()
            x = 'z'

        elif x == 'fl':
            motorLeft.forward()
            motorLeft.temp = 1
            x = 'z'

        elif x == 'bl':
            motorLeft.backward()
            motorLeft.temp = 0
            x = 'z'

        elif x == 'll':
            print("low")
            motorLeft.p.ChangeDutyCycle(25)
            x = 'z'

        elif x == 'ml':
            print("medium")
            motorLeft.p.ChangeDutyCycle(50)
            x = 'z'

        elif x == 'hl':
            print("high")
            motorLeft.p.ChangeDutyCycle(75)
            x = 'z'
        elif x == 'f':
            motorLeft.forward()
            motorLeft.temp = 1
            motorRight.forward()
            motorRight.temp = 1
            x = 'z'
        elif x == 'b':
            motorLeft.backward()
            motorLeft.temp = 0
            motorRight.backward()
            motorRight.temp = 0
            x = 'z'
        elif x == 's':
            motorLeft.stop()
            motorRight.stop()
            x = 'z'
        elif x == 'e':
            GPIO.cleanup()
            break

        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")


def keyTest():
    while True:
        try:
            myKey = keyboard.read_key()
        except:
            myKey = "0"

        if myKey == "0":
            pass

        print("You pressed ", myKey)
        if myKey == "e":
            break

        del myKey


def keyTest2():
    while True:
        if keyboard.is_pressed("e"):
            print("bastın")
            break
        else:
            # print("nono")
            pass
