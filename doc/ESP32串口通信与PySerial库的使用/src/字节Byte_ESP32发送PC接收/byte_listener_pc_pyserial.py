# -*- coding:utf-8 -*-
'''
PC上使用PySerial解析数据
接收byte字节数据

运行此程序的时候，需要修改设备的权限，

sudo chmod 777 /dev/ttyUSB1

'''
import serial

# 串口号 默认为 /dev/ttyUSB0
ser_dev = '/dev/ttyUSB1'


''' 
# 执行一次
with  serial.Serial(ser_dev,115200, timeout=1) as ser:
    print(ser)
    info = ser.readline()
    print(info)
'''

ser = serial.Serial(ser_dev,115200, timeout=1)

while True:
    # 读取的是byte类型 ，例如
    #　b'hello\n'
    # ser.read() # 读取单个字节
    # ser.read(n) # 读入N个字节
    info = ser.readline() # 读入一行数据
    
    # 打印接收的数据
    print(info)