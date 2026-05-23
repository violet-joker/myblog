[toc]

> RmlUi 一款类html语言设计ui样式的C++UI框架

# hello world (样例以SDL作为渲染后端)

复制官方提供的后端文件，platform和render相关文件即可

```cpp
SDL_Window *window = nullptr;
SDL_Renderer *renderer = nullptr;
int window_width;
int window_heigt;

Rml::RenderInterface *render_interface = nullptr;
Rml::SystemInterface *system_interface = nullptr;
Rml::Context *context;
Rml::ElementDocument *document;

void init() {
    // 设置接口，可自定义渲染方式，这里使用官方后端文件提供的接口
    render_interface = new RenderInterface_SDL(renderer);
    system_interface = new SystemInterface_SDL(window);

    Rml::SetRenderInterface(render_interface);
    Rml::SetSystemInterface(system_interface);

    Rml::Initialise();

    // 创建上下文
    context = Rml::CreateContext("main", Rml::Vector2i(window_width, window_heigt));

    // 加载字体文件(注意，rcss文件需要设置字体族与所选字体一致)
    Rml::LoadFontFace("./font.ttf");

    // 可以设置后备字体，rcss仅需设置与主字体一致即可
    Rml::LoadFontFace("./font-zh.ttf");
    Rml::LoadFontFace("./font-emoji.ttf");

    // 在创建doc文件前完成数据绑定
    bool show_text = true;
    Rml::String animal = "dog";
    if (Rml::DataModelConstructor constructor = context->CreateDataModel("animal")) {
        constructor.Bind("show_text", &show_text);
        constructor.Bind("animal", &animal);
    }

    // 创建doc文件
    document = context->LoadDocument("./hello_world.rml");
    document->Show();
}

void handle_event(SDL_Window *window, SDL_Event *event) {
    // 将SDL事件处理传递给rml
    RmlSDL::InputEventHandler(context, window, *event);
    // 处理鼠标移动,否则无法触发hover事件
    context->ProcessMouseMove(event->motion.x, event->motion.y, 0);
}

void loop() {
    context->Update();
    context->Render();
}
```

```html
<rml>
<head>
    <title>Hello world</title>
    <link type="text/rcss" href="window.rcss"/>
</head>
<body data-model="animals">
    <h1>RmlUi</h1>
    <p>Hello <span id="world">world</span>!</p>
    <p data-if="show_text">The quick brown fox jumps over the lazy {{animal}}.</p>
    <input type="text" data-value="animal"/>
</body>
</rml>
```

```css
body {
    font-family: "JetBrainsMono NF";
    font-size: 18px;
    color: #02475e;
    background: #fefecc;
    text-align: center;
    padding: 2em 1em;
    position: absolute;
    border: 2px #ccc;
    width: 500px;
    height: 200px;
    margin: auto;
}

h1, p, div {
    display: block;
}

h1 {
    color: #f6470a;
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 0.7em;
}

p {
    margin: 0.7em 0;
}

input.text {
    background-color: #fff;
    color: #555;
    border: 2px #999;
    padding: 5px;
    tab-index: auto;
    cursor: text;
    box-sizing: border-box;
    width: 200px;
    font-size: 0.9em;
}
```

# 数据绑定

给button绑定事件

```cpp
Rml::DataModelConstructor constructor = context->CreateDataModel("option");

auto on_test_click = [](Rml::DataModelHandle modle, Rml::Event& event, const Rml::VariantList& arguments) {
    std::print("clicked\n");
};

constructor.BindEventCallback("on_test_click", on_test_click);
```

```html
<button data-event-click="on_test_click()">btn</button>
```
