import Jetson.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

buzzer_pin = 13
scale = [262, 294, 330, 349, 392, 440, 494, 523] 

GPIO.setup(buzzer_pin, GPIO.OUT)
pwm = GPIO.PWM(buzzer_pin, 262) 
pwm.start(50.0)

try:
    while True:
        for i in range(8):
            pwm.ChangeFrequency(scale[i])
            time.sleep(0.3)
            if i == 8:
                i=0
        
        
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
