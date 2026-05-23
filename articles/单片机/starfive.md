> 昉星光2折腾记录

# 更新固件

```bash
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

```bash
# linux环境下串口调试工具
sudo apt install tio

# 确认端口号，并提前将板子启动模式设置为(1, 1)(Flash模式)
sudo tio /dev/ttyUSB0 -b 115200

# 屏幕不断出现

```


# 烧录系统

```bash
# ubuntu
sudo dd if=./ubuntu-24.04.4-preinstalled-server-riscv64+jh7110.img of=/dev/sda bs=4M status=progress conv=fsync

# 官方镜像
sudo dd if=starfive-jh7110-202510-minimal-desktop-wayland.img of=/dev/sda bs=4M status=progress conv=fsync
```

```bash
# 创建临时挂载
sudo mkdir /mnt/temp_home
sudo mount /dev/mmcblk1p6 /mnt/temp_home

# 使用 rsync 确保权限一致
sudo rsync -avxHAWXS /home/ /mnt/temp_home/

# 手动设置挂载
sudo vi /etc/fstab

# 添加配置，将分区挂在到/home
/dev/mmcblk1p6  /home  ext4  defaults,noatime  0  2

# 刷新挂载
sudo mount -a

# Debian13使用system管理挂在任务，刷新systemd状态
sudo systemctl daemon-reload

# 查看磁盘空间，确认挂载情况
df -h /home

# 卸载临时挂载点
sudo umount /mnt/temp_home
sudo rmdir /mnt/temp_home

# 迁移数据，创建软链接(使用cp -ax更稳健)
sudo cp -ax /opt /home/extensions/opt
sudo rm -rf /opt
sudo ln -s /home/extensions/opt /opt

# 可迁移的目录: /opt, /var/cache/apt, /usr/local, /usr/share, /var/lib, /var/log, /usr/src

# 查看软链接
ls -l /opt
```
