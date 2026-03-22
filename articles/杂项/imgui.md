## 设置字体:
```cpp
io.Fonts->AddFontFromFileTTF("路径/字体.fft", 18.0f, nullptr, io.Fonts->GetGlyphRangesChineseSimplifiedCommon());
```

## tips

```cpp
bool is_open;
ImGui::Begin("window_name", &is_open, window_flags);
// 传递bool指针只能修改布尔值为false，并非关闭窗口

// 以下达到关闭效果
if (is_open) {
    ImGui::Begin("window", &is_open);
}
```

## 设置背景docking窗口(达到在原生窗口上停靠的效果)

```cpp
void CreateDockingRootWindow() {
    int w, h;
    SDL_GetWindowSize(window, &w, &h);
    ImVec2 window_size {(float)w, (float)h};
    ImGuiWindowFlags flags = ImGuiWindowFlags_NoDocking |
        ImGuiWindowFlags_NoTitleBar |
        ImGuiWindowFlags_NoCollapse |
        ImGuiWindowFlags_NoResize |
        ImGuiWindowFlags_NoMove |
        ImGuiWindowFlags_NoBringToFrontOnFocus |
        ImGuiWindowFlags_NoNavFocus |
        ImGuiWindowFlags_NoBackground;

    // 暂时清空边距和边框宽度，结尾复原
    ImGuiStyle& style = ImGui::GetStyle();
    const ImVec2 padding = style.WindowPadding;
    const float border_size = style.WindowBorderSize;
    style.WindowPadding = ImVec2(0.0f, 0.0f);
    style.WindowBorderSize = 0.0f;

    ImGui::SetNextWindowPos(ImVec2(0, 0));
    ImGui::SetNextWindowSize(window_size);
    ImGui::SetNextWindowViewport(ImGui::GetMainViewport()->ID);

    ImGui::Begin("dockingRoot", nullptr, flags);
    // 将根窗口设为Docking根节点
    if (ImGui::GetIO().ConfigFlags & ImGuiConfigFlags_DockingEnable) {
        ImGuiID dockspace_id = ImGui::GetID("DockingRootSpace");
        ImGui::DockSpace(dockspace_id, ImVec2(0.0f, 0.0f), ImGuiDockNodeFlags_PassthruCentralNode);
        // ImGuiDockNodeFlags_PassthruCentralNode：允许点击根窗口空白处穿透（可选）
    }
    ImGui::End();


    style.WindowPadding = padding;
    style.WindowBorderSize = border_size;
}
```

## 渲染图片

```cpp
// 设置绝对位置
ImGui::SetCursorScreenPos(ImVec2(x, y));
// 设置相对位置 (用错函数一直对不上坐标，导致debug半个多点...)
ImGui::SetCursorPos(ImVec2(x, y));

...

ImVec2 imageSize {frameWidth * scale, frameHeight * scale};
ImVec2 uv0 {(float)currentFrame / totalFrames, 0};
ImVec2 uv1 {(float)(currentFrame + 1) / totalFrames, 1};
ImGui::SetCursorScreenPos(ImVec2(x, y));
// spriteSheet为图片纹理
ImGui::Image(spriteSheet, imageSize, uv0, uv1);
```
