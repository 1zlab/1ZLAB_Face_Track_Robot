# -*- coding:utf-8 -*-
'''
功能描述
    串口解析信息 二进制数据 获取的舵机云台的角度
    然后执行命令，舵机旋转对应的角度

接线：

1.USB转TTL模块
    ESP32,TDX,D19 -> RXD,USB转TTL
    ESP32,RXD,D18 -> TXD,USB转TTL
2.PCA9685(I2C舵机驱动板)
    ESP32,SCL，D25 -> PCA9685,SCL 
    ESP32,SDA, D26 -> PCA9685,SDA
'''
from machine import UART,Pin,I2C
import struct
import utime
import micropython
from cloud_platform import CloudPlatform

# UART串口通信协议的长度
uart_protocal_len = 9

# PCA9685模块的I2C接口接线
gpio_scl = 25
gpio_sda = 26

# 初始化I2C
scl_pin = Pin(gpio_scl)
sda_pin = Pin(gpio_sda)
i2c = I2C(scl=scl_pin, sda = sda_pin, freq=10000) # 创建I2C实例
# 创建一个云台对象 
cp = CloudPlatform(i2c, 0, 1)

# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)
# 初始化UART对象
uart = UART(2, baudrate=115200, rx=18,tx=19,timeout=10)


def depack_bin_data(byte_raw):
    '''
    将数据解包
        根据通信协议，解析数据， 并校验帧头
    '''
    global uart_protocal_len

    print('len: {}'.format(len(byte_raw)))
    if len(byte_raw) != uart_protocal_len:
        # 检查数据帧长度是否满足条件
        raise ValueError("ERROR: 长度不满足条件")
    
    (bottom_degree, top_degree, _) = struct.unpack('>iiB', byte_raw)
    return (bottom_degree, top_degree)



while True:
    if uart.any() < uart_protocal_len:
        # 如果缓存区不满9,就继续等待
        continue

    if uart.any():
        byte_raw = uart.read(uart_protocal_len)
        # print(byte_raw)
        # print(len(byte_raw))
        # 讲接收的字节流转换成容易读取的样式
        # byte_str = ':'.join(['{:02x}'.format(char_byte) for char_byte in byte_raw])
        try:
            (bottom_degree, top_degree) = depack_bin_data(byte_raw)
            # 舵机云台执行相关动作
            cp.set_btm_servo_angle(bottom_degree)
            cp.set_top_servo_angle(top_degree)
            print("Bottom: {} Top: {}".format(bottom_degree, top_degree))
        except ValueError as e:
            print('Error: {}'.format(e))
        # print(byte_raw)

    utime.sleep_ms(10)

