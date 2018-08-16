# 舵机云台人脸追踪-1Z实验室



出品：1Z实验室 （1ZLAB： Make Things Easy）

关键词： `MicroPython-ESP32` ， `Python-OpenCV`， `人脸检测` `Face Detection`， `人脸追踪` `Face Trak`



## 项目介绍

首先是使用一款名字叫做[IP摄像头的APP](https://www.jianshu.com/p/0586d7dad113) 采集手机摄像头的图像，在手机上建立一个**视频流服务器**。在局域网下，PC通过IP还有端口号获取图像。使用OpenCV的[人脸检测](https://github.com/1zlab/1ZLAB_OpenCV_Face_Detection)的API获取人脸在画面中的位置，根据人脸位置距离画面中心的x轴与y轴的**偏移量(offset)** ，通过**P比例控制(PID控制中最简单的一种)**控制二自由度云台上臂与下臂的旋转角度，将角度信息通过[串口通信UART](https://www.jianshu.com/p/d6f43875bfe1)发送给**ESP32单片机**(不限于ESP32，STM32,Arduino都可以)解析执行对应的操作，从而使得人脸**尽可能处在画面的正中间**。



![人脸追踪](https://upload-images.jianshu.io/upload_images/1199728-000705266d8960dd.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)



## 课程目录



![人脸追踪](https://upload-images.jianshu.io/upload_images/1199728-b36f9fc558602b30.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)

> TODO 添加视频链接

**追踪算法**

[人脸追踪-舵机云台比例控制-1Z实验室](https://www.jianshu.com/p/ed8f0c748050)

**图像处理**

[IP摄像头APP与OpenCV视频流读取-1Z实验室](https://www.jianshu.com/p/0586d7dad113)

[OpenCV人脸检测-1Z实验室](https://github.com/1zlab/1ZLAB_OpenCV_Face_Detection)

[B站视频【OpenCV基础教程】2.人脸检测初探（1Z实验室）](https://www.bilibili.com/video/av28774187?from=search&seid=17832170123663965893)



**MicroPython-ESP32**

[MicroPython-ESP32固件烧录-1Z实验室](https://www.jianshu.com/p/699e8350b753)

[用ESP32-MicroPython点亮一个LED-1Z实验室](https://www.jianshu.com/p/a25bc059ea1c)

[MicroPython-ESP32串口通信-1Z实验室](https://www.jianshu.com/p/d6f43875bfe1)

[PCA9685舵机控制板与MicroPython-ESP32-1Z实验室](https://www.jianshu.com/p/b2a6306e583d)



**零配件采购参考**

[舵机云台人脸追踪-零配件采购手册-1Z实验室](https://www.jianshu.com/p/dafc8257ac90)



## 推广

出品：1Z实验室 （1ZLAB： Make Things Easy）

1Z实验室 Make Things Easy .  致力于在机器人+计算机视觉+人工智能的重叠区域, 制作小白友好的教程.



![wechat](https://upload-images.jianshu.io/upload_images/1199728-d5b70e9fe807b390.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)



![qq](https://upload-images.jianshu.io/upload_images/1199728-b57eb90afb54f4f8.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)