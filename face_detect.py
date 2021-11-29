#!/usr/bin/env python

'''
face detection using haar cascades

USAGE:
    facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv

# local modules
from video import create_capture
from common import clock, draw_str

import glob
import time

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv.rectangle(img, (x1, y1), (x2, y2), color, 2)

    

    

def main():
    import sys, getopt

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try:
        video_src = video_src[0]
    except:
        video_src = 0
    
    args = dict(args)
  
    cascade_fn = args.get('--cascade', "/home/rye0824/opencv-4.5.1/data/haarcascades/haarcascade_frontalface_default.xml")
   

    cascade = cv.CascadeClassifier(cv.samples.findFile(cascade_fn))
    

    cam = create_capture(video_src, fallback='synth:bg={}:noise=0.05'.format(cv.samples.findFile('/home/rye0824/opencv-4.5.1/samples/data/lena.jpg')))

    count = 0 
    while True:
        _ret, img = cam.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)

   
        rects = detect(gray, cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0)) #face
        cv.imshow('facedetect', vis)

        if (len(rects) != 0):
            time.sleep(1)

            cv.imwrite("face_img"+".jpg", img)
            count += 1
            if count == 1:
                break 
    
        if cv.waitKey(5) == 27 :
            break
    img_file = glob.glob('./*.jpg')
    return img_file[0]

if __name__ == '__main__':
    print(__doc__)

    
    cv.destroyAllWindows()