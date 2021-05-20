import Jetson.GPIO as GPIO
import time
import os
import test

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#PIN Setting
IN1_pin = 20 #pin38
IN2_pin = 16 #pin36
IN3_pin = 26 #pin37
IN4_pin = 19 #pin35
tog_pin = 18 #pin12
btn_pin = 6 #pin31
buzzer_pin = 13 #pwm pin33

GPIO.setup(btn_pin, GPIO.IN)
GPIO.setup(tog_pin, GPIO.IN)
GPIO.setup(IN1_pin, GPIO.OUT)
GPIO.setup(IN2_pin, GPIO.OUT)
GPIO.setup(IN3_pin, GPIO.OUT)
GPIO.setup(IN4_pin, GPIO.OUT)
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
    GPIO.output(IN1_pin, GPIO.HIGH) 
    GPIO.output(IN2_pin, GPIO.LOW) 
    GPIO.output(IN3_pin, GPIO.LOW) 
    GPIO.output(IN4_pin, GPIO.HIGH)

def brake(): #motor off
    GPIO.output(IN1_pin, GPIO.LOW) 
    GPIO.output(IN2_pin, GPIO.LOW) 
    GPIO.output(IN3_pin, GPIO.LOW) 
    GPIO.output(IN4_pin, GPIO.LOW)
    time.sleep(3)

def stop(): #motor off
    GPIO.output(IN1_pin, GPIO.LOW) 
    GPIO.output(IN2_pin, GPIO.LOW) 
    GPIO.output(IN3_pin, GPIO.LOW) 
    GPIO.output(IN4_pin, GPIO.LOW)

matching_score = test.dist

try: 
    if (matching_score > 0.60):
        right()
    
        while True:
            start_push = GPIO.input(tog_pin)
            brake_push = GPIO.input(btn_pin)
            
            if start_push == 1:
                print("START")
                go()
                if brake_push == 0:
                    print("BRAKE")
                    brake()
                    matching_score = test.dist
                    if matching_score < 0.6:
                        wrong()
            
            else:
                print("STOP")
                stop()
    else:
        wrong()       
except KeyboardInterrupt:
    GPIO.cleanup()
    pwm.stop()