'''
串口发送信息 （字符chuan）
接线：
    ESP32,TDX,D12 -> RXD,CP2102 (USB转TTL)
    ESP32,RXD,D13 -> TXD,CP2102 (USB转TTL)
'''

from machine import UART,Pin
import utime

# 初始化串口 UART
# 波特率 115200
# rx -> Pin 13
# tx -> Pin 12

uart = UART(2, baudrate=115200, rx=13,tx=12,timeout=10)
while True:
    # 句子后面需要添加结束符\n
    # 以方便PC上进行数据解析
    # uart.write("Fange: HelloWorld\r\n")
    uart.write("hello\n")
    # 时间间隔1s
    utime.sleep_ms(100)