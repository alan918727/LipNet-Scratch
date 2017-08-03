# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 23:47:57 2017

@author: Alan
"""

import dlib
import numpy as np
import skvideo.io
import os,sys,fnmatch
import cv2

SOURCE_PATH = sys.argv[1]
SOURCE_EXTS = sys.argv[2]
TARGET_PATH = sys.argv[3]
FACE_PREDICTOR_PATH = sys.argv[4]

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

detector = dlib.get_frontal_face_detector()  #extract the face characteristic
predictor = dlib.shape_predictor(FACE_PREDICTOR_PATH)          
mouth_data=[]
for filepath in find_files(SOURCE_PATH, SOURCE_EXTS):
    #Initialization of cropped video size
    MOUTH_WIDTH = 100
    MOUTH_HEIGHT = 50
    HORIZONTAL_PAD = 0.15 #give spaces padding
    normalize_ratio = None
    mouth_frames = []
    print ("Processing: {}".format(filepath))
    videogen = skvideo.io.vreader(filepath)
    frames = np.array([frame for frame in videogen]) #read the video and save as numpy array
                     
    for frame in frames:
        dets=detector(frame,1)
        shape = None
        for k,d in enumerate(dets): #enumerate all the points
            shape = predictor(frame, d)
            i = -1
        mouth_points = []
        if shape == None:
            continue
        for i in range(68):

            if i < 48: # Only take mouth region from 48-67 (mouth)
                continue
            # append the mouth points to array
            mouth_points.append((shape.parts()[i].x,shape.parts()[i].y))
            
            if i == 59  :
                continue
            
            if i==67:
                cv2.line(frame,(shape.parts()[i].x,shape.parts()[i].y),\
                            (shape.parts()[i-7].x,shape.parts()[i-7].y),(0,255,0),1)
            else:
                
                # connect lines between feature point i and i+1 
                cv2.line(frame,(shape.parts()[i].x,shape.parts()[i].y),\
                                (shape.parts()[i+1].x,shape.parts()[i+1].y),(0,255,0),1)
                
            
            
        # alternative method to use circle visualization
            
#        for point in mouth_points:
#            cv2.circle(frame,point,2,(0,255,0))    
#        

            
    filepath_wo_ext = os.path.splitext(filepath)[0]
    target_dir = os.path.join(TARGET_PATH, filepath_wo_ext)
    print(target_dir)
    os.makedirs(target_dir)
    skvideo.io.vwrite(os.path.join(target_dir, "output.mpg"),frames)
