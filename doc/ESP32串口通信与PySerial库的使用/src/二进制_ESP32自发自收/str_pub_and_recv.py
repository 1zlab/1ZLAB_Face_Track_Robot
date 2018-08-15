'''
ESP32串口通信-字符串数据自发实验

接线 将开发板的 13号引脚与12号引脚用杜邦线相连接。

'''
from machine import UART,Pin
import utime

# 初始化一个UART对象
uart = UART(2, baudrate=115200, rx=13,tx=12,timeout=10)

count = 1

while True:
    print('\n\n===============CNT {}==============='.format(count))

    # 发送一条消息
    print('Send: {}'.format('hello {}\n'.format(count)))
    print('Send Byte :') # 发送字节数
    uart.write('hello {}\n'.format(count))
    # 等待1s钟
    utime.sleep_ms(1000)

    if uart.any():
        # 如果有数据 读入一行数据返回数据为字节类型
        # 例如  b'hello 1\n'
        bin_data = uart.readline()
        # 将手到的信息打印在终端
        print('Echo Byte: {}'.format(bin_data))

        # 将字节数据转换为字符串 字节默认为UTF-8编码
        print('Echo String: {}'.format(bin_data.decode()))
    # 计数器+1
    count += 1
    print('---------------------------------------')