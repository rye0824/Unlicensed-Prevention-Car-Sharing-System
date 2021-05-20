import Jetson.GPIO as GPIO
import time


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
  

try: 
    right()

    while True:
        a = GPIO.input(tog_pin)
        b = GPIO.input(btn_pin)
        
        if a == 1:
            print("START")
            go()
            if b == 0:
                print("BRAKE")
                brake()
                
        else:
            print("STOP")
            stop()
            
        
except KeyboardInterrupt:
    GPIO.cleanup()