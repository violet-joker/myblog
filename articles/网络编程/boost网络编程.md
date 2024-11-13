## 检测连接何时关闭

```c++
char data[0xff];
boost::system::error_code err;
size_t length = sock.read_some(buffer(data), err);
if (err == error::eof) {
    return;
}
```

## 三种io_context处理模式

+ 一个io处理一个线程，基础

```c++
io_context io;
ip::tcp::socket sock(io);
sock.async_connect(ep, connect_handler);
io.run();
```

+ 一个io实例处理多个线程

```c++
io_context io;
ip::tcp::socket sock1(io);
ip::tcp::socket sock2(io);
sock1.async_connect(ep, connect_handler);
sock2.async_connect(ep, connect_handler);
for (int i = 0; i < 5; i++) {
    boost::thread {run_service};
}

...

void run_service() {
    io.run();
}
```

+ 多个io实例处理多个线程

```c++
io_context io[2];
ip::tcp::socket sock1(io[0]);
ip::tcp::socket sock2(io[1]);
sock1.async_connect(ep, connect_handler);
sock2.async_connect(ep, connect_handler);
for (int i = 0; i < 2; i++) {
    boost::thread{run_service, i};
}

...

void run_service(int idx) {
    io[idx].run();
}
```

## 回显服务器/客户端

### TCP同步客户端

```c++
#include <boost/asio.h>
#include <iostream>
#include <vector>
#include <thread>

using namespace std;
using namespace boost::asio;
io_context io;
ip::tcp::endpoint ep(ip::address::from_string("127.0.0.1"), 2001);

void sync_echo(string msg) {
    // 初始化socket，连接终端，发送消息
    ip::tcp::socket sock(io);
    sock.connect(ep);
    sock.write_some(buffer(msg));
    
    // buf接收回传消息，bytes接收读取的字节数，便于构造copy字符串
    char buf[0xff];
    int bytes = sock.read_some(buffer(buf));
    string copy(buf, bytes);
    cout << "server echoed our " << msg << ": "
        << (copy == msg ? "OK" << "FAIL") << endl;
    
    sock.close();
}

int main() {
    string messages[] = {
        "hello world", "ha ha ha",
        "fine fine", "well well"
    };
    vector<thread> v;
    for (auto s : messages) {
        v.emplace_back(sync_echo, s);
    }
    for (auto &t : v) {
        t.join();
    }
}

```

### TCP同步服务端

```c++
#include <iostream>
#include <boost/asio.hpp>

using namespace std;
using namespace boost::asio;

io_context io;
ip::tcp::endpoint ep(ip::tcp::v4(), 2001);

void handle_connections() {
    ip::tcp::acceptor acc(io, ep);
    char buf[0xff];

    while (true) {
        ip::tcp::socket sock(io);
        acc.accept(sock);
        int bytes = sock.read_some(buffer(buf));
        string msg(buf, bytes);
        // 回传信息
        sock.write_some(msg);
        sock.close();
    }
}

int main() {
    handle_connections();
}

```
