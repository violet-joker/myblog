[toc]

> 玩玩树莓派，简单记录常用命令、配置

## 换源

```shell
# /etc/apt/sources.list

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware
deb https://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware

# raspi.list

deb https://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ bookworm main
```

## 下载桌面

```shell
sudo apt install xfce4
startxfce4

sudo apt install --no-install-recommends lxde
sudo apt install xorg lightdm
```

## 配置中文系统环境

安装中文语言包

```shell
sudo apt install language-pack-zh-hans
```

添加中文语言

```shell
sudo dpkg-reconfigure locales
```


## 安装opencv

参考官方指导[How To Install OpenCV on Ubuntu 24.04 LTS - idroot](https://idroot.us/install-opencv-ubuntu-24-04/)

```shell
sudo apt install libopencv-dev python3-opencv
```

## vnc

```shell
sudo apt install tightvncserver
```

启用vncserver端口1，

```shell
vncserver :1
export DISPLAY=:1
startxfce4
```

## 树莓派5，关闭5v5a电流启动检测：

修改
```shell
sudo vi /boot/firmware/config.txt

# 添加
usb_max_current_enable=1
```

## 安装zsh

```shell
sudo apt install zsh
chsh -s /bin/zsh
echo $SHELL
```

## 命令行连接wifi

```shell
nmcli dev wifi list
nmcli dev wifi connect "SSID名称" password "密码"
```
