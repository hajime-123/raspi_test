## 1動画の問題

５分ごとに動画は作成されているが、再生時間が実際より長いということが判明した。

厳密にいうと、再生時間がばらついていることが判明した。

理由を調べるために動画のフレーム数とフレームレートを調べた

```python
import cv2

#cap = cv2.VideoCapture("202104060940.m4v")                  # 動画を読み込む
cap = cv2.VideoCapture("202104061740.m4v")                  # 動画を読み込む
video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) # フレーム数を取得する
video_fps = cap.get(cv2.CAP_PROP_FPS)                 # フレームレートを取得する
video_len_sec = video_frame_count / video_fps         # 長さ（秒）を計算する
print(video_len_sec)                                  # 長さ
print(video_frame_count)  
print(video_fps)  
```

実際に１フレーム取得する時間を測定してみた

~~~python
import cv2
import time

cap = cv2.VideoCapture(0)


for i in range(5):
    t1 = time.time() * 1000
    ret, frame = cap.read()
    #cv2.imshow('Capture',frame)
    key = cv2.waitKey(1)
    t2 = time.time() * 1000
    print("diff : {0}[ms], ret : {1}".format((t2 - t1), ret))

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
~~~
![6](ラズパイflask本番画像3\1.PNG)

最初は動画の取得時間が長いが、それ以外は早く処理出来ている

下記のように20フレーム取得するのにsleep時間を調整したがうまくいかなかったでの断念

なぜか、frameを取得できなくなった？

```python
while True:
    #test=Camera()
    #20210408
    t3 = time.perf_counter() * 1000
    testframe=test2.get_frame()
    #display(Image(data=testframe))
    
    testframe2 = io.BytesIO(testframe)
    testframe3=Image.open(testframe2)
    testframe4=np.asarray(testframe3)
    testframe5= cv2.cvtColor(testframe4, cv2.COLOR_RGBA2BGR)
    testframe5 = cv2.resize(testframe5, size)
    #cv2.imwrite("./video/test2.jpg",testframe4)
    writer.write(testframe5)
    cv2.imshow('frame',testframe5)
    
    todaydetail = datetime.datetime.today()
    nametime1=todaydetail.strftime("%Y%m%d%H%M")
    if int(nametime1[-1])<5:
        nametime2=nametime1[:-1]+'0'
    else:
        nametime2=nametime1[:-1]+'5'
    #print(nametime2)
    if nametime2!=t2:
        #保存
        writer.release()
        #os.renames('../video/work/'+videoname,'../video/save/'+videoname)
        shutil.move('./video/work/'+videoname,'./video/save/'+videoname)#20210329変更
        #20210329変更
#             with zipfile.ZipFile('./video/save/'+t2+'.zip', "w", zipfile.ZIP_DEFLATED) as zf:
#                 zf.write( './video/work/'+videoname, arcname='./'+videoname)
#            os.remove('./video/work/'+videoname)
        path='./video/save/'
        files = os.listdir(path)
        files2 = sorted(files)
        MAX_CNT = 4
        for i in range(len(files)-MAX_CNT):
                print('{}は削除します'.format(files2[i]))
                os.remove('./video/save/'+files2[i])
        
        if os.path.exists(woek_path)!=True:
            os.mkdir(woek_path)
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        fps = 20.0
        size = (640, 360)
        t2=nametime2
        videoname=t2+'.m4v'
        writer = cv2.VideoWriter('./video/work/'+videoname, fmt, fps, size)
    
    if cv2.waitKey(1) & 0xFF == 13:   
        break
    
    # #20210408
    # t4= time.perf_counter() * 1000
    # process_time=t4- t3
    # sleep_time=45-process_time
    # if sleep_time<0:
    #     print(sleep_time)
    #     if cv2.waitKey(1)& 0xFF == 13:
    #             break

    # else:
       
    #     #print('{}処理時間'.format(sleep_time))
    #     if cv2.waitKey(int(sleep_time))& 0xFF == 13:
    #         break
        
    #     if cv2.waitKey(1) & 0xFF == 13:   
    #         break
writer.release()
cv2.destroyAllWindows()
```

また、スレッド部分をやめて別プログラムとして動かそうとしたが、カメラ部分でエラーを出したので

