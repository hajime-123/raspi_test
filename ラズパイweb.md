###fwebセッティング
まずはflaskのインストール

~~~  
sudo pip3 install flask
~~~  
開発環境どちらか選ぶ
~~~  
sudo apt install spyder3
thonny
~~~  
opencvは下記を参考にした  
~~~  
https://sd08419ttic.hatenablog.com/entry/2020/01/26/231151
~~~  

mjpg-streamerのインストール  
https://denkenmusic.com/raspberry-pi-4b-%E3%82%AB%E3%83%A1%E3%83%A9%E5%8B%95%E7%94%BB%E9%85%8D%E4%BF%A1%E3%80%8Cmjpg-streamer%E3%80%8D%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%A8%E8%A8%AD%E5%AE%9A/
~~~  
#mjpg-streamerに必要なモジュールをインストール
sudo apt-get install libjpeg8-dev cmake
#mjpgというフォルダを作り、mjpg-streamerのソースコードをダウンロード
mkdir ~/mjpg
cd ~/mjpg
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
make
sudo make install
~~~ 
mjpg-streamerの確認
~~~  
cd mjpg-streamer/mjpg-streamer-experimental
bash start.sh
~~~ 
ストリーミングされた動画を別PCで受信して処理する方法
~~~  
https://sd08419ttic.hatenablog.com/entry/2020/01/26/231151
~~~ 
ファイル共有
~~~ 
sudo apt-get install samba#うまくいかない？
sudo apt install samba
sudo vi /etc/samba/smb.conf

[Share]#共有するディレクトリ名
path = /home#共有ディレクトリのパス
writeable = yes#書き込み許可
guest ok = yes#ゲストユーザーを許可
guest only = yes#ゲストユーザーのみ接続可
create mode = 0777# フルアクセスでファイル作成
directory mode = 0777# フルアクセスでフォルダ作成

testparm
sudo systemctl restart smbd
sudo systemctl enable smbd 
sudo systemctl status smbd
\\IPアドレスで確認することができる
~~~ 
mp4再生
~~~ 
sudo apt install ubuntu-restricted-extras
sudo apt install libav-tools ffmpeg#うまくいかなかった
sudo apt install ffmpeg#これを入れてもうまくいかなかった
sudo apt install libdvd-pkg#これを入れたら成功した
~~~ 
エラー対策
~~~ 

dpkg was interrupted, you must manually run 'sudo dpkg --configure -a' to correct the probrem

~~~ 

flaskとopencvを使って画像表示
https://qiita.com/RIckyBan/items/a7dea207d266ef835c48
FlaskとOpenCVでカメラ画像をストリーミングして複数ブラウザでアクセスする
~~~ 
.
├── app.py
├── base_camera.py
├── camera.py
└── templates
    └── stream.html
~~~ 
templates/stream.html
~~~ 
.<html>
  <head>
    <title>Flask Streaming Test</title>
  </head>
  <body>
    <h1>Flask Streaming Test</h1>
    <img src="{{ url_for('video_feed') }}">
  </body>
</html>
~~~ 
app.py
~~~ 
import cv2
from flask import Flask, render_template, Response

from camera import Camera

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"

@app.route("/stream")
def stream():
    return render_template("stream.html")

def gen(camera):
    while True:
        frame = camera.get_frame()

        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame.tobytes() + b"\r\n")
        else:
            print("frame is none")

@app.route("/video_feed")
def video_feed():
    return Response(gen(Camera()),
            mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, threaded=True)
~~~ 
camera.py
~~~ 
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    def __init__(self):
        super().__init__()

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
~~~ 
base_camera.py
~~~ 
import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """
    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    event = CameraEvent()

    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            # start background frame thread
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        BaseCamera.last_access = time.time()

        # wait for a signal from the camera thread
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None
~~~ 











