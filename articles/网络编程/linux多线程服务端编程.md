# 线程安全

## 二段式构造

构造函数 + initialize()

构造函数中泄露this指针，多线程中可能出现还未构造完成就被另一个
线程使用，这是线程不安全的。当某些回调函数需要传递this指针，可
以在外定义一个函数，构造结束后执行

## 内存问题

+ 缓冲区溢出 ---> 用string或vector<char>

+ 空悬指针/野指针 ---> 用shared_ptr/weak_ptr，智能引用计数指针

+ 重复释放、内存泄露 ---> scoped_ptr

+ 不配对的new/delete ---> 用vector或scoped_ptr

+ 内存碎片

## 线程安全的Observer

完成模式基本逻辑，Observer通过register_在Observable登记，
Observable的notifyObservers通知所有登记的Observer对象进行
更新；当Observer销毁析构时取消登记。

```c++
class Observer {
public:
    void observer(Observable* s) {
        s->register_(this);
        subject_ = s;
    }
    virtual void update() = 0;
    virtual ~Observer() {
        subject_->unregister(this);
    } 
private:
    Observable* subject_;
};

class Observable {
public:
    void register_(Observer* x);
    void unregister(Observer* x);
    void notifyObservers() {
        for (Observer* x : observers_) {
            x->update();
        }
    }
private:
    vector<Observer*> observers_;
};
```

可能出现的race conditions:

Observable并不知道实例是否销毁，当实例正在析构，
此时Observable发出更新通知，整个对象处于将死未死的状态，后果是未知的。
可以通过加锁来解决，但仍需要解决Observable查询对象是否存在。

能用判断指针是否为空来查询吗？

使用原始指针并不妥，当其暴露给别的线程，如果在某个地方通过其他的指针
释放了这段内存，此时原指针成为了空悬指针。

## 使用智能指针实现Observer

shared_ptr引用计数管理对象，weak_ptr判断是否空悬。

```c++
class Observer {
public:
    virtual void update() = 0;
    void observe(Observable* s) {
        s->register_(make_shared<Observer>(this));
        subject_ = s;
    }
private:
    Observable* subject_;
};

class Observable {
public:
    void register_(weak_ptr<Observer> x);
    void notifyObservers();
private:
    mutex mutex_; 
    vector<weak_ptr<Observer>> observers_;
    typedef vector<weak_ptr<Observer>>::iterator Iterator;
};

void Observable::notifyObservers() {
    lock_guard<mutex> lock {mutex_};
    Iterator it = observers_.begin();
    while (it != observers_.end()) {
        // weak_ptr提升成shared_ptr，再进行操作
        shared_ptr<Observer> obj {it->lock()};
        if (obj) {
            obj->update();
        } else {
            // 提升失败，对象已被销毁
            it = observers_.erase(it);
        }
    }
}
```

## 再论shared_ptr的线程安全

- 一个shared_ptr对象可以被多个线程同时读取

- 两个shared_ptr对象可以被两个线程同时写入

- 如果多线程读写同一个shared_ptr对象，需要加锁

shared_ptr引用计数本身是安全且无锁的，但对象的读写不是(析构算写操作)。


```c++
class Foo {};
shared_ptr<Foo> globalPtr;
mutex mut;

void doit(shared_ptr<Foo>& pFoo);

void read() {
    shared_ptr<Foo> localPtr;
    {
        lock_guard<mutex> lock {mut};
        localPtr = globalPtr;
    }
    doit(localPtr);
}

void write() {
    shared_ptr<Foo> newPtr {new Foo};
    // 引用计数+1，将globalPtr可能出现的析构"移出"临界区，缩短临界区长度
    shared_ptr<Foo> tmpPtr {globalPtr};
    {
        lock_guard<mutex> lock {mut};
        globalPtr = newPtr;
    }
    doit(newPtr);
}

```

我的理解是，对globalPtr对象的读写操作时需要互斥访问(互斥即可，
具体对内容有什么操作，是否需要读写锁由doit内决定)。注意将函数本地
的shared_ptr的构造和析构放在临界区外，以提升性能。


## shared_ptr技术与陷阱

意外延长对象声明期，例如function，bind等将实参拷贝了一份。

函数参数；使用const reference传参可解决。

总之就是注意是否存在未考虑到的额外计数引用的地方导致未能在预想的时机释放资源。


## 对象池

假设有一个Stock类表示股票，同名的股票对象可以共享，当没有任何人使用
该股票时对象析构。设计一个对象池StockFactory类，根据key返回Stock对象。
多人共享Stock类属于引用计数，可以设计返回shared_ptr。

StockFactory设计思路：

get函数通过参数key，在map<string, weak_ptr<Stock>> stocks_里判断查询，
若存在，将weak_ptr指针提升成shared_ptr返回；否则根据key生成一个实例。
使用weak_ptr便于析构对象，内存回收(不能使用shared_ptr)；


```c++
class Stock {
public:
    Stock(const string& s) : key(s) {}
    string getKey() { return key; }
private:
    string key;
};

// 继承enable_shared_from_this，将this指针包装成shared_ptr类型；但在定义时也需用shared_ptr
class StockFactory : public enable_shared_from_this<StockFactory> {
public:
    shared_ptr<Stock> get(const string& key);
private:
    // 定义在内部便于调用stock_
    void deleteStock(Stock* stock) {
        if (stock) {
            // 注意临界区设置互斥，从map中删除该stock
            lock_guard<mutex> lock {mutex_};
            stocks_.erase(stock->getKey());
        }
        delete stock;
    }
private:
    mutex mutex_;
    map<string, weak_ptr<Stock>> stocks_;
};

shared_ptr<Stock> StockFactory::get(const string& key) {
    shared_ptr<Stock> pStock;
    // 读操作，可能出现写操作，临界区设置互斥
    lock_guard<mutex> lock {mutex_};
    weak_ptr<Stock>& wkStock = stocks_[key];
    pStock = wkStock.lock();
    if (!pStock) {
        // key不存在，提升失败，创建对象，并绑定析构函数，使其析构时从map中删除
        pStock.reset(new Stock(key),
                    bind(&StockFactory::deleteStock,
                    shared_from_this(),
                    placeholders::_1));
        // wkStock需设置引用类型，才能更新stocks_
        wkStock = pStock;
    }
    return pStock;
}
```

