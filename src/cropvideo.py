# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 23:47:57 2017

@author: Alan
"""

import dlib
import numpy as np
from skimage import io
from scipy.misc import imresize
import skvideo.io
import os,sys,fnmatch

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
        
        for part in shape.parts(): #len(shape.parts)=68
            i += 1
            if i < 48: # Only take mouth region from 48-67 (mouth)
                continue
            mouth_points.append((part.x,part.y))
        np_mouth_points = np.array(mouth_points)
        mouth_centroid = np.mean(np_mouth_points[:, -2:], axis=0)
        
        #cropped the image
        if normalize_ratio is None:
            mouth_left = np.min(np_mouth_points[:, :-1]) * (1.0 - HORIZONTAL_PAD) #first column: the x-axis min
            mouth_right = np.max(np_mouth_points[:, :-1]) * (1.0 + HORIZONTAL_PAD)#first column: the x-axis max
        
            normalize_ratio = MOUTH_WIDTH / float(mouth_right - mouth_left) #x-axis scaling ratio
        
        new_img_shape = (int(frame.shape[0] * normalize_ratio), int(frame.shape[1] * normalize_ratio))
        resized_img = imresize(frame, new_img_shape)
        
        mouth_centroid_norm = mouth_centroid * normalize_ratio #new resized centroid
        
        mouth_l = int(mouth_centroid_norm[0] - MOUTH_WIDTH / 2)
        mouth_r = int(mouth_centroid_norm[0] + MOUTH_WIDTH / 2)
        mouth_t = int(mouth_centroid_norm[1] - MOUTH_HEIGHT / 2)
        mouth_b = int(mouth_centroid_norm[1] + MOUTH_HEIGHT / 2)
        
        mouth_crop_image = resized_img[mouth_t:mouth_b, mouth_l:mouth_r]
        
        mouth_frames.append(mouth_crop_image)
        mouth = np.array(mouth_frames)
    filepath_wo_ext = os.path.splitext(filepath)[0]
    target_dir = os.path.join(TARGET_PATH, filepath_wo_ext)
    print(target_dir)
    os.makedirs(target_dir)

    fr = 0
    for croppedframe in mouth:
        io.imsave(os.path.join(target_dir, "mouth_{0:03d}.png".format(fr)), croppedframe)
        fr += 1  #save frames into target_dir
        
    mouth_data.append(mouth_frames) #save all videos' data 
    alldata=np.array(mouth_data) # with size Samples*Frames*Height*Weight*Channels
        