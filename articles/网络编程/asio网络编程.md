# 常用函数

## IP地址

```c++
// 根据字符串创建v4或v6地址
ip::address::from_string(str);

ip::address addr = ip::address::from_string("127.0.0.1");
```

## 端点

```c++
ip::tcp::endpoint;
ip::udp::endpoint;
ip::icmp::endpoint;

endpoint();                 // 默认构造函数
endpoint(protocol, port);   // 常用来创建可以接受新连接的服务端socket
endpoint(addr, port);       // 连接到某个地址和端口号的端点

ip::tcp::endpoint ep;
ip::tcp::endpoint ep(ip::tcp::v4(), 80);
ip::tcp::endpoint ep(ip::address::from_string("127.0.0.1"), 80);

// 根据端点获取地址、端口、协议
cout << ep.address().to_string();
cout << ep.port();
cout << ep.protocol();
```

## 套接字

```c++
io_service service;
ip::udp::socket socket(service, ep);

```

## udp 通讯
```c++
ip::udp::endpoint target_ep;                    // 用于接收记录另一设备的ip和端口号
ip::udp::endpoint local_ep(ip::address, port);  // 绑定本地端口的ip和端口号
ip::udp::socket socket(service, local_ep);      // 将套接字绑定本地端点
socket.receive_from(buffer, target_ep);         // 接受时将自动绑定target_ep的ip和端口
socket.send_to(buffer, target_ep);
```

## 检测是否关闭链接

```c++
char data[0xff];
boost::system::error_code err;
size_t length = sock.read_some(buffer(data), err);
if (err == error::eof) {
    return;
}
```

# 三种io_context处理模式

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

# 回显服务器/客户端

## TCP同步客户端

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
        << (copy == msg ? "OK" : "FAIL") << endl;
    
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

## TCP同步服务端

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
        sock.write_some(buffer(msg));
        sock.close();
    }
}

int main() {
    handle_connections();
}

```

# UDP超时结束堵塞

```c++
// 使用asio::steady_timer定时器设置timeout

steady_timer timer(service, 100ms);
// 回调函数必须匹配错误码参数
timer.async_wait([&](error_code ec) {
    if (!ec) {
        socket.close();
        std::cout << "timeout\n";
    }
});

// 缓冲区，端点，处理完成后的回调函数
socket.async_receive_from(buffer(buf), ep, 
        [&] (error_code ec, size_t bytes) {
            timer.cancel(); 
        });

service.run();



// 回调签名必须严格匹配：错误码，实际接受字节数
void handler(const asio::error_code& ec, std::size_t bytes_transferred);
```
