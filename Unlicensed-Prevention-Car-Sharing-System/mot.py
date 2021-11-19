import Jetson.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pin1 = 19 #pin35
pin2 = 16 #pin36
btn_pin = 20 #pin38

GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
#GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try: 
    while True:
        a = GPIO.input(btn_pin)
        if a == 1:
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.LOW)
        else:
            GPIO.output(pin1, GPIO.HIGH) 
            GPIO.output(pin2, GPIO.LOW) 
            time.sleep(5)     
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.LOW) 
            time.sleep(5)
            GPIO.output(pin1, GPIO.HIGH) 
            GPIO.output(pin2, GPIO.LOW)             
except KeyboardInterrupt:
    GPIO.cleanup()
   




