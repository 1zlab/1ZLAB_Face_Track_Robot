# IP摄像头APP的使用说明-1Z实验室



## 概要

本节课阿凯给大家讲解了如何使用IP摄像头APP，将你的手机变成IP摄像头，同时介绍了如何使用OpenCV读取IP摄像头的视频流。

出品：1Z实验室 （1ZLAB： Make Things Easy）



## 目录

* [1-下载IP摄像头APP](#1-下载IP摄像头APP)
* [2-局域网](#2-局域网)
* [3-运行APP](3-运行APP)
* [4-在网页中预览视频流](#4-在网页中预览视频流)
* [5-OpenCV读取视频流](#5-OpenCV读取视频流)
* [6-设置VideoCapture的缓存区大小](#6-设置VideoCapture的缓存区大小)





## 1-下载IP摄像头APP

在你手机的应用市场里面搜索这款名字叫做**IP摄像头**的APP, 图标就是下面这样的：

![IP摄像头](./image/ipcamera.png)

> PS1: 这款APP是有广告的注意不要乱点广告，略影响用户体验。

> TODO 有没有可能我们开发一个性能更好的APP 

## 2-局域网

需要确定你的手机与电脑处在同一个局域网下，即他们连接同一个WIFI。



## 3-运行APP

点击运行**IP摄像头**APP ， 点击下方的**打开IP摄像头服务器** 的选项。![0811_1](./image/0811_1.png)





是否继续，点击**确定**

![0811_2](./image/0811_2.png)

服务器开启之后，会提示你这个视频流服务器在局域网中的IP还有端口号。 

![0811_3](./image/0811_3.png)



在当下的url是

```
http://192.168.43.1:8081
```

**在没有客户端连接的时候，你可以点击右上角设置画面的分辨率。**

可以点击**切换** 选择使用前置摄像头还是后置摄像头。



## 4-在网页中预览视频流

在浏览器中输入地址

```
http://192.168.43.1:8081
```



![IPCAMERA-admin](./image/IPCAMERA-admin.png)

接下来就需要填入用户名跟密码，默认为：

```
用户名： admin
密码： admin
```



下方有很多工具栏， 你可以设定图像的分辨率，快照等一系列操作。

![图图片ip cam](./image/ip-cam.png)



## 5-OpenCV读取视频流

如果我们像进行图像处理，就必须读取到IP摄像头提供的视频流，通信协议为http。

核心代码就两行 

```python
# 制定URL  http://用户名：密码@IP地址：端口号/
ip_camera_url = 'http://admin:admin@192.168.43.1:8081/'
# 创建一个VideoCapture
cap = cv2.VideoCapture(ip_camera_url)
```

> TODO ? Windows下要怎么做

IP需要自己修改， 端口号默认为8081

完整代码如下：

`ipcam-cap.py`

```python
# -*- coding: utf-8 -*- 
'''
读取手机摄像头的视频流

1. 手机与电脑链接同一个WIFI热点
2. 需要sudo权限：
sudo python  ipcam-cap.py
'''
import cv2
import time

ip_camera_url = 'http://admin:admin@192.168.2.237:8081/'
# 创建一个窗口
cv2.namedWindow('ip_camera', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)

cap = cv2.VideoCapture(ip_camera_url)

if not cap.isOpened():
    print('请检查IP地址还有端口号，或者查看IP摄像头是否开启，另外记得使用sudo权限运行脚本')

while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('ip_camera', frame)


    if cv2.waitKey(1) == ord('q'):
        # 退出程序
        break

cv2.destroyWindow('ip_camera')
cap.release()
```



**代码必须使用管理员权限运行**

```bash
sudo python  ipcam-cap.py
```



运行代码，初始化需要一段时间。

不出意外的话， 你可以看到下面的这个窗口。

![ipcamera-demo](./image/ipcamera-demo.png)



## 6-设置VideoCapture的缓存区大小

有时候，如果你在OpenCV中做图像处理的时候，如果图像处理比较耗时，就导致存在VideoCapture缓存区的图像队列越积越多。 你就会发现延时好高啊，过了半天画面才更新，实际的画面与VideoCapture的实际画面时差越拉越大。

**这个问题，可以通过缩小缓冲区尺寸来解决。**

`cap.set`  设定VideoCapture的各种属性，这里指定缓冲区的尺寸为1：

```
cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
```



完整一些的代码片段：

```python
# 摄像头的IP地址  
# http://用户名：密码@IP地址：端口/
ip_camera_url = 'http://admin:admin@192.168.2.237:8081/'
# 创建一个VideoCapture
cap = cv2.VideoCapture(ip_camera_url)
# 设置缓存区的大小 !!!
cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
```



## 推广

出品：1Z实验室 （1ZLAB： Make Things Easy）

1Z实验室 Make Things Easy .  致力于在机器人+计算机视觉+人工智能的重叠区域, 制作小白友好的教程. 



![ad](./image/ad.png)