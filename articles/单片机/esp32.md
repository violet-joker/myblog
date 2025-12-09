[toc]

# 点亮板载led

```c++
void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
}
```

# 点亮tft屏幕(ST7735)

## tft符号功能说明：

- VCC/GND 电源正负极，电压范围2.8~3.5v
- SCL SPI串口时钟线
- SDA SPI数据线，接单片机MOSI引脚
- RES 使能引脚，低电平使能
- DC SPI数据/指令选择引脚
- CS SPI片选引脚，低电平有效，不用时接地
- BLK 背光控制开关，默认打开，低电平关闭背光(可以不接线)


## 修改User_Setup.h配置

```
<!--  ESP32-S3 的 SPI 控制器： -->
SPI2_HOST (HSPI) - 通常引脚: MOSI=11, SCLK=12
SPI3_HOST (VSPI) - 通常引脚: MOSI=35, SCLK=36

<!--  默认情况下，TFT_eSPI 使用 VSPI -->
<!--  使用HSPI引脚则需要宏USE_HSPI_PORT -->
```

```c++
#include <TFT_eSPI.h>

#define ST7735_DRIVER   // 选择对应驱动
#define ST7735_ROBOTLCD // 选择7735驱动型号
#define TFT_RGB_ORDER TFT_RGB  // 如果反色则打开TFT_GBR 

#define TFT_WIDTH 128
#define TFT_HEIGHT 160

#define USE_HSPI_PORT // 如果选择HSPI引脚，则需要打开宏
#define TFT_SCLK 12 // SDL
#define TFT_MOSI 11 // SDA
#define TFT_RST 10 
#define TFT_DC 9
#define TFT_CS 46 
```

简单测试

```c++
#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();

void setup() {
    tft.init();  
    tft.setRotation(1);
    tft.fillScreen(0x1F00);
    tft.setTextColor(TFT_WHITE);
    tft.setTextSize(2);
    tft.setCursor(10, 20);
    tft.println("hello world!");
}


```

# esp32运行imgui

ImDuino项目，配置屏幕尺寸，并重新实现screen_init和screen_draw函数；
若颜色异常，修改驱动配置或位运算修改screen.pixels的RGB顺序即可，
16位(5,6,5)分别表示三种通道的rgb数值。


完整实例代码

```c++
#include <TFT_eSPI.h>
#include <imgui.h>

TFT_eSPI tft = TFT_eSPI();

#define SCREENX 160
#define SCREENY 128
#define LOW_BIT     31        // 0000000000011111
#define MID_BIT     2016      // 0000011111100000
#define HIGH_BIT    63488     // 1111100000000000
texture_alpha8_t fontAtlas;
texture_color16_t screen;
ImGuiContext *context;
ImDrawList *draw_list;

ImGuiWindowFlags windowFlags;

void screen_init() {
    tft.init();
    tft.setRotation(1);
    screen.init(SCREENX, SCREENY);
}

void screen_draw() {
    uint16_t *pixels = (uint16_t*)screen.pixels;
    for (int i = 0; i < screen.w * screen.h; i++) {
        uint16_t low = LOW_BIT & pixels[i];
        uint16_t mid = MID_BIT & pixels[i];
        uint16_t high = HIGH_BIT & pixels[i];
        
        low <<= 11;
        mid >>= 1, mid &= MID_BIT, mid >>= 5;
        high >>= 5;
        pixels[i] = low | mid | high;
    }
    tft.pushImage(0, 0, screen.w, screen.h, (uint16_t*)screen.pixels);
}


void setup() {
    Serial.begin(9600);
    context = ImGui::CreateContext();
    ImGui_ImplSoftraster_Init(&screen);

    ImGuiStyle &style      = ImGui::GetStyle();
    style.AntiAliasedLines = false;
    style.AntiAliasedFill  = false;
    style.WindowRounding   = 0.0f;

    ImGuiIO &io = ImGui::GetIO();
    io.Fonts->Flags |=
        ImFontAtlasFlags_NoPowerOfTwoHeight | ImFontAtlasFlags_NoMouseCursors;

    uint8_t *pixels;
    int width, height;
    io.Fonts->GetTexDataAsAlpha8(&pixels, &width, &height);
    fontAtlas.init(width, height, (alpha8_t *)pixels);
    io.Fonts->TexID = &fontAtlas;

    windowFlags |= ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoTitleBar;

    screen_init();
}

unsigned long currentTime;
unsigned long lastTime;

void loop() {

    ImGui_ImplSoftraster_NewFrame();
    ImGui::NewFrame();
    ImGui::SetNextWindowPos(ImVec2(0.0, 0.0));
    ImGui::SetNextWindowSize(ImVec2(SCREENX, SCREENY));

    ImGui::Begin("test", nullptr, windowFlags);

    currentTime = millis();
    float delta_time = currentTime - lastTime;
    float value = 1000.0f / delta_time;
    ImGui::Text("FPS:%.1f", value);
    lastTime = currentTime;

    draw_list = ImGui::GetWindowDrawList();
    static float step = 40.0f;
    ImVec2 pos1 {0, 100};
    ImVec2 pos2 {step, 150};
    ImU32 red = IM_COL32(255, 0, 0, 255);
    ImU32 green = IM_COL32(0, 255, 0, 255);
    ImU32 blue = IM_COL32(0, 0, 255, 255);
    ImU32 color[3] {red, green, blue};

    for (int i = 0; i < 3; i++) {
        draw_list->AddRectFilled(pos1, pos2, color[i]);
        pos1.x += step;
        pos2.x += step;
    }

    ImGui::End();

    ImGui::Render();
    ImGui_ImplSoftraster_RenderDrawData(ImGui::GetDrawData());

    screen_draw();
}
```

