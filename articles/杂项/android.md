[toc]

> linux环境下,命令行构建android项目

# andrud工具

```bash
npm install -g andrud
andrud --help
# 使用andrud即可快速构建android项目模板
andrud create
```

# SDL3 on android

使用andrud仅仅能构建最基础的模板,MainActivity.java仍需手动实现,而SDL3提供的模板已经完成了相关实现.

```bash
# 拉取SDL3源码
git clone https://github.com/libsdl-org/SDL.git
cp SDL/android-project ~/Projects/my_android_project
cd ~/Projects/my_android_project/app/jni
# 在app/jni目录下创建软链接/或者复制源码到该目录
ln -s /path/SDL SDL
# 回到项目根目录,使用gradlew脚本打包apk
./gradew assemble

# 第一次会自动下载所需的gradle版本,换源加速下载
vim gradle/wrapper/gradle-wrapper.properties
# 注释掉原来的源,使用腾讯云镜像
# distributionUrl=https\://services.gradle.org/distributions/gradle-8.12-bin.zip
distributionUrl=https\://mirrors.cloud.tencent.com/gradle/gradle-8.12-bin.zip

# 打包完成后,生成的apk文件在app/build/outpus目录下
# release版尚未签名,可以安装测试debug.apk
waydroid app install app-debug.apk
```

SDL3源码里有写好的Android.mk文件,通过Android.mk构建十分方便,然而许多第三方库没有Android.mk文件,可预先编译好android平台的动态库,复制过来即可.

```bash
# 预先编译好SDL库,将头文件和动态库文件复制到jni目录下,编写jni/src/Android.mk文件:

LOCAL_PATH := $(call my-dir)

#================== 声明预编译的动态库 =====================
include $(CLEAR_VARS)
LOCAL_MODULE := SDL3
LOCAL_SRC_FILES := $(LOCAL_PATH)/../SDL/lib/$(TARGET_ARCH_ABI)/libSDL3.so
include $(PREBUILT_SHARED_LIBRARY)
#===========================================================

include $(CLEAR_VARS)
# 将cpp项目编译成libmain.so,SDL将main作为程序入口
LOCAL_MODULE := main
LOCAL_SRC_FILES := main.cpp

LOCAL_C_INCLUDES := $(LOCAL_PATH)/../SDL/include

LOCAL_SHARED_LIBRARIES := SDL3
LOCAL_LDLIBS := -lGLESv1_CM -lGLESv2 -lOpenSLES -llog -landroid

include $(BUILD_SHARED_LIBRARY)
```

```bash
# 在app目录下创建jniLibs目录,将动态库so文件复制到该目录下自动打包
# 预编译的动态库需要与项目使用的c++标准一致,否则出现"找不到libc++_shared.so"错误
vim app/jni/Application.mk

APP_STL := c++_shared
# 目前仅在pc的waydroid上进行调试,所以选择的x86_64架构
# 需与app/build.gradle的externalNativeBuild配置一致
# abiFilters 'armeabi-v7a', 'arm64-v8a', 'x86', 'x86_64'
APP_ABI := x86_64
APP_PLATFORM=android-21
APP_CPPFLAGS += -std=c++23
```

# 预编译第三方库,生成指定架构的动态库文件

```bash
# 需提前配置好ndk环境变量,使用ndk编译
# 定义架构变量（只需修改这一行）
# 可选: armeabi-v7a, arm64-v8a, x86, x86_64
# ABI=x86
# ABI=x86_64
# ABI=armeabli-v7a
ABI=arm64-v8a

# 构建目录
BUILD_DIR="build-android-${ABI}"

# 创建并进入构建目录
mkdir -p ${BUILD_DIR} && cd ${BUILD_DIR}

# CMake 配置
cmake .. \
    -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
    -DANDROID_ABI=${ABI} \
    -DANDROID_PLATFORM=android-21 \
    -DANDROID_STL=c++_shared \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=~/android_libs/${ABI} \
    -DBUILD_SHARED_LIBS=ON

make -j8
make install
cd ..
```
rmlui依赖freetype字体库,需先编译好对应平台的freetype文件,并手动设置路径

```bash
cmake .. \
    -DFREETYPE_INCLUDE_DIRS=/home/xf/android_libs/${ABI}/include/freetype2 \
    -DFREETYPE_LIBRARY=/home/xf/android_libs/${ABI}/lib/libfreetype.so
```