同一プログラム内に記載することにした



app.py

files2 = sorted(files)これがないと新しいものから消していった

app.use_reloader=False

app.run(host='192.168.100.111', port=8000,threaded=True, use_reloader=False)

・zipファイルを作るところをやめた

・ファイル一覧のところがおかしかったのでソートした

この２個がないとうまくスレッド部分が動かなかった

```python
import cv2
from flask import Flask, render_template, Response,session
import threading
import numpy as np
from PIL import Image,ImageOps
import io
import time
import datetime
import os
import shutil
from datetime import timedelta
import zipfile
import logging
from logging.handlers import TimedRotatingFileHandler

from camera import Camera,Camera2

app = Flask(__name__)
#app.debug = False
app.use_reloader=False

#保存
todaydetail = datetime.datetime.today()
t1=todaydetail.strftime("%Y%m%d%H%M")
if int(t1[-1])<5:
    t2=t1[:-1]+'0'
else:
    t2=t1[:-1]+'5'
videoname=t2+'.m4v'
videoname2=t2+'_2'+'.m4v'#20210409

#(1)workディレクトリがない場合は作る
work_path='./video/work'
if os.path.exists(work_path)!=True:
    os.mkdir(work_path)

#(2)workディレクトリに入っているデータはsaveへ移動最後にworkディレクトリ作成
files1 = os.listdir(work_path)
for file in files1:
    #os.renames('../video/work/'+file,'../video/save/'+file)
    shutil.move('./video/work/'+file,'./video/save/'+file)
    if os.path.exists(work_path)!=True:
        os.mkdir(work_path)

#20210409
#(1)work2ディレクトリがない場合は作る
work_path2='./video/work2'
if os.path.exists(work_path2)!=True:
    os.mkdir(work_path2)
#20210409
#(2)workディレクトリに入っているデータはsave2へ移動最後にwork2ディレクトリ作成
files2 = os.listdir(work_path2)
for file in files2:
    #os.renames('../video/work/'+file,'../video/save/'+file)
    shutil.move('./video/work2/'+file,'./video/save2/'+file)
    if os.path.exists(work_path2)!=True:
        os.mkdir(work_path2)

fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 20.0
size = (640, 360)
writer = cv2.VideoWriter('./video/work/'+videoname, fmt, fps, size)
writer2 = cv2.VideoWriter('./video/work2/'+videoname2, fmt, fps, size)#20210409




def test():
    global t2,videoname,writer,size,writer2

    test2=Camera()
    test2_2=Camera2()
    
    while True:
        #test=Camera()
        #20210408
        #t3 = time.perf_counter() * 1000
        testframe=test2.get_frame()
        #display(Image(data=testframe))
        
        testframe2 = io.BytesIO(testframe)
        testframe3=Image.open(testframe2)
        testframe4=np.asarray(testframe3)
        testframe5= cv2.cvtColor(testframe4, cv2.COLOR_RGBA2BGR)
        testframe5 = cv2.resize(testframe5, size)
        #cv2.imwrite("./video/test2.jpg",testframe4)
        writer.write(testframe5)
        cv2.imshow('frame',testframe5)
        
        #20210409
        testframe_2=test2_2.get_frame()
        testframe2_2 = io.BytesIO(testframe_2)
        testframe3_2=Image.open(testframe2_2)
        testframe4_2=np.asarray(testframe3_2)
        testframe5_2= cv2.cvtColor(testframe4_2, cv2.COLOR_RGBA2BGR)
        testframe5_2 = cv2.resize(testframe5_2, size)
        #cv2.imwrite("./video/test2.jpg",testframe4)
        writer2.write(testframe5_2)
        cv2.imshow('frame2',testframe5_2)
        
        todaydetail = datetime.datetime.today()
        nametime1=todaydetail.strftime("%Y%m%d%H%M")
        if int(nametime1[-1])<5:
            nametime2=nametime1[:-1]+'0'
        else:
            nametime2=nametime1[:-1]+'5'
        #print(nametime2)
        #------------
        if nametime2!=t2:
            #保存
            writer.release()
            #writer2.release()#20210409
            #os.renames('../video/work/'+videoname,'../video/save/'+videoname)
            shutil.move('./video/work/'+videoname,'./video/save/'+videoname)#20210329変更
            #shutil.move('./video/work2/'+videoname2,'./video/save2/'+videoname2)#2021409変更
            #20210329変更
    #             with zipfile.ZipFile('./video/save/'+t2+'.zip', "w", zipfile.ZIP_DEFLATED) as zf:
    #                 zf.write( './video/work/'+videoname, arcname='./'+videoname)
    #            os.remove('./video/work/'+videoname)
            path='./video/save/'
            files = os.listdir(path)
            files2 = sorted(files)
            MAX_CNT = 4
            for i in range(len(files)-MAX_CNT):
                    print('{}は削除します'.format(files2[i]))
                    os.remove('./video/save/'+files2[i])
            #2021409変更
            path_2='./video/save2/'
            files_2 = os.listdir(path_2)
            files2_2 = sorted(files_2)
            MAX_CNT = 4
            for i in range(len(files_2)-MAX_CNT):
                    print('{}は削除します'.format(files2_2[i]))
                    os.remove('./video/save2/'+files2_2[i])
            
            if os.path.exists(work_path)!=True:
                os.mkdir(work_path)
            fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            fps = 20.0
            size = (640, 360)
            t2=nametime2
            videoname=t2+'.m4v'
            writer = cv2.VideoWriter('./video/work/'+videoname, fmt, fps, size)
            #2021409変更
            if os.path.exists(work_path2)!=True:
                os.mkdir(work_path2)
            
            videoname2=t2+'_2'+'.m4v'#20210409
            writer2 = cv2.VideoWriter('./video/work2/'+videoname2, fmt, fps, size)
        
        
        if cv2.waitKey(1) & 0xFF == 13:   
            break
        
    writer.release()
    writer2.release()
    cv2.destroyAllWindows()

try:
    thread1 =threading.Thread(target=test)
    thread1.setDaemon(True)
    thread1.start()
except:
    writer.release()
    cv2.destroyAllWindows()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stream")
def stream():
    return render_template("stream.html")


def gen(camera):
    test_time=time.time()
    while True:
        frame = camera.get_frame()
        test_time2=time.time()
        if test_time2-test_time>60:
            break
        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        else:
            print("frame is none")

@app.route("/video_feed")
def video_feed():
    return Response(gen(Camera()),
            mimetype="multipart/x-mixed-replace; boundary=frame")
#20210409
@app.route("/stream2")
def stream2():
    return render_template("stream2.html")


def gen2(camera):
    test_time=time.time()
    while True:
        frame = camera.get_frame()
        test_time2=time.time()
        if test_time2-test_time>60:
            break
        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        else:
            print("frame is none")

@app.route("/video_feed2")
def video_feed2():
    return Response(gen2(Camera2()),
            mimetype="multipart/x-mixed-replace; boundary=frame")

# Blueprintを読み込む
import dist
app.register_blueprint(dist.app)

import glob
@app.route('/file1')
def root():
    #files=glob.glob('save/1/20200101/*')
    files=glob.glob('video/save/*')
    files2 = sorted(files)
    html='<html><meta charset="utf-8"><body>'
    html+='<h1>ファイル一覧</h1>'
    for f in files2:
        html+='<p><a href="{0}">{0}</a></p>'.format(f)
    html+='</body></html>'
    return html
#20210409
@app.route('/file2')
def root2():
    #files=glob.glob('save/1/20200101/*')
    files=glob.glob('video/save2/*')
    files2 = sorted(files)
    html='<html><meta charset="utf-8"><body>'
    html+='<h1>ファイル一覧</h1>'
    for f in files2:
        html+='<p><a href="{0}">{0}</a></p>'.format(f)
    html+='</body></html>'
    return html



if __name__ == "__main__":
    #rootロガーを取得
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    #出力のフォーマットを定義
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    #ファイルへ出力するハンドラーを定義
    #when='D','H','M'
    fh=logging.handlers.TimedRotatingFileHandler(filename='logs/log.txt',
                                                 when='D',
                                                 backupCount=7)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    #rootロガーにハンドラーを登録する
    logger.addHandler(fh)
    #app.run(host='127.0.0.1', port=8000,threaded=True)
    #app.run(host='192.168.100.111', port=8000,threaded=True, use_reloader=False)
    app.run(host='127.0.0.1', port=8000,threaded=True, use_reloader=False)
```

