# -*- coding:utf-8 -*-
from machine import I2C,Pin
from servo import Servos

scl_pin = Pin(25)
sda_pin = Pin(26)
# 创建一个I2C对象
i2c = I2C(scl=scl_pin, sda = sda_pin, freq=10000)
# scan 得到的结果： [64, 112]
# PCA9685默认地址为0x40 = 64 
print(i2c.scan())

# 实例化一个舵机控制板(servo control board)
servos = Servos(i2c, address=0x40)
# 下方的舵机旋转角度范围： 0(左)-180（右）
# 上方的舵机旋转角度范围： 0(后)-180（前）  
servos.position(1, degrees=90)