# 控制舵机

```c++
#include <ESP32Servo.h>

#define PIN_SERVO 14

Servo servo;
int servo_angle;

void setup() {
    servo.attach(PIN_SERVO);
    servo.write(servo_angle);
}
```

# FreeRTOS

实现异步调度

## 创建任务

```c++
TaskHandle_t task_handle;

void setup() {
    // 创建任务: 任务函数、别名、分配内存、参数、优先级、句柄
    xTaskCreate(task_one, "one", 8 * 1024, NULL, 1, &task_handle);
}

void task_one(void *param) {
    for (int i = 0; i < 10; i++) {
        Serial.println("task_one");
        deley(1000);
    } 
    vTaskDelete(task_handle);
}
```

## 消息队列

QueueHandle_t queHandle;

```c++
void setup() {
    // 优先级、分配内存大小
    queHandle = xQueueCreate(1, sizeof(unsigned char));
    xTaskCreate(task, "task", 1024, NULL, 1, NULL);
}

void loop() {
    unsigned char message;
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        if (cmd == '1') {
            message = 1;
            xQueueSend(queHandle, (void*) &message, 0);
        } else if (cmd == '2') {
            message = 2;
            xQueueSend(queHandle, (void*) &message, 0);
        }
    }
}

void task(void *param) {
    unsigned char message;
    while (1) {
        // 无消息则跳出
        xQueueReceive(queHandle, &message, portMAX_DELAY); 
        ...
    }
}
```

## 互斥锁

```c++
SemaphoreHandle_t mutex;

void setup() {
    // 创建互斥锁
    mutex = xSemaphoreCreateMutex();
}

void task() {
    // 获取锁
    if (xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE) {
        // 临界区 
        ...
        // 释放锁
        xSemaphoreGive(mutex);
    }
}
```

# 读写SD卡

```c++
File dir = SD.open(path);
dir.isDirectory();

// 仅针对目录文件有效
File file = dir.openNextFile();

```

```c++
// 配置SPI引脚(MISO, SCLK, MOSI, CS)
#define SD_CS_PIN 4

// dfs遍历目录
void dfs(const char *path, uint8_t cnt = 0) {
    File dir = SD.open(path);
    if (!dir || !dir.isDirectory()) return;
    Serial.printf("%s:\n", path);
    File file = dir.openNextFile();

    while (file) {
        if (file.isDirectory()) {
            std::string d_path(cnt ? path : "");
            d_path += "/" + std::string(file.name());
            dfs(d_path.c_str(), cnt+1);
        } else {
            Serial.printf("%s/%s\n", path, file.name());
        }
        file.close();
        file = dir.openNextFile();
    }
}

void setup() {
    SD.begin(SD_CS_PIN);
    Serial.println("遍历SD卡目录:\n");
    dfs("/");
}
```