## 2mjpg-streamerのインストール

```
sudo apt-get install build-essential imagemagick libv4l-dev libjpeg-dev cmake -y
mkdir ~/mjpg
cd ~/mjpg
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
make
sudo make install
bash start.sh
```

/home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental/start.sh

自動起動できるようにする

/etc/systemd/system/内にmjpg.serviceファイルを作る

sudo nano mjpg1.service

```
[Unit]
Description = mjpg1
After = multi-user.target
[Service]
WorkingDirectory=/home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental/
ExecStart = /bin/bash /home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental/start.sh
User=root
Restart=always
KillSignal=SIGQUIT
Type=notify
#StandardError=syslog
NotifyAccess=all
[Install]
WantedBy=multi-user.target
```

WorkingDirectoryを記載（start.sh内に相対パス使っているから）

ExecStart = /bin/bashを記載

以上が大切

2台起動させるには以下のコマンドを打った

```
mjpg_streamer -i "./input_uvc.so -f 10 -r 640x360 -d /dev/video0 -y" -o "./output_http.so -w ./www -p 8080"
```

```
mjpg_streamer -i "./input_uvc.so -f 10 -r 640x360 -d /dev/video2 -y" -o "./output_http.so -w ./www -p 8081"
```

sudo nano mjpg2_1.service

