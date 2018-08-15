# -*- coding:utf-8 -*-
'''
PC上使用PySerial发送字节数据

运行此程序的时候，需要修改设备的权限，

sudo chmod 777 /dev/ttyUSB1
'''
import serial
import time
# 串口号 默认为 /dev/ttyUSB0
ser_dev = '/dev/ttyUSB1'

ser = serial.Serial(ser_dev,115200, timeout=1)

count = 1
MAX_NUM = 10
while True:
    
    info_str = 'INFO-%d\n'%(count)
    print(info_str)
    # 以字节的方式发出 编码方式，默认为UTF8 --ERROR
    # info_byte = bytes(info_str, encoding='utf8')

    info_byte = b'INFO-%d\n'%(count)

    # print("Byte : {}".format(info_byte))
    ser.write(info_byte) # 通过串口发送BYTE

    count = (count+1)%MAX_NUM    
    # 停顿一秒
    time.sleep(2)