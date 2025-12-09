# Permission denied

```shell
avrdude: ser_open(): can't open device "/dev/ttyACM0": Permission denied
Failed uploading: uploading error: exit status 1
```

大多数linux发行版使用dialout组来管理串口访问权限，将用户添加到
dialout组，重启生效。

```shell
sudo usermod -a -G dialout $USER
```

# 点亮板载led

```c++
void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
```

# 模拟Xbox手柄

## 添加第三方板卡(ArduinoXInput_AVR)

在IDE首选项，开发板管理器地址添加https://raw.githubusercontent.com/dmadison/ArduinoXInput_Boards/master/package_dmadison_xinput_index.json

"开发板管理器"里下载XInput AVR Boards

"选择其他开发板和接口"选择XInput相关开发板

烧录成USB HID设备后不再以传统arduino串口方式工作，无法再通过常规方式
上传程序，需要让板子进入"bootloader"模式:按下复位键，点击烧录，当IDE
编译完代码，进入上传阶段时松开复位键。(时机不好掌握，多试几次)

## 添加软件库(XInput)

```c++
#include <XInput.h>

void setup() {
    XInput.begin();
}

void loop() {
    XInput.press(BUTTON_A);
    delay(1000);
    XInput.release(BUTTON_A);

    for (int i = 0; i < 255; i++) {
        XInput.setTrigger(TRIGGER_LEFT, i);
        delay(10);
    }
}
```

## 连接编码器(520编码器)

### 编码器相关原理

增量式编码器，将位移转换成周期性电信号，再将电信号转变成计数脉冲，
用脉冲个数表示位移大小。

转动电机，AB电平波形出现相位差，正转A相领先90度，反转B相领先90度；
根据AB相位触发的状态是否相同以及触发中断的相，判断正反转。

```
// 以正转为例
时间轴:     t0 --- t1 --- t2 --- t3
A相:        低-----高-----低-----高
B相:          低-----高-----低-----高
```

每一次边沿转换触发一次中断；产生一个物理脉冲需要两次终端(上升沿+下降沿)

物理旋转角度 = (脉冲数 / PPR) x 360° (PPR为编码器分辨率(脉冲/圈))

编码器连接：

- 红:电机电源+
- 黑:编码器电源-
- 黄:信号线 电机一圈11个脉冲
- 绿:信号线 分辨率11*减速比=分辨率
- 蓝:编码器电源+
- 白:电机电源-

### 代码

```c++
// 使用D2、D3引脚触发中断
#define A_PIN 2
#define B_PIN 3
int cnt;

void interruptA() {
    int state_a = digitalRead(A_PIN);
    int state_b = digitalRead(B_PIN);

    if (state_a != state_b)
        cnt++;
    else
        cnt--;
}

void interruptB() {
    int state_a = digitalRead(A_PIN);
    int state_b = digitalRead(B_PIN);

    if (state_a == state_b)
        cnt++;
    else
        cnt--;
}

void setup() {
    // 上升沿和下降沿都触发中断
    attachInterrupt(digitalPinToInterrupt(A_PIN), interruptA, CHANGE);
    attachInterrupt(digitalPinToInterrupt(B_PIN), interruptB, CHANGE);
}

```

使用Encoder库最简便

```c++
#include <XInput>
#include <Encoder.h>
#define A_PIN 2
#define B_PIN 3

Encoder myEncoder(A_PIN, B_PIN);

int oldPosition = 0;

void setup() {
    Serial.begin(9600);
    XInput.begin();

    XInput.setJoystickRange(JOY_LEFT, -900, 900);
}

void loop() {
    int newPosition = myEncoder.read();
    if (newPosition != oldPosition) {
        oldPosition = newPosition;
        Serial.println("位置:" + String(newPosition));
        // x轴设置为编码器值，y轴为0
        Serial.setJoystick(JOY_LEFT, newPosition, 0);
    }
}

```

## H排挡

设置引脚启用内部上拉电阻;
微动电阻常开引脚连接板子gpio引脚;
公共引脚连接GND引脚

电路情况: 3.3v --> gpio --> 常开引脚 | 断开 | 公共引脚 --> GND

原理: 开合电路中gpio电压为3.3v，微动开关触发闭合后，闭合电路中gpio
电压为0。

```c++
void setup() {
    // 将D4~D9设置成档位控制，尽量留出其他特殊引脚
    // A类引脚为模拟输入引脚，将连续变化的电压转换成0~1023数字值，用于识别霍尔踏板
    pinMode(D4, INPUT_PULLUP);
    ...
    pinMode(D9, INPUT_PULLUP);
}

void loop() {
    int status = digitalRead(D4);
    if (!D4) {
        // 该档位开关被按下
        ...
    }
}
```

