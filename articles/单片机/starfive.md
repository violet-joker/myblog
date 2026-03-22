> 昉星光2折腾记录

# 更新固件

```shell
# 烧录的官方最小系统，/目录下空间不够，可删除帮助文档腾一点空间
sudo rm -rf /usr/share/doc/*

apt install mtd-utils

# 查看编号以及内存表
cat /proc/mtd

# 1. 写入 SPL (至 mtd0)
sudo flashcp -v u-boot-spl.bin.normal.out /dev/mtd0

# 2. 写入 U-Boot (至 mtd1)
sudo flashcp -v visionfive2_fw_payload.img /dev/mtd1
```

固件初始内存不够，使用usb串口转换器烧录固件

```shell
# linux环境下串口调试工具
sudo apt install tio

# 确认端口号，并提前将板子启动模式设置为(1, 1)(Flash模式)
sudo tio /dev/ttyUSB0 -b 115200

# 屏幕不断出现

```
