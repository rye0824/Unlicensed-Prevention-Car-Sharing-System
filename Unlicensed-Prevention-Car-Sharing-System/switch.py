import Jetson.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

btn_pin = 19
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try: 
    while True:
        a = GPIO.input(btn_pin)
        if a ==1:
            print("a is 1")
        else:
            print("a is 0")
except KeyboardInterrupt:
    GPIO.cleanup()
   