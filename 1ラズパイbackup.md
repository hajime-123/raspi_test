###バックアップ
~~~  
sudo fdisk -l
~~~

![Test Image 1](ラズパイbackup画像/1.PNG)  

/dev/mmcblk0にラズパイ環境が入っている  
sdカードを接続  

![Test Image 1](ラズパイbackup画像/2.PNG)  

/dev/sdaにマウントされていることがわかる  
FAT32にフォーマットする  

![Test Image 1](ラズパイbackup画像/3.PNG)  

FAT32にフォーマットされていることが確認できる  


~~~ 
#bs=1Mこれでは遅いかも
sudo dd if=/dev/mmcblk0 bs=10M | gzip > /home/ubuntu/ubuntubackup_202103.gz
gzip -dc /home/ubuntu/ubuntubackup_202103.gz | sudo dd bs=10M of=/dev/sda status=progress
#こちらで実行
sudo dd if=/dev/mmcblk0 bs=10M of=/dev/sda status=progress
~~~
ソースカードのパーティション縮小  
~~~ 
sudo apt-get install gparted
sudo apt install gparted
~~~
gpartedを起動  
アンマウントしてリサイズをする  
![Test Image 1](ラズパイbackup画像/4.PNG)  

書き込みをする前に、SDカードをアンマウントする必要があります  
~~~ 
df -h
umount dev/sda2
sudo dd if=/dev/mmcblk0 bs=10M of=/dev/sda2 status=progress
sync
~~~
やり方を変える  
まずは先に外付けHDDにデータを保存  

~~~ 
sudo fdisk -l
#mmcblk0ここにラズパイ情報が入っているsdaが外付けハード
sudo dd if=/dev/mmcblk0 bs=20M of=/dev/sda status=progress

~~~
起動用sdカードを使用しバックアップｓｄカードを操作する
~~~ 
sudo fdisk -l
~~~
![Test Image 1](ラズパイbackup画像/5.PNG)  
gpartedを利用してパーテーションを縮小してapply 

![Test Image 1](ラズパイbackup画像/6.PNG)  
gpartedを利用別sdに保存するとラズパイが使えるようになる。

