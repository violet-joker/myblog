# 最简单的内核模块

```c
#include <linux/module.h>

static int __init hello_init(void)
{
    printk(KERN_INFO "hello linux module!\n");
    return 0;
}

static void __exit hello_exit(void)
{
    printk(KERN_INFO "hello module exit\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("Dual BSD/GPL");
MODULE_AUTHOR("xf");
```

```make
KERNELDIR   ?= /lib/modules/$(shell uname -r)/build
PWD         := $(shell pwd)
obj-m       := hello.o

all:
    make -C $(KERNELDIR) M=$(PWD) modules
clean:
    rm -rf *.o  core .depend .*.cmd *.mod.c *.mod *.order *.symvers
```

```bash
lsmod
dmesg
sudo insmod hello.ko
sudo rmmode hello.ko
```

# 内核模块参数和导出符号

```c
#include <linux/module.h>

static int cnt = 1;
extern char *p = "hello world\n";
static int arr[] = {1, 2, 3, 4, 5, 6};
static int nums = sizeof(arr) / sizeof(int);

// 模块参数，声明变量名称、类型、权限位
module_param(cnt, int, S_IRUGO);
module_param(p, charp, S_IRUGO);
module_param_array(arr, int, &nums, S_IRUGO);

void prt(void)
{
    printk(KERN_INFO "this is hello module\n");
}

static int __init hello_init(void)
{
    for (int i = 0; i < cnt; i++)
        printk(KERN_INFO "%d:%s", i, p);
    for (int i = 0; i < nums; i++)
        printk(KERN_INFO "%d\n", arr[i]);
    
    return 0;
}

static void __exit hello_exit(void)
{
    printk(KERN_INFO "hello module exit\n");
}

module_init(hello_init);
module_exit(hello_exit);

// 模块导出，供其他模块使用
EXPORT_SYMBOL(p);
EXPORT_SYMBOL(prt);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("xf");
```

```bash
sudo insmod hello.ko cnt=3 p=fine,world arr=3,2,1
```

```c
#include <linux/module.h>

// 依赖hello模块中的p和ptr
extern char *p;
extern void ptr(void);

static int __init printp_init(void)
{
    printk(KERN_INFO "printp:%s\n", p);
    prt();
    return 0;
}

static void __exit printp_exit(void)
{

}

module_init(printp_init);
module_exit(printp_exit);

MODULE_LICENSE("GPL");
```

# 分配设备号，字符设备&块设备


