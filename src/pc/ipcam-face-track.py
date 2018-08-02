# -*- coding:utf-8 -*-
'''
人脸识别并控制舵机进行人脸追踪

NOTE
1. 为保证人脸识别的帧率分辨率控制在320x240
TODO
1. 偏移量计算，得出人脸在画面中所占的百分比
2. 添加PID控制（纯比例控制其实就足够了）

'''
import cv2
import time
from uart_cloud_platform import set_cloud_platform_degree

# 最近一次底部舵机的角度值记录
last_btm_degree = 100
# 最近一次顶部舵机的角度值记录
last_top_degree = 100
# 舵机角度初始化
set_cloud_platform_degree(last_btm_degree, last_top_degree)


# 载入人脸检测的Cascade模型
FaceCascade = cv2.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')

# 创建一个窗口 名字叫做Face
cv2.namedWindow('FaceDetect',flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)


# 摄像头的IP地址  
# http://用户名：密码@IP地址：端口/
ip_camera_url = 'http://admin:admin@192.168.2.237:8081/'
# 创建一个VideoCapture
cap = cv2.VideoCapture(ip_camera_url)
# 设置缓存区的大小 !!!
cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
print('IP摄像头是否开启： {}'.format(cap.isOpened()))



def btm_servo_control(offset_x):
    '''
    这里舵机使用开环控制
    '''
    Kp = 0.1 # 控制舵机旋转的比例系数
    global last_btm_degree
    # offset范围在-50到50左右
    delta_degree = offset_x * Kp
    # 设置最小阈值
    if abs(delta_degree) < 1:
        delta_degree = 0
    
    next_btm_degree = last_btm_degree + delta_degree
    # 添加边界检测
    if next_btm_degree < 0:
        next_btm_degree = 0
    elif next_btm_degree > 180:
        next_btm_degree = 180
    
    return next_btm_degree

def top_servo_control(offset_y):
    '''
    这里舵机使用开环控制
    '''
    Kp = 0.1 # 控制舵机旋转的比例系数
    global last_top_degree
    # offset_y *= -1
    # offset范围在-50到50左右
    delta_degree = offset_y * Kp
    # 设置最小阈值
    if abs(delta_degree) < 1:
        delta_degree = 0
    
    next_top_degree = last_top_degree + delta_degree
    # 添加边界检测
    if next_top_degree < 0:
        next_top_degree = 0
    elif next_top_degree > 180:
        next_top_degree = 180
    
    return next_top_degree

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
    '''
    (x, y, w, h) = face
    face_x = float(x + w/2.0)
    face_y = float(y + h/2.0)
    # 人脸举例
    offset_x = int(float(face_x / img_width - 0.5) * 100)
    offset_y = int(float(face_y / img_height - 0.5) * 100)
    # offset_x = face_x - img_width/2
    # offset_y = face_y - img_height/2

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

    key = cv2.waitKey(1)
    if key == ord('q'):
        # 退出程序
        break
    elif key == ord('r'):
        print('舵机重置')
        # 重置电机
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