sudo nano /etc/systemd/system/mjpg2_1.service

```
[Unit]
Description = mjpg2_1
After = multi-user.target
[Service]
WorkingDirectory=/home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental/
ExecStart = mjpg_streamer -i "./input_uvc.so -f 10 -r 640x360 -d /dev/video0 -y" -o "./output_http.so -w ./www -p 8080"
User=root
Restart=always
KillSignal=SIGQUIT
Type=notify
#StandardError=syslog
NotifyAccess=all
[Install]
WantedBy=multi-user.target
```

sudo nano /etc/systemd/system/mjpg2_2.service

```
[Unit]
Description = mjpg2_2
After = multi-user.target
[Service]
WorkingDirectory=/home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental/
ExecStart = mjpg_streamer -i "./input_uvc.so -f 10 -r 640x360 -d /dev/video2 -y" -o "./output_http.so -w ./www -p 8081"
User=root
Restart=always
KillSignal=SIGQUIT
Type=notify
#StandardError=syslog
NotifyAccess=all
[Install]
WantedBy=multi-user.target
```



```
#!/bin/sh
cd /home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental/
mjpg_streamer -i "./input_uvc.so -f 10 -r 640x360 -d /dev/video2 -y" -o "./output_http.so -w ./www -p 8081"
```

```
export LD_LIBRARY_PATH="/home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental"
STREAMER="$LD_LIBRARY_PATH/mjpg_streamer"
$STREAMER -i "./input_uvc.so -f 10 -r 640x360 -d /dev/video2 -y" -o "./output_http.so -w ./www -p 8081"
```

systemctlのコマンドは以下の通り

```
$ sudo systemctl status mjpg1 //status確認
$ sudo systemctl status mjpg2_1 //status確認
$ sudo systemctl daemon-reload
$ sudo systemctl start mjpg1 // uWSGI停止
$ sudo systemctl start mjpg2_1
$ sudo systemctl enable mjpg1
$ sudo systemctl enable mjpg2_1
$ sudo systemctl disable mjpg1
$ sudo systemctl disable mjpg2_1
```

なぜかsystemctlで起動するとビデオ収集が止まったり２台目カメラが止まったりした

クーロンタブに登録した

```
crontab -e
#@reboot                   sudo bash /home/pi/mjpg/vieo0.sh
#@reboot                   sudo bash /home/pi/mjpg/vieo2.sh
@reboot sudo bash /home/pi/mjpg/video0.sh
#@reboot sudo bash /home/pi/mjpg/video2.sh
```

video0.sh

```
cd /home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental
mjpg_streamer -i "./input_uvc.so -f 10 -r 640x360 -d /dev/video0 -y" -o "./output_http.so -w ./www -p 8080"
```

