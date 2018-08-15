# -*- coding:utf-8 -*-
'''
人脸识别并控制舵机进行人脸追踪

NOTE
1. 为保证人脸识别的帧率分辨率控制在320x240
BUG
1. 刚开始的时候缓存区视频流的问题， 导致舵机云台会乱转 向大佬低头  数值越界
ESP32出解析的数据：Bottom: 6553600 Top: 6556160
2. Reset 舵机云台，串口数据发送之后，ESP32有时候不执行
TODO
1. 获得舵机旋转角度的反馈数据
2. 创建两个Trackbar， 设置两个Kp取值
3. 绘制上下臂舵机的波形图

参考Kp取值
1. Kp = 10  比例系数较大，来回抖动非常明显
2. Kp = 20  幅度过大，旋转后目标直接丢失
3. Kp = 5   幅度适中，有小幅抖动
4. Kp = 2   相应速度比较慢
'''
import cv2
import time
from uart_cloud_platform import set_cloud_platform_degree

last_btm_degree = 100 # 最近一次底部舵机的角度值记录
last_top_degree = 100 # 最近一次顶部舵机的角度值记录

btm_kp = 5 # 底部舵机的Kp系数
top_kp = 5 # 顶部舵机的Kp系数

offset_dead_block = 0.1 # 设置偏移量的死区

# 舵机角度初始化
set_cloud_platform_degree(last_btm_degree, last_top_degree)

# 载入人脸检测的Cascade模型
FaceCascade = cv2.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')

# 创建一个窗口 名字叫做Face
cv2.namedWindow('FaceDetect',flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)

def update_btm_kp(value):
    # 更新底部舵机的比例系数
    global btm_kp
    btm_kp = value

def update_top_kp(value):
    # 更新顶部的比例系数
    global top_kp
    top_kp = value

# 创建底部舵机Kp的滑动条
cv2.createTrackbar('BtmServoKp','FaceDetect',0, 20,update_btm_kp)
# 设置btm_kp的默认值
cv2.setTrackbarPos('BtmServoKp', 'FaceDetect', btm_kp)
# 创建顶部舵机Kp的滑动条
cv2.createTrackbar('TopServoKp','FaceDetect',0, 20,update_top_kp)
# 设置top_kp的默认值
cv2.setTrackbarPos('TopServoKp', 'FaceDetect', top_kp)


# 摄像头的IP地址  
# http://用户名：密码@IP地址：端口/
ip_camera_url = 'http://admin:admin@192.168.43.1:8081/'
# 创建一个VideoCapture
cap = cv2.VideoCapture(ip_camera_url)
# 设置缓存区的大小 !!!
cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
print('IP摄像头是否开启： {}'.format(cap.isOpened()))



def btm_servo_control(offset_x):
    '''
    底部舵机的比例控制
    这里舵机使用开环控制
    '''
    global offset_dead_block # 偏移量死区大小
    global btm_kp # 控制舵机旋转的比例系数
    global last_btm_degree # 上一次底部舵机的角度
    
    # 设置最小阈值
    if abs(offset_x) < offset_dead_block:
       offset_x = 0

    # offset范围在-50到50左右
    delta_degree = offset_x * btm_kp
    # 计算得到新的底部舵机角度
    next_btm_degree = last_btm_degree + delta_degree
    # 添加边界检测
    if next_btm_degree < 0:
        next_btm_degree = 0
    elif next_btm_degree > 180:
        next_btm_degree = 180
    
    return int(next_btm_degree)

def top_servo_control(offset_y):
    '''
    顶部舵机的比例控制
    这里舵机使用开环控制
    '''
    global offset_dead_block
    global top_kp # 控制舵机旋转的比例系数
    global last_top_degree # 上一次顶部舵机的角度

    # 如果偏移量小于阈值就不相应
    if abs(offset_y) < offset_dead_block:
        offset_y = 0

    # offset_y *= -1
    # offset范围在-50到50左右
    delta_degree = offset_y * top_kp
    # 新的顶部舵机角度
    next_top_degree = last_top_degree + delta_degree
    # 添加边界检测
    if next_top_degree < 0:
        next_top_degree = 0
    elif next_top_degree > 180:
        next_top_degree = 180
    
    return int(next_top_degree)

def face_filter(faces):
    '''
    对人脸进行一个过滤
    '''
    if len(faces) == 0:
        return None
    
    # 目前找的是画面中面积最大的人脸
    max_face =  max(faces, key=lambda face: face[2]*face[3])
    (x, y, w, h) = max_face
    if w < 10 or h < 10:
        return None
    return max_face

def calculate_offset(img_width, img_height, face):
    '''
    计算人脸在画面中的偏移量
    偏移量的取值范围： [-1, 1]
    '''
    (x, y, w, h) = face
    face_x = float(x + w/2.0)
    face_y = float(y + h/2.0)
    # 人脸在画面中心X轴上的偏移量
    offset_x = float(face_x / img_width - 0.5) * 2
    # 人脸在画面中心Y轴上的偏移量
    offset_y = float(face_y / img_height - 0.5) * 2

    return (offset_x, offset_y)

while cap.isOpened():
    # TODO 阅读最后一帧
    ret, img = cap.read()
    # 手机画面水平翻转
    img = cv2.flip(img, 1)
    # 将彩色图片转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 检测画面中的人脸
    faces = FaceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )
    # 人脸过滤
    face = face_filter(faces)
    if face is not None:
        # 当前画面有人脸
        (x, y, w, h) = face
        # 在原彩图上绘制矩形
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 4)

        img_height, img_width,_ = img.shape
        print("img h:{} w:{}".format(img_height, img_width))
        # 计算x轴与y轴的偏移量
        (offset_x, offset_y) = calculate_offset(img_width, img_height, face)
        # 计算下一步舵机要转的角度
        next_btm_degree = btm_servo_control(offset_x)
        next_top_degree = top_servo_control(offset_y)
        # 舵机转动
        set_cloud_platform_degree(next_btm_degree, next_top_degree)
        # 更新角度值
        last_btm_degree = next_btm_degree
        last_top_degree = next_top_degree
        print("X轴偏移量：{} Y轴偏移量：{}".format(offset_x, offset_y))
        print('底部角度： {} 顶部角度：{}'.format(next_btm_degree, next_top_degree))
    # 在窗口Face上面展示图片img
    cv2.imshow('FaceDetect', img)
    # 等待键盘事件
    key = cv2.waitKey(1)
    if key == ord('q'):
        # 退出程序
        break
    elif key == ord('r'):
        print('舵机重置')
        # 重置舵机
        # 最近一次底部舵机的角度值记录
        last_btm_degree = 100
        # 最近一次顶部舵机的角度值记录
        last_top_degree = 100
        # 舵机角度初始化
        set_cloud_platform_degree(last_btm_degree, last_top_degree)

# 释放VideoCapture
cap.release()
# 关闭所有的窗口
cv2.destroyAllWindows()
