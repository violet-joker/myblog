> b站 Cherno C++教程学习笔记

# 浅拷贝与深拷贝

浅拷贝不会复制new在堆上的数据，只会拷贝指针，两个指针指向的是同一个
内存区。导致在析构delete时重复释放内存，程序崩溃。

以用原始c++特性写string数据类型为例

```c++
#include <iostream>
#include <cstring>

using namespace std;

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
    cout << a << endl << b << endl;
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

实现多态

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

使用虚函数，虚表维护映射关系，查找真正对应的函数。
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


