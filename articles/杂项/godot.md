# 开发基础流程

个人理解为,每个Scene作为一个模块的封装,scene里设置一个根节点,需要什么功能都可以通过创建子节点实现,通过godot的检查器ui设置,或者通过绑定的脚本设置.每一个scene都可以当做一个可复用的节点,最后选定一个主场景,将所有内容组合运行.

# 基础函数介绍

```gdscript
# 先于_ready执行,只执行一次(用于执行节点初始化前的某些条件)
func _enter_tree() -> void:
	print("enter tree")

# 节点初始化执行一次
func _ready() -> void:
	print("hello")

# 每帧执行
func _process(delta: float) -> void:
	pass

# 按相同物理时间执行(不同设备帧率不同,但可以保持间隔物理时间相同)
func _physics_process(delta: float) -> void:
	pass

# 节点销毁时执行
func _exit_tree() -> void:
	pass
```
