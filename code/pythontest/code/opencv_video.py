#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 14:26:00 2021

@author: ubuntu
"""

import cv2

URL = "http://192.168.100.111:8080/?action=stream" 
cap = cv2.VideoCapture(0)
 
#保存
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 20.0
size = (640, 360)
writer = cv2.VideoWriter('outtest.m4v', fmt, fps, size)
 
while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, size)
     
    #保存
    writer.write(frame)
     
    cv2.imshow('frame', frame)
    #Enterキーで終了
    if cv2.waitKey(1) == 13:
        break
 
#保存
writer.release()
cap.release()
cv2.destroyAllWindows()