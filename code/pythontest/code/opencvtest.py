#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 06:19:53 2021

@author: ubuntu
"""

import cv2

cap = cv2.VideoCapture(0) # VideoCaptureのインスタンスを作成する。(複数のカメラがあるときは引数で識別)

while True:
    ret, frame = cap.read()     # 1フレーム読み込む

    # 画像を表示する
    cv2.imshow('Image', frame)

    k = cv2.waitKey(1)  #引数は待ち時間(ms)
    if k == 27: #Esc入力時は終了
        break

# 終了処理
cap.release()
cv2.destroyAllWindows()

