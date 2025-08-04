设置字体:

```c++
io.Fonts->AddFontFromFileTTF("绝对路径/字体.fft", 18.0f, nullptr, io.Fonts->GetGlyphRangesChineseSimplifiedCommon());
```

```c++
bool is_open;
ImGui::Begin("window_name", &is_open, window_flags);
// 传递bool指针只能修改布尔值为false，并非关闭窗口

// 以下达到关闭效果
if (is_open) {
    ImGui::Begin("window", &is_open);
}

```
