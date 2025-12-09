> b站 Cherno C++教程学习笔记

# 浅拷贝与深拷贝

浅拷贝不会复制new在堆上的数据，只会拷贝指针，两个指针指向的是同一个
内存区。导致在析构delete时重复释放内存，程序崩溃。

以用原始c++特性写string数据类型为例

```c++
#include <iostream>
#include <cstring>

class String {
public:
    String(const char* string) {
        m_size = strlen(string);
        m_buffer = new char[m_size+1];
        memcpy(m_buffer, string, m_size + 1);
    }
    ~String() {
        delete[] m_buffer;
    }
    friend std::ostream& operator<<(std::ostream& stream, const String& string);
private:
    char *m_buffer;
    unsigned int m_size;
};

// 设置友元函数，使用std流输出
std::ostream& operator<<(std::ostream& stream, const String& string) {
    stream << string.m_buffer;
    return stream;
}

int main() {
    String a = "hello world";
    String b = a;
    // 此时为浅拷贝，m_buffer指向同一段地址
    // 程序结束后同一段内存释放两次，内存释放错误
    std::cout << a << std::endl << b << std::endl;
}
```

深拷贝

```c++
// 重写拷贝构造函数
String(const String& other)
    : m_size(other.m_size)
{
    m_buffer = new char[m_size+1];
    memcpy(m_buffer, other.m_buffer, m_size+1);
}
```


（ps：函数传值，全用const type& 即可，若需要复制，函数内部
复制即可，避免拷贝复制传参，浪费资源）

# 虚函数

实现多态的动态绑定

当使用基类指针或引用调用成员函数时，非虚函数只会调用基类的函数，而
虚函数则能正确调用实际对象对应派生类的成员函数。

没有使用虚函数的情况：将打印两次Entity，根据数据类型寻找对应的函数

```c++
#include <iostream>

using namespace std;

class Entity {
public:
    string GetName() {
        return "Entity";
    }
};

class Player : public Entity {
private:
    string name;
public:
    Player(const string& name) : name(name) {}
    string GetName() {
        return name;
    }
};

void print(Entity* e) {
    cout << e->GetName() << endl;
}

int main() {
    Entity* e1 = new Entity();
    Player* e2 = new Player("Jack");
    print(e1);
    print(e2);
}
```

使用虚函数，虚表维护映射关系，遍历查找真正对应的函数。
虚表会带来内存空间上的消耗以及查询映射时的性能消耗，
但其影响微乎其微，非极限状态可忽略不记。


设置虚函数：打印Entity和Jack
```c++
class Entity {
public:
    virtual string GetName() {
        return "Entity";
    }
};

class Player : public Entity {
public:
    string GetName() override {
        return name;
    }
}
```

纯虚函数：
基类不必实现函数功能，子类必须实现。
可用于写接口，要求子类必须完成某项功能。
类似其他语言中的interface关键字

```c++
#include <iostream>

using namespace std;

class Printable {
public:
    virtual string GetClassName() = 0;
};

class A : public Printable {
public:
    string GetClassName() override {
        return "A";
    }
};

void print(Printable* p) {
    cout << p->GEtClassName() << endl;
}

int main() {
    print(new A());
}
```

# 仿函数

即对象重载()符号，使对象看起来和函数一样。

```c++
class A {
public:
    int operator() (int a, int b) {
        return a + b;
    }
    double operator() (double a, double b) {
        return (a + b) * 2;
    }
};

int main() {
    A a;
    cout << a(2, 3) << " " << a(2.0, 3.0) << endl;
}
```


# 个人使用笔记

## 函数返回引用

```c++
class A {
public:
    int& getValue() { return value; }
private:
    int value;
};

class B {
public:
    B() = delete;
    B(A *a) :value(a->getValue()) {}
private:
    // 引用类型必须在声明的时候进行初始化，而类成员则必须在构造函数里初始化
    int& value;
};
```

## 文件操作

```c++
#include <filesystem>
#include <fstream>

namespace fs = std::filesystem;

int main() {
    // 设置路径
    fs::path dir_path = "test_dir";
    // 使用 / 拼接路径
    fs::path file_path = dir_path / "test.txt";

    // 创建目录
    if (!fs::exists(dir_path)) {
        fs::create_directory(dir_path);
    }

    std::ofstream file(file_path);
    file << "hello world!";
    file.close();

    // 读取文件大小
    std::cout << "file size:" << fs::file_size(file_path) << "\n";

    fs::path new_file_path = dir_path / "new_name.txt";
    fs::rename(file_path, new_file_path);

    // 遍历目录
    for (const auto& entry : fs::directory_iterator(dir_path)) {
        std::cout << entry.path() << "\n";
        // 可以直接调用成员函数获取文件类型，例如
        entry.is_regular_file();
        entry.is_directory();

        fs::path path = entry.path();
        // 文件名相关
        path.filename();       // 获取纯文件名，例如test.txt
        path.stem();           // 获取文件名主体 test
        path.extension();      // 获取文件扩展名
        path.relative_path();  // 获取相对路径(相对于指定的根路径)
        path.parent_path();    // 获取父目录路径(删除最后一级文件名)

        fs::path filename = entry.filename();
        std::string s_name = filename.string();
        char *c_name = filename.c_str();
    }

    // 删除文件/目录
    fs::remove(dir_path);
}

```
