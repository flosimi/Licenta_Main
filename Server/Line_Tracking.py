import time
from Motor import *
import RPi.GPIO as GPIO
class Line_Tracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)
    def run(self):
        while True:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            
            if self.LMR==2:
                PWM.setMotorModel(1000,1000,1000,1000)
            elif self.LMR==6:
                PWM.setMotorModel(-1100,-1100,1100,1100)
            elif self.LMR==4:
                PWM.setMotorModel(-1300,-1300,1300,1300)
            elif self.LMR==3:
                PWM.setMotorModel(1100,1100,-1100,-1100)
            elif self.LMR==1:
                PWM.setMotorModel(1300,1300,-1300,-1300)
            elif self.LMR==0:
                PWM.setMotorModel(0,0,0,0)
            elif self.LMR==7:
                PWM.setMotorModel(0,0,0,0)
            
infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        PWM.setMotorModel(0,0,0,0)
        print('Motor model has been set to stop state.')