video2.sh

```
cd /home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental
mjpg_streamer -i "./input_uvc.so -f 10 -r 640x360 -d /dev/video0 -y" -o "./output_http.so -w ./www -p 8080"
```



chmod +x /home/pi/mjpg/video0.sh

chmod +x /home/pi/mjpg/video2.sh

ps -ef | grep sudo bash /home/pi/mjpg/video0

ps -ef | grep sudo bash



sudo nano /etc/systemd/system/mjpg0.service

```
[Unit]
Description = mjpg0
After = multi-user.target
[Service]
ExecStart = /bin/bash /home/pi/mjpg/video0.sh
User=root
Restart=always
#KillSignal=SIGQUIT
Type=simple
#StandardError=syslog
#NotifyAccess=all
[Install]
WantedBy=multi-user.target
```



```
sudo systemctl status mjpg0 //status確認
sudo systemctl daemon-reload
sudo systemctl start mjpg0
sudo systemctl enable mjpg0
```



## 3mjpg-streamerから動画撮影

video.py

```python
import cv2
# 映像が送られてくるリンクを指定する.
URL ="http://192.168.100.117:8080/?action=stream"
s_video = cv2.VideoCapture(URL)



while True:
    ret, img = s_video.read()
    cv2.imshow("WebCamera form Raspberry pi",img)
    key = cv2.waitKey(1)
    if key == 27: #Esc入力時は終了
        break

s_video.release()
cv2.destroyAllWindows()
```

video2.py

```bash
import cv2
# 映像が送られてくるリンクを指定する.
URL ="http://192.168.100.117:8080/?action=stream"
s_video = cv2.VideoCapture(URL)

fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 20.0
size = (640, 360)
writer = cv2.VideoWriter('output.mp4', fmt, fps, size)

while True:
    ret, frame = s_video.read()
    frame = cv2.resize(frame, size)
    cv2.imshow('frame', frame)
    writer.write(frame)
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
s_video.release()
writer.release()
cv2.destroyAllWindows()
```

video3.py

URL ="http://127.0.0.1:8080/?action=stream"これでIP変わってもいちいち打ち直さなくてもOK

```python
import cv2
import time
import datetime
import os
import shutil
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

#保存
todaydetail = datetime.datetime.today()
t1=todaydetail.strftime("%Y%m%d%H%M")
if int(t1[-1])<5:
    t2=t1[:-1]+'0'
else:
    t2=t1[:-1]+'5'
videoname=t2+'.m4v'

#(1)workディレクトリがない場合は作る
woek_path='./video/work'
if os.path.exists(woek_path)!=True:
    os.mkdir(woek_path)

#(2)workディレクトリに入っているデータはsaveへ移動最後にworkディレクトリ作成
files1 = os.listdir(woek_path)
for file in files1:
    #os.renames('../video/work/'+file,'../video/save/'+file)
    shutil.move('./video/work/'+file,'./video/save/'+file)
    if os.path.exists(woek_path)!=True:
        os.mkdir(woek_path)

fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 20.0
size = (640, 360)
writer = cv2.VideoWriter('./video/work/'+videoname, fmt, fps, size)

#URL ="http://192.168.100.117:8080/?action=stream"
URL ="http://127.0.0.1:8080/?action=stream"
s_video = cv2.VideoCapture(URL)

#--------------------------
#rootロガーを取得
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#出力のフォーマットを定義
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#ファイルへ出力するハンドラーを定義
#when='D','H','M'
fh=logging.handlers.TimedRotatingFileHandler(filename='logs/videolog.txt',
                                             when='H',
                                             backupCount=7)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
#rootロガーにハンドラーを登録する
logger.addHandler(fh)
logger.debug('ロギング 開始')
#--------------------------
logger.info(t1)

try:
    while True:
        logging.basicConfig(filename='logs/'+t1+'error.log',level=logging.DEBUG)
        
        t3 = time.perf_counter() * 1000
        ret, frame = s_video.read()
        frame = cv2.resize(frame, size)
        todaydetail = datetime.datetime.today()
        t=todaydetail.strftime("%Y/%m/%d/ %H:%M:%S")
        cv2.putText(frame,t,(2,26),cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
        
        cv2.imshow('frame',frame) 
        writer.write(frame)
        
        nametime1=todaydetail.strftime("%Y%m%d%H%M")
        if int(nametime1[-1])<5:
                nametime2=nametime1[:-1]+'0'
        else:
            nametime2=nametime1[:-1]+'5'
        
        if nametime2!=t2:
                #保存
            writer.release()
            shutil.move('./video/work/'+videoname,'./video/save/'+videoname)#20210329変更
            path='./video/save/'
            files = os.listdir(path)
            files2 = sorted(files)
            MAX_CNT = 4
            for i in range(len(files)-MAX_CNT):
                    logger.info('{}は削除します'.format(files2[i]))
                    os.remove('./video/save/'+files2[i])
            
            if os.path.exists(woek_path)!=True:
                os.mkdir(woek_path)
            fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            fps = 20.0
            size = (640, 360)
            t2=nametime2
            videoname=t2+'.m4v'
            writer = cv2.VideoWriter('./video/work/'+videoname, fmt, fps, size)
        
        if cv2.waitKey(1) & 0xFF == 13:   
            break
except:
    logger.exception(sys.exc_info())
```

