import Jetson.GPIO as GPIO
import time
import os
#import conpig
import test

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#----------pin setting----------
pin1 = 19 #pin35
pin2 = 16 #pin36
buzzer_pin = 13
btn_pin = 20 #pin38

GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

scale = [262, 294, 330, 349, 392, 440, 494, 523] 
pwm = GPIO.PWM(buzzer_pin, 262) 
pwm.start(50.0)

def right(): #right sound
    for i in range(8):
            pwm.ChangeFrequency(scale[i])
            time.sleep(0.3)
            pwm.stop()

def wrong(): #wrong sound
    for i in range(7, -1, -1):
                pwm.ChangeFrequency(scale[i])
                time.sleep(0.3)  
                pwm.stop()

def go(): #motor on
    GPIO.output(pin1, GPIO.HIGH) 
    GPIO.output(pin2, GPIO.LOW)
    time.sleep(3)

def stop(): #motor off
    GPIO.output(pin1, GPIO.LOW) 
    GPIO.output(pin2, GPIO.LOW)
    time.sleep(5)

#-------------------------------------
#x = 0.9345 # x, y : value for check
x = test.dist
y = 0.2234
try:
    if (x > 0.9): #Before drive / if he was same person
        right()
        while True: 
            a = GPIO.input(btn_pin)  
            if a == 0: #start
                go()
                for i in range(19000): #situation for check 
                    if i % 10000 == 0: #start, stop
                        stop()
                    elif i % 10000 == 1 : #face re-check
                        if (y > 0.8): #Driving / if he was same person
                            right()
                        else:
                            wrong()
                            go()
            else:
                stop()
    else : #Driving / if he wasn't same person
        wrong()      
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()