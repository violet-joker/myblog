[toc]

> box2d 3.1.0

# Hello Box2D 

## creating a world

```cpp
// C无法将结构体初始化成0，所以有必要使用默认的初始化函数
b2WorldDef worldDef = b2DefaultWorldDef();
worldDef.gravity = (b2Vec2){0.0f, 10.0f};   // 默认是-10
b2WorldId worldId = b2CreateWorld(&worldDef);
```

## creating a box

```cpp
b2BodyDef bodyDef = b2DefaultBodyDef();
bodyDef.type = b2_dynamicBody;
bodyDef.position = (b2Vec2){0.0f, 4.0f};
b2BodyId bodyId = b2CreateBody(worldId, &bodyDef);

// half width, half height
b2Polygon box = b2MakeBox(1.0f, 1.0f);
b2ShapeDef shapeDef = b2DefaultShapeDef();
shapeDef.density = 1.0f;
shapeDef.material.friction = 0.3f;

b2CreatePolygonShape(bodyId, &shapeDef, &box);
```

## simulating the world

```cpp
float timeStep = 1.0f / 60.0f;
int subStepCount = 4;
for (int i = 0; i < 90; i++) {
    b2World_Step(worldId, timeStep, subStepCount);
    b2Vec2 position = b2Body_GetPosition(bodyId);
    b2Rot rotation = b2Body_GetRotation(bodyId);
    printf("%4.2f %4.2f %4.2f\n", position.x, position.y, b2Rot_GetAngle(rotation));
}
```

timeStep表示前进时间量,subStepCount反映模拟精度与计算成本,平台跳跃游戏设置成2,赛车设置成4,高精度设置成6~8

```cpp
// 按60帧演算
void update() {
    static Uint64 lastTime = SDL_GetTicks();
    Uint64 currentTime = SDL_GetTicks();
    if (currentTime - lastTime > (Uint64)(1000 / 60)) {
        lastTime = currentTime;
        b2World_Step(worldId, timeStep, subStepCount);
    }
}

// 使用累积器计算更新时间
void update() {
    static Uint64 accumulator = 0;
    static Uint64 lastTime = SDL_GetTicks();
    cosnt Uint64 stepMs = 1000 / 60;

    Uint64 currentTime = SDL_GetTicks();
    Uin64 frameTime = currentTime - lastTime;
    lastTime = currentTime;
    accumulator += frameTime;

    // 若卡顿延迟,通过accumulator可以多执行几次step赶超
    while (accumulator >= stepMs) {
        b2World_Step(worldId, timeStep, subStepCount);
        accumulator -= stepMs;
    }
}
```

## cleanup

```cpp
b2DestroyWorld(worldId);
```


# debug

## b2DebugDraw

使用b2DebugDraw配置回调函数和上下文指针，选择需要的渲染类型即可，若未实现则会跳过渲染
```cpp
void DrawCircleFcn(b2Vec2 center, float radius, b2HexColor, void *context);
void DrawPointFcn(b2Vec2 p, float size, b2HexColor color, void *context);
void DrawPolygonFcn(const b2Vec2 *vertices, int vertexCount, b2HexColor color, void *context);
void DrawSegmentFcn(b2Vec2 p1, b2Vec2 p2, b2HexColor color, void *context);
void DrawSolidCapsuleFcn(b2Vec2 p1, b2Vec2 p2, float radius, b2HexColor color, void *context);
void DrawSolidCircleFcn(b2Transform transform, float radius, b2HexColor color, void *context);
void DrawSolidPolygonFcn(b2Transform transform, const b2Vec2 *vertices, int vertexCount, float radius, b2HexColor color, void *context);
void DrawStringFcn(b2Vec2 p, const char *s, b2HexColor color, void *context);
void DrawTransformFcn(b2Transform transform, void *context);
```


以渲染矩形为例:b2MakeBox()创建的矩形会调用实体多边形函数，以下使用SDL简单渲染边框

```cpp
// 编写回调函数渲染逻辑
void DrawSolidPolygonFcn(b2Transform transform, const b2Vec2 *vertices, int vertexCount, float radius, b2HexColor color, void *context) {
    // 根据不同渲染后端，转换上下文指针
    SDL_Renderer *renderer = (SDL_Renderer *)context;
    Uint8 r = (color >> 16) & 0xFF;
    Uint8 g = (color >> 8 ) & 0xFF;
    Uint8 b = color & 0xFF;
    Uint8 a = (color >> 24) & 0xFF;
    SDL_SetRenderDrawColor(renderer, r, g, b, a);
    b2Vec2 point1, point2;
    for (int i = 0; i < vertexCount; i++) {
        // transform为物理世界真实坐标，vertices为物体内部相对坐标，调用相关函数转换坐标
        point1 = b2TransformPoint(transform, vertices[i]);
        point2 = b2TransformPoint(transform, vertices[(i + 1) % vertexCount]);
        point1 *= PIXEL_SIZE;
        point2 *= PIXEL_SIZE;
        SDL_RenderLine(renderer, point1.x, point1.y, point2.x, point2.y);
    }
    // printf("DrawSolidPolygonFcn\n");
}

// 配置需要的回调函数
void setup() {
    b2DebugDraw debugDraw = b2DefaultDebugDraw();
    debugDraw.DrawSolidPolygonFcn = DrawSolidPolygonFcn;
    debugDraw.context = renderer;
}

// 在游戏循环中启用debugDraw
void loop() {
    update();
    b2World_Draw(worldId, &debugDraw);
    SDL_RenderPresent(renderer);
}
```


# b2Chain

由点构成闭合不规则多边形，用于制作围栏;
注意点的顺序，对于闭合图形，仅有一侧可以检测碰撞，
比如点序顺时针绘制的图形从外到内产生碰撞，从内到外无碰撞，
将点序逆时针排列即可达到相反效果。

```cpp
b2BodyId chainBodyId;
b2ChainId;
{
    b2BodyDef bodyDef = b2DefaultBodyDef();
    bodyDef.type = b2_staticBody;
    chainBodyId = b2CreateBody(worldId, &bodyDef);

    // 相对于刚体中心坐标的局部坐标
    b2Vec2 points[4] = {{0, 0}, {5, 0}, {5, 5}, {0, 5}};
    b2ChainDef chainDef = b2DefaultChainDef();
    chainDef.isLoop = true;
    chainDef.points = points;
    chainDef.count = 4;
    chainId = b2CreateChain(chainBodyId, &chainDef);
}


// 若想启用b2DebugDraw，需实现回调函数debugDraw.DrawLineFcn;
```
