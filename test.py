import os
import torch
import numpy as np
import cv2
import time
import glob

from dataLoader import *
from preprocessing import *
from utils import *
from config import *
from models.LightCNN.light_cnn import *

def l2_norm(input,axis=1):
    norm = torch.norm(input,2,axis,True)#input tensor, dimension => vector size function 
    output = torch.div(input, norm)#devide input by norm
    return output

config = configuration()
if config.device == -1:
    device_info = "cpu"
else:
    device_info = "cuda:" + str(config.device) #config.device = 0, run cuda
device = torch.device(device_info)#default cuda device 


def gstreamer_pipeline(
    capture_width=3280,
    capture_height=2464,
    display_width=820,
    display_height=616,
    framerate=21,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


        
with torch.no_grad():
    os.remove("face_0.png")
    face_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    )
   
    count = 0 

    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        cv2.namedWindow("Face Detect", cv2.WINDOW_AUTOSIZE)
       
        while cv2.getWindowProperty("Face Detect", 0) >= 0:
           
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            cv2.imshow("Face Detect", img)

            if (len(faces) != 0):
                cv2.imwrite("face_"+str(count)+".png", img)
                
                count += 1
            if count == 1:
                break 

    model = LightCNN_29Layers_v2(1)
    model = loadModel(model, config.pretrained_model, device)
    model.to(device) #convert to optimized model
    model.eval()

    ref = []
    query = []

    img_file = glob.glob('./*.png')
  
    ref.append(image_norm(config.refImg))#preprocessing.py->def image_norm : plus to list 
    ref = np.array(ref, dtype='float32')#make array with float32 type 
    refData = torch.from_numpy(ref).float()#numpy -> make tensor dataset ==> input model ==> loss ...
    refData = refData.to(device)
    refFeatVec = model(refData, embedding=True).to(device)
    refFeatVec = refFeatVec.detach()
    refFeatVec = l2_norm(refFeatVec)

    query.append(image_norm(img_file[0]))
    query = np.array(query, dtype='float32')
    queryData = torch.from_numpy(query).float()
    queryData = queryData.to(device)
    queryFeatVec = model(queryData, embedding=True)
    queryFeatVec = queryFeatVec.detach()
    queryFeatVec = l2_norm(queryFeatVec)

    refFV = refFeatVec.detach().cpu().numpy()#GPU TO CPU
    queryFV = queryFeatVec.detach().cpu().numpy()#GPU TO CPU

    dist_mat = np.dot(refFV, queryFV.T)#refFV[0]*queryFV.T[0]+refFV[1]*queryFV.T[1]
    dist = np.diag(dist_mat)#Extract a diagnal or construct a diagonal array 
    
    print("matching score: " ,dist)	
    cap.release()
    cv2.destroyAllWindows()  
    

   