> box2d 2.4.1

# Hello Box2D

使用b2BodyDef、b2FixtureDef定义刚体基本信息

```c++
// 定义物理世界
b2Vec2 gravity(0, 10);
b2World world(gravity);


b2BodyDef bodyDef;
// 设置允许动态运动
bodyDef.type = b2_dynamicBody;
bodyDef.position.Set(0, 10);

/*
    bodyDef.type决定刚体在物理世界的根本行为模式，分三种：
    b2_staticBody静态物体:质量无限大，速度恒为零，不消耗迭代次数，
    性能消耗低，适合做平台、墙壁;
    b2_dynamicBody动态物体:有限的质量，受物理定律支配;
    b2_kinematicBody运动学物体:质量无限大，运动状态由代码控制，
    适合作为移动平台、传送带。

*/

// 设置刚体形状
b2PolygonShape box;
box.SetAsBox(1, 2); // 宽2高4的矩形
b2FixtureDef fixtureDef;
fixtureDef.shape = &box;    // 刚体形状
fixtureDef.density = 1;     // 刚体密度
fixtureDef.friction = 0.3;  // 摩擦系数

// 创建刚体，并设置基础属性
b2Body *body = world.CreateBody(&bodyDef);
body->CreateFixture(&fixtureDef);
```


world.Step推进物理世界的时间步长，计算物体运动状态

```c++
// 对应60fps
float timeStep = 1.0f / 60.0f;  
// 求解约束系统中速度、力约束迭代次数（越高性能消耗越大，模拟越精准）
// 推荐值：平台跳跃6，赛车游戏8，高精度模拟10
int velocityIterations = 6; 
// 求解约束系统重位置约束的迭代次数(修正物体重叠和穿透，关节连接正确性)
// 位置修正对性能影响更大，一般情况2~3，高精度4~6
int positionIterations = 2;

for (int i = 0; i < 60; i++) {
    world.Step(timeStep, velocityIterations, positionIterations);
    b2Vec2 position = body->GetPosition();
    float angle = body->GetAngle();
    std::cout << "position.x, position.y, angle:"
        << position.x << ", "
        << position.y << ","
        << angle << "\n";
}
```

# SDL中更新world

sdl逐帧渲染，在时间循环中计时，累计一定时间后调用step更新物理世界

```c++
SDL_AppResult SDL_AppIterate(void *appstate) {
    static Uint64 lastTime = SDL_GetTicks();
    Uint64 currentTime = SDL_GetTicks();
    if (currentTime - lastTime > (Uint64)(1000 / 60)) {
        lastTime = currentTiem;
        world.Step(timeStep, velocityIterations, positionIterations);
    }

    return SDL_APP_CONTINUE;
}
```

# 碰撞模块

```c++
// 设置多边形
b2Vec2 vertices[count];
b2PolygonShape polygon;
polygon.Set(vertices, count);
```

-------------------------------------------------

> box2d 3.1.0

# Hello Box2D 

## creating a world

```c++
// C无法将结构体初始化成0，所以有必要使用默认的初始化函数
b2WorldDef worldDef = b2DefaultWorldDef();
worldDef.gravity = (b2Vec2){0.0f, 10.0f};   // 默认是-10
b2WorldId worldId = b2CreateWorld(&worldDef);
```

## creating a box

```c++
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

```c++
float timeStep = 1.0f / 60.0f;
int subStepCount = 4;
for (int i = 0; i < 90; i++) {
    b2World_Step(worldId, timeStep, subStepCount);
    b2Vec2 position = b2Body_GetPosition(bodyId);
    b2Rot rotation = b2Body_GetRotation(bodyId);
    printf("%4.2f %4.2f %4.2f\n", position.x, position.y, b2Rot_GetAngle(rotation));
}
```

## cleanup

```c++
b2DestroyWorld(worldId);
```