変更エラー処理を追加

```python
import cv2
import time
import datetime
import os
import shutil
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

#保存
todaydetail = datetime.datetime.today()
t1=todaydetail.strftime("%Y%m%d%H%M")
if int(t1[-1])<5:
    t2=t1[:-1]+'0'
else:
    t2=t1[:-1]+'5'
videoname=t2+'.m4v'

#(1)workディレクトリがない場合は作る
woek_path='./video/work'
if os.path.exists(woek_path)!=True:
    os.mkdir(woek_path)

#(2)workディレクトリに入っているデータはsaveへ移動最後にworkディレクトリ作成
files1 = os.listdir(woek_path)
for file in files1:
    #os.renames('../video/work/'+file,'../video/save/'+file)
    shutil.move('./video/work/'+file,'./video/save/'+file)
    if os.path.exists(woek_path)!=True:
        os.mkdir(woek_path)

fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 20.0
size = (640, 360)
writer = cv2.VideoWriter('./video/work/'+videoname, fmt, fps, size)

URL ="http://192.168.100.117:8080/?action=stream"
s_video = cv2.VideoCapture(URL)
err_count=0

#--------------------------
#rootロガーを取得
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#出力のフォーマットを定義
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#ファイルへ出力するハンドラーを定義
#when='D','H','M'
fh=logging.handlers.TimedRotatingFileHandler(filename='logs/videolog.txt',
                                             when='H',
                                             backupCount=7)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
#rootロガーにハンドラーを登録する
logger.addHandler(fh)
logger.debug('ロギング 開始')
#--------------------------
logger.info(t1)

try:
    while True:
        #logging.basicConfig(filename='logs/'+t1+'error.log',level=logging.DEBUG)
        
        t3 = time.perf_counter() * 1000
        try:
            ret, frame = s_video.read()
            frame = cv2.resize(frame, size)
        except:
            logger.info('通信エラー')
            logger.info(t1)
            time.sleep(20)
            err_count=err_count+1
            logger.info(err_count)
            s_video = cv2.VideoCapture(URL)
            if err_count==5:
                logger.info('再起動してください')
                break
            continue
            
        
        todaydetail = datetime.datetime.today()
        t=todaydetail.strftime("%Y/%m/%d/ %H:%M:%S")
        cv2.putText(frame,t,(2,26),cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
        
        #cv2.imshow('frame',frame) 
        writer.write(frame)
        
        nametime1=todaydetail.strftime("%Y%m%d%H%M")
        if int(nametime1[-1])<5:
                nametime2=nametime1[:-1]+'0'
        else:
            nametime2=nametime1[:-1]+'5'
        
        if nametime2!=t2:
                #保存
            writer.release()
            shutil.move('./video/work/'+videoname,'./video/save/'+videoname)#20210329変更
            path='./video/save/'
            files = os.listdir(path)
            files2 = sorted(files)
            MAX_CNT = 4
            for i in range(len(files)-MAX_CNT):
                    logger.info('{}は削除します'.format(files2[i]))
                    os.remove('./video/save/'+files2[i])
            
            if os.path.exists(woek_path)!=True:
                os.mkdir(woek_path)
            fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            fps = 20.0
            size = (640, 360)
            t2=nametime2
            videoname=t2+'.m4v'
            writer = cv2.VideoWriter('./video/work/'+videoname, fmt, fps, size)
        
        if cv2.waitKey(1) & 0xFF == 13:   
            break
except:
    logger.exception(sys.exc_info())
    

```

