import Jetson.GPIO as GPIO
import time
import os
import test


import torch
from dataLoader import *
from preprocessing import *
from utils import *
from config import *
from models.LightCNN.light_cnn import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

matching_score = test.dist

#==================pin setting===============
IN1_pin = 20 #pin38
IN2_pin = 16 #pin36
IN3_pin = 26 #pin37
IN4_pin = 19 #pin35
btn_pin = 18 #pin12, green
brake_pin = 6 #pin31. white

GPIO.setup(btn_pin, GPIO.IN)
GPIO.setup(brake_pin, GPIO.IN)
GPIO.setup(IN1_pin, GPIO.OUT)
GPIO.setup(IN2_pin, GPIO.OUT)
GPIO.setup(IN3_pin, GPIO.OUT)
GPIO.setup(IN4_pin, GPIO.OUT)


#==================sensor control===============
def go(): #motor on
    GPIO.output(IN1_pin, GPIO.HIGH) 
    GPIO.output(IN2_pin, GPIO.LOW) 
    GPIO.output(IN3_pin, GPIO.LOW) 
    GPIO.output(IN4_pin, GPIO.HIGH)

def brake():
    for _ in range(3000): 
        GPIO.output(IN1_pin, GPIO.LOW) 
        GPIO.output(IN2_pin, GPIO.LOW) 
        GPIO.output(IN3_pin, GPIO.LOW) 
        GPIO.output(IN4_pin, GPIO.LOW)
    print("*****************BRAKE*******************")
    def l2_norm(input,axis=1):
        norm = torch.norm(input,2,axis,True)
        output = torch.div(input, norm)
        return output

    config = configuration()
    if config.device == -1:
        device_info = "cpu"
    else:
        device_info = "cuda:" + str(config.device)
    device = torch.device(device_info)

    model = LightCNN_29Layers_v2(1)
    model = loadModel(model, config.pretrained_model, device)
    model.to(device)
    model.eval()

    ref = []
    query = []

    with torch.no_grad():
        ref.append(image_norm(config.refImg))
        ref = np.array(ref, dtype='float32')
        refData = torch.from_numpy(ref).float()
        refData = refData.to(device)
        refFeatVec = model(refData, embedding=True).to(device)
        refFeatVec = refFeatVec.detach()
        refFeatVec = l2_norm(refFeatVec)

        query.append(image_norm("./test_img/D1.jpg"))
        query = np.array(query, dtype='float32')
        queryData = torch.from_numpy(query).float()
        queryData = queryData.to(device)
        queryFeatVec = model(queryData, embedding=True)
        queryFeatVec = queryFeatVec.detach()
        queryFeatVec = l2_norm(queryFeatVec)

        refFV = refFeatVec.detach().cpu().numpy()
        queryFV = queryFeatVec.detach().cpu().numpy()

        dist_mat = np.dot(refFV, queryFV.T)
        new_dist = np.diag(dist_mat)

        print("Matching Score : " , new_dist)  
    
    if (new_dist > 0.90):
        for _ in range(100): 
            print("PASS")
            
    else:   
        for _ in range(100): 
            print("FAIL")
            time.sleep(100)
            
        
def callback_func1(channel):
    brake()

    
def stop(): #motor off
    GPIO.output(IN1_pin, GPIO.LOW) 
    GPIO.output(IN2_pin, GPIO.LOW) 
    GPIO.output(IN3_pin, GPIO.LOW) 
    GPIO.output(IN4_pin, GPIO.LOW)


GPIO.add_event_detect(6, GPIO.RISING, callback=callback_func1)


try: 
    if (matching_score > 0.90):
        print("PASS")
        while True:    
            start_push = GPIO.input(btn_pin)
            if start_push == 0:
                for _ in range(7000):
                    print("START")
                    go()
                

            else:
                print("STOP")
                stop()
    else:
        print("FAIL")
        stop()
                   
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()