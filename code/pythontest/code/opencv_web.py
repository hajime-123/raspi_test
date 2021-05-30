#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 06:45:50 2021

@author: ubuntu
"""

import cv2

 #mjpg-streamerを動作させているPC・ポートを入力
URL = "http://192.168.100.111:8080/?action=stream"
s_video = cv2.VideoCapture(URL)

while True:
    ret, img = s_video.read()
    cv2.imshow("WebCamera form Raspberry pi",img)
    k = cv2.waitKey(1)
    if k == 27: #Esc入力時は終了
        break


