###ubunt20.04の32ビットのセッティング
まずはパスワードの変更をする  
WiFiの設定を行う  
cd /etc/netplan  
sudo vim 50-cloud-init.yaml  

~~~  
netwoek:  
	ethernets:  
		eth0:  
		dhcp4: true  
		optional: true
	version: 2  
	#ここから下を追加  
	wifis:  
		wlan0:  
			optional: true
			dhcp4: true
			access-points:
				"ssid":
					password: "パスワード"
~~~  
エラー確認  
~~~  
sudo netplan --debug try
sudo netplan --debug generate
~~~  
反映  
~~~  
sudo netplan --debug apply
~~~  
うまくいかない時
~~~  
sudo systemctl start wpa_supplicant
shutdown now
sudo 
~~~  
###デスクトップ導入
~~~ 
sudo apt update
sudo apt upgrade
sudo apt install net-tools
sudo apt install ubuntu-desktop
sudo apt install ubuntu-mate-desktop　こっちは重いかも
sudo apt-get install xrdp リモート接続できるように
sudo apt-get install lxde　デスクトップが重いときなくてもいい
~~~ 


Ubuntuのバージョン確認
~~~  
cat /etc/os-release
~~~ 
GPIOの設定
~~~  
sudo apt install wiringpi
sudo gpio readall
うまくいかない時は
cd /tmp
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
~~~ 
デスクトップが重いとき
~~~ 
sudo apt-get install gnome
sudo apt-get install lxde　こっちのほうがいいかな

~~~ 
openCVインストール  
~~~ 
sudo python3 get-pip.py #うまくいかない
sudo pip install --upgrade pip　#うまくいかない
sudo apt-get install python3-pip　
sudo pip3 install opencv-python==4.1.0.25　#うまくいかない	
pip install opencv-contrib-python　#うまくいかない
sudo pip3 install opencv-python　#うまくいかない？時間かかる？
sudo apt-get install python-opencv　#うまくいかない
pip3 install opencv-contrib-python　#うまくいかない？時間かかる？
sudo pip3 install opencv-python==4.3.0.38 #うまくいかない？時間かかる？
sudo pip3 install opencv-python==3.4.10.37
sudo pip3 install opencv-python==4.3.0.38
https://qiita.com/masaru/items/658b24b0806144cfeb1c
sudo apt-get install libopencv-dev
sudo apt-get install python-opencv
pip3 install opencv-python==3.4.2.17

# ビルドツール関係(もしかしたらいらないかも)
sudo apt-get install build-essential cmake pkg-config
# 画像関係
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev #入らない
# 動画関係
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
# 最適化関係
sudo apt-get install libatlas-base-dev gfortran
# HDF5関係
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
# Qtライブラリ

sudo apt install libopencv-dev python3-opencv#これでうまくいった
~~~ 