自動起動できるようにする

video3.sh

```
cd /home/pi/flask-test4/
python3 /home/pi/flask-test4/video3.py
```

sudo nano /etc/systemd/system/mjpg_video.service

```
[Unit]
Description = mjpg_video
After = multi-user.target
[Service]
WorkingDirectory=/home/pi/flask-test4
ExecStart = /bin/bash /home/pi/flask-test4/video3.sh
User=root
Restart=always
KillSignal=SIGQUIT
Type=notify
#StandardError=syslog
NotifyAccess=all
[Install]
WantedBy=multi-user.target
```

/usr/bin/python3 /home/pi/flask-test4/video3.py

/bin/bash /home/pi/flask-test4/video3.sh

Type=simpleにしないと動かなかった。

```
[Unit]
Description = mjpg_video
After = multi-user.target
[Service]
WorkingDirectory=/home/pi/flask-test4
ExecStart = /bin/bash /home/pi/flask-test4/video3.sh
User=root
Restart=always
#KillSignal=SIGQUIT
Type=simple
#StandardError=syslog
#NotifyAccess=all
[Install]
WantedBy=multi-user.target
```



```
$ sudo systemctl status mjpg_video //status確認
$ sudo systemctl daemon-reload
$ sudo systemctl start mjpg_video // スタート
$ sudo systemctl enable mjpg_video // uWSGI停止
```

うまくいかないのでクーロンに登録

```
crontab -e
00 * * * * sudo bash /home/pi/flask-test3/log.sh
@reboot sudo bash /home/pi/mjpg/video0.sh
@reboot sudo bash /home/pi/flask-test4/video3.sh
```



## 4mjpg-streamerとflask



```python
import cv2
from flask import Flask, render_template, Response,session
import threading
import numpy as np
from PIL import Image,ImageOps
import io
import time
import datetime
import os
import shutil
from datetime import timedelta
import zipfile
import logging
from logging.handlers import TimedRotatingFileHandler

#from camera import Camera

app = Flask(__name__)
#app.debug = False
app.use_reloader=False


@app.route("/")
def index():
    return render_template("index.html")


# Blueprintを読み込む
import dist
app.register_blueprint(dist.app)

import glob
@app.route('/file1')
def root():
    #files=glob.glob('save/1/20200101/*')
    files=glob.glob('video/save/*')
    files2 = sorted(files)
    html='<html><meta charset="utf-8"><body>'
    html+='<h1>ファイル一覧</h1>'
    for f in files2:
        html+='<p><a href="{0}">{0}</a></p>'.format(f)
    html+='</body></html>'
    return html

if __name__ == "__main__":
    #rootロガーを取得
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    #出力のフォーマットを定義
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    #ファイルへ出力するハンドラーを定義
    #when='D','H','M'
    fh=logging.handlers.TimedRotatingFileHandler(filename='logs/log.txt',
                                                 when='D',
                                                 backupCount=7)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    #rootロガーにハンドラーを登録する
    logger.addHandler(fh)
    #app.run(host='127.0.0.1', port=8000,threaded=True)
    app.run(host='192.168.100.111', port=8000,threaded=True, use_reloader=False)
    #app.run(host='127.0.0.1', port=8000,threaded=True, use_reloader=False)
```

index.html

```html
<html>
  <head>
    <title>AKT Test</title>
  </head>
  <body>
    <h1>AKT Test</h1>
    <a href="http://192.168.100.117:8080/stream_simple.html">動画1</a>
    <a href="/file1">動画1ファイル</a>
    <p class="news-item">
      半割ROD装置のリアルタイム動画サイトです。<br>
      動画1にリアルタイム動画<br>
      動画1ファイルに過去動画があります<br>
      よろしくお願いします。<br>
      
  </p>
  </body>
</html>
```