将StockFactory的this指针包装成shared_ptr，防止StockFactory的生命周期比Stock短时
导致Stock析构造回调StockFactory造成内存错误。

包装成shared_ptr会导致StockFactory的生存期延长，使用weak_ptr，实现若对象存在，
则进行操作，否则不作处理。这样不管Stock和StockFactory谁先销毁，程序都不会崩溃。

```c++
class StockFactory : public enable_shared_from_this<StockFactory> {
public:
    shared_ptr<Stock> get(const string& key);
private:
    void weakDeleteCallback(const weak_ptr<StockFactory>& wkFactory, Stock* stock) {
        // 尝试提升，若StockFactory仍存在，则进行操作；否则忽略
        shared_ptr<StockFactory> factory = wkFactory.lock();
        if (factory) {
            removeStock(stock);
        }
        delete stock;
    }
    void removeStock(Stock* stock) {
        if (stock) {
            lock_guard<mutex> lock {mutex_};
            stocks_.erase(stock->getKey());
        }
    }
private:
    mutex mutex_;
    map<string, weak_ptr<Stock>> stocks_;
};

shared_ptr<Stock> StockFactory::get(const string& key) {
    shared_ptr<Stock> pStock;
    lock_guard<mutex> lock {mutex_};
    weak_ptr<Stock>& wkStock = stocks_[key];
    pStock = wkStock.lock();
    if (!pStock) {
        // bind函数传递this对象，同时传递weak_ptr强制转换包装的this对象
        pStock.reset(new Stock(key), 
                    bind(&StockFactory::weakDeleteCallback,
                    this,
                    weak_ptr(shared_from_this()),
                    placeholders::_1)); 
        wkStock = pStock;
    }
    return pStock;
}
```

# 线程同步精要

## 互斥器(mutex)

坚持使用非递归互斥器

```c++
class Foo {
public:
    void doit();
};

vector<Foo> foos;
mutex mutex_;

void post(const Foo& f) {
    lock_guard<mutex> lock {mutex_};
    foos.push_back(f);
}

void traverse() {
    lock_guard<mutex> lock {mutex_};
    for (auto it = foos.begin(); it != foos.end(); it++) {
        it->doit();
    }
}
```

如果doit里间接调用了post函数：
互斥锁非递归时陷入死锁(post申请的锁已被traverse持有，导致post堵塞。
doit堵塞，traverse无法释放锁，形成死锁)；
可递归时vector添加新元素，可能导致vector迭代器失效，遍历崩溃。

第二种不一定能被发现，而第一种出现问题时一定能发现，
因此推荐坚持使用非递归互斥锁。


解决办法：将修改推后，遍历结束后再修改；或者使用copy-on-write(修改副本)


经典死锁例子：
业务流程：Inventory清单负责添加、删除Request，Request构造后需要登记到Inventory，
析构时从Inventory清单删除。

Inventory打印所有Request信息(遍历调用每个实例的print方法)

```c++
#include <iostream>
#include <mutex>
#include <thread>
#include <set>

using namespace std;
class Request;

class Inventory {
public:
    void add(Request* req) {
        lock_guard<mutex> lock {mutex_1};
        requests_.insert(req);
    }
    void remove(Request* req) {
        lock_guard<mutex> lock {mutex_1};
        requests_.erase(req);
    }
    void printAll();
private:
    mutex mutex_1;
    set<Request*> requests_;
} g_inventory;

class Request {
public:
    void process() {
        lock_guard<mutex> lock {mutex_2};
        g_inventory.add(this);
    }
    ~Request() {
        lock_guard<mutex> lock {mutex_2};
        this_thread::sleep_for(1s);
        g_inventory.remove(this);
    }
    void print() {
        lock_guard<mutex> lock {mutex_2};
        cout << "hello from Request.\n";
    }
private:
    mutex mutex_2;
};

void Inventory::printAll() {
    lock_guard<mutex> lock {mutex_1};
    for (auto it = requests_.begin(); it != requests_.end(); it++) {
        (*it)->print();
    }
}

void threadFunc() {
    Request* req = new Request;
    req->process();
    delete req;
}

int main() {
    thread t {threadFunc};
    this_thread::sleep_for(500ms); // 确保调用printAll之前t线程完成new操作
    g_inventory.printAll();
    t.join();
}
```
申请锁情况：

printAll -> mutex_1

print -> mutex_2

=======================

~Request -> mutex_2

remove -> mutex_1

当printAll发生在~Request与remove之间，或者~Request发生在printAll与print之间时
造成了经典死锁: x 持有a申请b，y持有b申请a

代码手动设置延时可以模拟两种死锁情况(画甘特图更直观)。
上述代码为第一种死锁情况，第二种：

```c++
void threadFunc() {
    Request* req = new Request;
    req->process();
    this_thread::sleep_for(1s);
    delete req;
}
void printAll() {
    lock_guard<mutex> lock {mutex_1};
    this_thread::sleep_for(1s);
    ...
}
```

解决方法：将print或remove移出临界区(需要考虑其他方案解决race condition)
