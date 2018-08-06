# -*- coding:utf-8 -*-

'''
二自由度云台
2DOF
'''
from machine import I2C,Pin
from servo import Servos

class CloudPlatform(object):
    def __init__(self, i2c, btm_servo_idx, top_servo_idx):
        '''
        PCA9685与ESP32之间通过I2C相连接
        @gpio_scl ： I2C的SCL管脚GPIO编号
        @gpio_sda : I2C的SDA管脚的GPIO编号
        @btm_servo_idx: 云台下方舵机在PCA9685上面的编号
        @top_servo_idx: 云台上方电机在PCA9695上面的编号
        '''
        

        self.servos = Servos(i2c, address=0x40) # 实例化一个舵机控制板(servo control board)
        self.btm_servo_idx = btm_servo_idx # 底部舵机的编号
        self.top_servo_idx = top_servo_idx # 云台上方舵机的编号
        self.btm_min_angle = 0 # 底部舵机最小旋转角度
        self.btm_max_angle = 180 # 底部舵机最大旋转角度
        self.btm_init_angle = 100 # 底部舵机的初始角度
        self.top_min_angle = 0 # 顶部舵机的最小旋转角度
        self.top_max_angle = 180 # 顶部舵机的最大旋转角度
        self.top_init_angle = 100 # 顶部舵机的初始角度

        # 初始化云台角度
        self.init_cloud_platform()

    def set_btm_servo_angle(self, degree):
        '''
        设定云台底部舵机的角度
        '''
        if degree < self.btm_min_angle:
            degree = self.btm_min_angle
        elif degree > self.btm_max_angle:
            degree = self.btm_max_angle
        
        self.servos.position(self.btm_servo_idx, degrees=degree)

    def set_top_servo_angle(self, degree):
        '''
        设定云台顶部舵机的角度
        '''
        if degree < self.top_min_angle:
            degree = self.top_min_angle
        elif degree > self.top_max_angle:
            degree = self.top_max_angle
        
        self.servos.position(self.top_servo_idx, degrees=degree)

    def init_cloud_platform(self):
        self.set_btm_servo_angle(self.btm_init_angle)
        self.set_top_servo_angle(self.top_init_angle)

