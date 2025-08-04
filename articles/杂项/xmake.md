模板

```c++
add_rules("mode.debug", "mode.release")

target("main")
    -- 目标文件类型
    set_kind("binary")
    -- 所要编译的文件
    add_files("src/*.cpp")
    -- 设置工具链
    set_toolchains("clang")
    -- 设置目标文件输出路径
    set_targetdir("build/release")
    -- 设置成静态链接(默认使用动态链接)
    add_ldflags("-static")
    -- 设置编译平台
    set_plat("linux")
    -- 设置系统架构
    set_arch("arm")
```

设置debug模式，编译出可调式文件

```lua
xmake f -m debug
xmake f -m release
```

导出cmake文件

```lua
xmake project -k cmakelists
```

添加第三方库

```lua
add_reauires("imgui", {configs = {glfw_opengl3 = true}})

target("imgui-demo")
    -- ...
    add_packages("imgui")
```


设置编译平台

```lua
-- -p 平台 -a 架构
xmake f -p linux -a arm64
```

## 配置树莓派工具链

```lua

add_rules("mode.release")

toolchain("raspi")
    set_kind("standalone")
    set_toolset("cc", "arm-linux-gnueabihf-gcc")
    set_toolset("cxx", "arm-linux-gnueabihf-g++")
    set_toolset("ld", "arm-linux-gnueabihf-g++")

target("main")
    set_kind("binary")
    add_files("main.cpp")
    set_toolchains("raspi")
    set_targetdir("./")
    set_plat("linux")
    set_arch("arm") 
    add_ldflags("-static")
```
