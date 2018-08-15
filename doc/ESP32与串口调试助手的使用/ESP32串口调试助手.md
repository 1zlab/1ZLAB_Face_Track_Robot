## 串口调试工具

> TODO ESP32收发历程+串口调试助手



串口调试工具可以方便我们测试串口通信的收发的功能。 在进行串口调试的时候，你需要使用USB转TTL将ESP32连接到PC上面，电脑会给其分配一个端口号。

### cutecom

在Ubuntu上进行串口调试，可以借助**CuteCom**



首先需要安装CuteCom

```
sudo apt-get install cutecom
```


以管理员的权限 运行cutecom
```
sudo cutecom
```

或者需要修改USB设备的权限
```
sudo chmod 777 /dev/ttyUSB1
```



运行cutecom之后，需要手动修改设备名称， 
在`Device`输入框里面，将设备编号修改为：

` /dev/ttyUSB1`






http://blog.csdn.net/jiangchao3392/article/details/73740841



