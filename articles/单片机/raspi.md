[toc]

> 玩玩树莓派，简单记录常用命令、配置


## 无头模式调节终端字体

```
# 打开设置界面
sudo dpkg-reconfigure console-setup
```

依次选择:

- Encoding: UTF-8(保持默认)
- Character set: Combined - Latin; Slavic and Cyrillic; Greek
- Font: Terminus(必选)
- Font size: 16x32(最大尺寸)

## 换源

### rasp os换清华源

```shell
# /etc/apt/sources.list

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware
deb https://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware

# raspi.list

deb https://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ bookworm main
```

### ubuntu换清华源

清华源ubuntu-ports栏

```shell
Types: deb
URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
# Types: deb-src
# URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports
# Suites: noble noble-updates noble-backports
# Components: main restricted universe multiverse
# Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

# 以下安全更新软件源包含了官方源与镜像站配置，如有需要可自行修改注释切换
Types: deb
URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

# Types: deb-src
# URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports
# Suites: noble-security
# Components: main restricted universe multiverse
# Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

# 预发布软件源，不建议启用

Types: deb
URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports
Suites: noble-proposed
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

# Types: deb-src
# URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports
# Suites: noble-proposed
# Components: main restricted universe multiverse
# Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

## 下载桌面

```shell
sudo apt install xfce4
startxfce4

sudo apt install --no-install-recommends lxde
sudo apt install xorg lightdm

# 设置默认启动目标为图形界面
sudo systemctl set-default graphical.target
```

在烧录ubuntu24.04无头版本，下载桌面时始终无法启动xserver,
也许是ubuntu内核架构与raspi-config脚本在KMS管理上存在冲突，
放弃X11驱动，切换到wayland方案成功打开桌面

```shell
# 安装核心组件
sudo apt install labwc xwayland qtwayland5
# 配置LXQt在Wayland下运行
export QT_QPA_PLATFORM=wayland
labwc -s startlxqt


# 设置开机自动进入Wayland,使用sddm登录管理器
sudo apt install sddm

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
nmcli dev show      # 查看ip
nmcli dev status    # 查看网卡状况
```
