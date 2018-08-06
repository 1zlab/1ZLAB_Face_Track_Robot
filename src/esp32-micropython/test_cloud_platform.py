# -*- coding:utf-8 -*-
from cloud_platform import CloudPlatform
from machine import I2C,Pin

gpio_scl = 25
gpio_sda = 26

# 初始化I2C
scl_pin = Pin(gpio_scl)
sda_pin = Pin(gpio_sda)
i2c = I2C(scl=scl_pin, sda = sda_pin, freq=10000) # 创建I2C实例

# 创建一个云台对象 
cp = CloudPlatform(i2c, 0, 1)
