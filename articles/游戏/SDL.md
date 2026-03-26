[toc]

# examples

[SDL实例](https://examples.libsdl.org/SDL3/)

# 窗口管理

```cpp
// 创建窗口
SDL_Window *window = SDL_CreateWindow(
    "title",
    Width,
    Height,
    SDL_WINDOW_RESIZEABLE
);

// 资源回收，避免内存泄漏
if (window)
    SDL_DestroyWindow(window);
SDL_Quit();


// 同时创建window和renderer
SDL_CreateWindowAndRenderer("name", WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_RESIZEABLE, &window, &renderer);
```

## 渲染器

```cpp
// 渲染器相关函数
SDL_CreateRenderer();       // 为窗口创建一个渲染器
SDL_DestroyRenderer();      // 销毁渲染器
SDL_SetRenderDrawColor();   // 设置用于绘制操作的颜色
SDL_RenderClear();          // 用绘制颜色清除当前渲染目标
SDL_RenderPresent();        // 用已执行的渲染更新屏幕

// 绘制矩形
SDL_FRect rect {100, 100, 100, 100};
SDL_RenderRect(renderer, &rect);
SDL_RenderFillRect(renderer, &rect);

// 绘制线
SDL_RenderLine(renderer, x1, y1, x2, y2);

// 绘制散点
SDL_FPoint points[100];
SDL_RenderPoints(renderer, points, SDL_arraysize(points));

// 绘制凸多边形
SDL_Vertex *vertices;
SDL_RenderGeometry(renderer, NULL, vertices, vertexCount, NULL, 0);
// 可设置顶点数据，vertexCount需为3的倍数，本质是三个顶点一组，绘制多个三角形
vertices[i].position.x = x;
vertices[i].position.y = y;
vertices[i].color.r = r; // 0~1.0
vertices[i].color.g = g;
vertices[i].color.b = b;
vertices[i].color.a = a;

// 设置重叠部分的渲染方式，SDL_BLENDMODE_BLEND为混合模式，默认的NONE会覆盖渲染
SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);

```



SDL_Renderer渲染过程为"准备-提交"两个阶段(双缓冲机制)，SDL_RenderClear,
SDL_RenderCopy,SDL_RenderDrawLine等函数属于准备阶段，在一个后台缓冲区
进行所有绘制操作；SDL_RenderPresent将后台缓冲区已完成的画面交换到前台显示。

```cpp
// SDL_RenderClear会清空之前的渲染，并以当前renderer颜色填充背景，需要重新设置颜色
SDL_SetRenderDrawColor(renderer, r, g, b, a);
SDL_RenderClear(renderer);

...各种渲染操作...

// 呈现渲染，每次循环结束时调用即可
SDL_RenderPresent(renderer);

```

## 纹理

```cpp
// 纹理(可从surface创建、文件加载)
SDL_CreateTexture();        // 为渲染上下文创建纹理
SDL_CreateTextureFromSurface();
SDL_DestroyTexture();       // 销毁纹理
SDL_UpdateTexture();        // 用新的像素数据更新纹理的一部分
SDL_LockTexture();          // 提供直接的像素访问，用于流式纹理
SDL_UnlockTexture();
SDL_RenderTexture();        // 将纹理渲染到当前目标
SDL_SetRenderTarget();      // 将纹理设置成当前渲染目标

    
// 渲染纹理: .., .., 纹理裁剪矩形，实际目标矩形(若两者不符会自动进行缩放)，填NULL表示FULL
SDL_RenderTexture(renderer, texture, NULL, &dsf_rect);
// 绕中心点center旋转rotation度(中心点以dst_rect作为参考系而非全局坐标系), flip参数可设置水平、竖直翻转
SDL_RenderTextureRotated(renderer, texture, NULL, &dst_rect, rotation, &center, SDL_FLIP_NONE);
```

通过图片创建纹理

```cpp
float texture_width;
float texture_height;
SDL_Texture *texture;

void init() {
    SDL_Surface *surface = SDL_LoadPNG("path/test.png");
    texture_width = surface->w;
    texture_height = surface->h;
    texture = SDL_CreateTextureFromSurface(renderer, surface);
    SDL_DestroySurface(surface);
}

void loop() {
    SDL_FRect dsf_rect {WIDTH / 2, HEIGHT / 2, texture_width, texture_height};
    SDL_RenderTexture(renderer, texture, NULL, &dsf_rect);
}
```

自定义纹理

```cpp
SDL_Surface *surface = SDL_CreateSurface(100, 200, SDL_PIXELFORMAT_RGBA8888);
SDL_FillSurfaceRect(surface, NULL, SDL_MapRGB(SDL_GetPixelFormatDetails(surface->format), NULL, 255, 100, 100));
SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, surface);
```

SDL_Window主要是创建一个窗口，设置窗口相关属性；
SDL_Renderer主要是在某个窗口中渲染纹理，展现视觉效果；
纹理是某个图形画面数据，可以修改、变换、组合。

SDL_Window是容器，SDL_Renderer是画家(图形API的跨平台封装)，
SDL_Texture是颜料和素材(纹理数据的统一封装)。

纹理数据 --> 渲染器处理 --> 窗口显示

# 事件处理

```cpp
// 监听输入
bool quit = false;
SDL_Event e;
while (!quit) {
    // 非阻塞监听(读取事件队列,将每次读取到的队首赋值给e)
    while (SDL_PollEvent(&e)) {
        if (e.type == SDL_EVENT_QUIT)
            quit = true; 
        else if ()
    }
    // 设置延时，避免cpu占用过高
    SDL_Delay(10);
}
```

# 模板

使用SDL_MAIN_USE_CALLBACKS，程序入口不再是传统的main函数，
而是SDL内部管理的主入口点，会调用几个特定的回调函数。如主要的
四个回调函数：SDL_AppInit, SDL_AppEvent, SDL_AppIterate，SDL_AppQuit

使用模板便于不同平台之间移植，尤其android，ios。

```cpp
// 启用回调机制
#define SDL_MAIN_USE_CALLBACKS 1
#include <SDL3/SDL.h>
// 该头文件适配各个平台的main函数
#include <SDL3/SDL_main.h>

// 仅在程序启动时运行一次(初始化)
SDL_AppResult SDL_AppInit(void **appstate, int argc, char *argv[]) {

    // 可选项，指定应用名，版本号，包名
    SDL_SetAppMetadata("test", "1.0", "com.example.test");

    return SDL_APP_CONTINUE;
}

// 当有事件发生时调用(处理用户输入)
SDL_AppResult SDL_AppEvent(void *appstate, SDL_Event *event) {
    if (event->type == SDL_EVENT_QUIT)    
        return SDL_APP_SUCCESS;

    return SDL_APP_CONTINUE;
}

// 每一帧都会调用，执行逻辑更新、画面渲染
SDL_AppResult SDL_AppIterate(void *appstate) {


    SDL_Delay(10);
    return SDL_APP_CONTINUE;
}

// 程序退出前，释放所有资源
void SDL_AppQuit(void *appstate, SDL_AppResult result) {

}
```