自動起動できるようにする

sudo nano /home/pi/flask-test4/myapp.ini

```
[uwsgi]
current_release = /home/pi/flask-test4
chdir = %(current_release)
wsgi-file=%(current_release)/app.py
callable=app
#callable=logger

processes = 4
threads = 2
thunder-lock = true
max-requests = 3000
max-requests-delta = 300
master = True
workers = 1
enable-threads = true
lazy-apps = true

socket = /tmp/uwsgi.sock
chmod-socket = 666
vacuum = true
die-on-term = true
logto = /home/pi/flask-test4/logs/uwsgi.log
logfile-chown
log-master = true
log-reopen = true
touch-logreopen = /home/pi/flask-test3/logs/logreopen
```

動作確認

/usr/local/bin/uwsgi --ini  /home/pi/flask-test4/myapp.ini

sytemed登録

/etc/systemd/system/内にuwsgi4.serviceファイルを作る

sudo nano /etc/systemd/system/uwsgi4.service

```
[Unit]
Description = uWSGI4
After = syslog.target
[Service]
WorkingDirectory=/home/pi/flask-test4
ExecStart = /usr/local/bin/uwsgi --ini /home/pi/flask-test4/myapp.ini
User=root
Restart=always
KillSignal=SIGQUIT
Type=notify
#StandardError=syslog
NotifyAccess=all
[Install]
WantedBy=multi-user.target
```

起動

```
sudo systemctl daemon-reload
sudo systemctl start uwsgi4
sudo systemctl enable uwsgi4
```

logローテーション設定設定

sudo nano /etc/logrotate.d/uwsgi4_log

```
/home/pi/flask-test4/logs/uwsgi.log {
    create 666 root root
    hourly
    missingok
    rotate 10
    notifempty
    compress
    dateext
    dateformat -%Y%m%d%H
    sharedscripts
    postrotate
            touch /home/pi/flask-test4/logs/logreopen
    endscript
}
```

sudo /usr/sbin/logrotate -f /etc/logrotate.d/uwsgi4_log

あとはcrontabで動かす

sudo nano /home/pi/flask-test4/uwsgi4_log.sh

```
#!/bin/bash
sudo /usr/sbin/logrotate -f /etc/logrotate.d/uwsgi4_log
```

 crontab -e

```
crontab -e
#00 * * * * sudo bash /home/pi/flask-test3/log.sh
@reboot sudo bash /home/pi/mjpg/video0.sh
@reboot sudo bash /home/pi/flask-test4/video3.sh
00 * * * * sudo bash /home/pi/flask-test4/uwsgi4_log.sh
```



## 有線、無線の設定

```
sudo nano /etc/dhcpcd.conf
```

```
#無線
interface wlan0
static ip_address=192.168.100.111/24
static routers=192.168.100.1
#static domain_name_servers=192.168.100.1
#無線
interface wlan0
static ip_address=192.168.100.117/24
static routers=192.168.100.1
#static domain_name_servers=192.168.100.1
#有線
interface eth0
static ip_address=172.21.5.160/24
static routers=172.21.5.253
#static domain_name_servers=172.21.5.253

interface eth0
static ip_address=192.168.9.57/26
static routers=192.168.9.62
```



## ファイアウォール設定



ログイン用のポートは/etc/xrdp/xrdp.ini

![6](ラズパイflask本番画像\7.PNG)

画面転送用のポートは/etc/xrdp/sesman.ini

![6](ラズパイflask本番画像\8.PNG)

ここでリモートデスクトップのポート確認



```bash
sudo apt install ufw
sudo ufw status
sudo ufw allow 22
sudo ufw allow 5900
sudo ufw allow 3389
sudo ufw allow 3350
sudo ufw allow Samba
sudo ufw allow vnc
sudo ufw allow 5000
sudo ufw allow 8000
sudo ufw allow 8080
sudo ufw allow 8081
sudo ufw default deny  # 許可されたポート以外を閉じる
sudo ufw enable  # ufwの有効化
sudo ufw status numbered
sudo ufw app list
sudo ufw disable
```











































```
 crontab -e
```

```
00 * * * * sudo bash /home/pi/flask-test3/log.sh
```

