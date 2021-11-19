import Jetson.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

IN1_pin = 20 #pin38
IN2_pin = 16 #pin36
IN3_pin = 26 #pin37
IN4_pin = 19 #pin35
tog_pin = 18 #pin12

GPIO.setup(tog_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN1_pin, GPIO.OUT)
GPIO.setup(IN2_pin, GPIO.OUT)
GPIO.setup(IN3_pin, GPIO.OUT)
GPIO.setup(IN4_pin, GPIO.OUT)

try: 
    while True:
        a = GPIO.input(tog_pin)
        print(a)
        
        if a == 1:
            GPIO.output(IN1_pin, GPIO.HIGH) 
            GPIO.output(IN2_pin, GPIO.LOW) 
            GPIO.output(IN3_pin, GPIO.HIGH) 
            GPIO.output(IN4_pin, GPIO.LOW) 
        else:
            GPIO.output(IN1_pin, GPIO.LOW) 
            GPIO.output(IN2_pin, GPIO.LOW) 
            GPIO.output(IN3_pin, GPIO.LOW) 
            GPIO.output(IN4_pin, GPIO.LOW) 
        

except KeyboardInterrupt:
    GPIO.cleanup()