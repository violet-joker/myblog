> b站 小彭老师(双笙子佯谬) 课程笔记

# 现代C++中的多线程

## std::thread

thread的实现背后基于pthread

构造函数可以是任意lambda表达式，当线程启动时，会执行lambda里的内容。

成员函数join()等待该进程结束(主线程等待子线程结束，阻塞等待)

遵循RAII思想，当所在函数退出时，会调用thread的析构函数。

使用detach()分离该线程：线程声明周期不再由当前std::thread对象管理，
而是线程退出后自动销毁；进程退出时也会自动退出，且主进程不会等待
所有子进程结束。

移动到全局线程池

```c++
std::vector<std::thread> pool;

void myfunc() {
	std::thread t1([] {
		std::cout << "hello world!\n";
	});
	pool.push_back(std::move(t1));
}

int main() {
	myfunc();
	for (auto &t : pool) t.join();
}
```

main函数退出后自动join全部函数: 定义TreadPool类，析构函数调用join

```c++
class ThreadPool {
	std::vector<std::thread> m_pool;
public:
	void push_back(std::thread thr) {
		m_pool.push_back(std::move(thr));
	}

	~ThreadPool() {
		for (auto &t : m_pool) t.join();
	}
}

ThreadPool tpool;

...
tpool.push_back(std::move(t1));
...
```

## 异步 std::async

std::async接收一个带返回值的lambda，自身返回一个std::future对象。

lambda的函数体将在另一个线程里执行。

调用future的get()方法，会阻塞等待线程完成，并获取返回值。

wait()也可阻塞等待其执行完毕，但不会返回值。

wait_for(), 指定一个最长等待时间(chrono里的类)，返回一个future_status
表示是否成功。超时返回future_status::timeout，成功返回future_status::ready

wait_until()，传入指定时间点

std::async的第一个参数可以设为std::launch::deferred，将lambda函数体内的
运算推迟到future的get()被调用时开始。可以实现惰性求值。

std::async 底层实现：std::promise

如果需要future的浅拷贝，可以用std::shared_future


## 互斥量

std::mutex的lock()会检测是否上锁，若没有则上锁；否则陷入等待，直到mutex
被另一个线程解锁后，才再次上锁。

unlock()进行解锁操作。

mtx.lock()和mtx.unlock()之间的代码段，同一时间只有一个线程在执行，
从而避免数据竞争。

std::lock_guard 符合RAII思想的上锁和解锁。

std::lock_guard的构造函数里调用mtx.lock()，析构函数里调用mtx.unlock()

```c++
std::lock_guard grd(mtx);
```

std::lock_guard严格在析构时unlock()，若希望提前unlock，可使用std::unique_lock

std::unique_lock额外存储了一个flag表示是否释放，析构时会检测flag判断是否调用unlock

```c++
std::unique_lock grd(mtx);
grd.unlock();
grd.lock();
```

std::unique_lock的构造函数可以传递std::defer_lock参数(不会自动lock，需要手动
调用grd.lock()才能上锁)


```c++
std::mutex mtx;

mtx.try_lock(); //无阻塞尝试上锁，上锁失败直接返回false，否则返回true
mtx.try_lock_for(); //等待一段时间(传递chrono时间单位)
mtx.try_lock_until();
...
std::unique_lock grd(mtx, std::try_to_lock); // 会调用mtx.try_lock()
grd.owns_lock(); // 判断是否上锁成功
...
mtx.lock();
std::unique_lock grd(mtx, std::adopt_lock); // 默认mtx已经上锁
std::lock_guard grd(mtx, std::adopt_lock); // 默认mtx已经上锁
```

std::unique_lock 和 std::mutex 具有相同的接口

## 死锁

两个线程同时持有彼此需要的锁，且无法释放。

同一个线程重复调用lock()

解决方案：

```c++
// 1.一个线程永远不同时持有两个锁

// 2.双方上锁顺序一致

// 3.使用std::lock同时对多个上锁
std::lock(mtx1, mtx2);

std::scoped_lock(mtx1, mtx2);  // std::lock的RAII版本

// 4.同一线程会调用到的后续函数不再上锁并说明非线程安全

// 5. 使用std::recursive_mutex，自动判断是不是同一个线程lock同一个锁，但会有性能损失

std::recursive_mutex mtx;
```

封装一个线程安全的vector
```c++
class myVector {
    std::vector<int> m_arr;
    std::mutex m_mtx;
public:
    void push_back(int val) {
        m_mtx.lock();
        m_arr.push_back(val);
        m_mtx.unlock();
    }
    size_t size() const {
        m_mtx.lock();
        size_t ret = m_arr.size();
        m_mtx.unlock();
        return ret;
    }
};

// 在size()函数中，m_mtx是非const的，使用mutabl修饰即可
// 解决逻辑上const而部分成员非const
mutable std::mutex m_mtx;
```

读写锁shared_mutex

```c++
class myVector {
    std::vector<int> m_arr;
    mutable std::shared_mutex m_mtx;
public:
    void push_back(int val) { // 写操作
        m_mtx.lock();
        m_arr.push_back(val);
        m_mtx.unlock();
    }
    size_t size() const {   // 读操作
        m_mtx.lock_shared();
        size_t ret = m_arr.size();
        m_mtx.unlock_shared();
        return ret;
    }
};


...

void push_back(int val) {
    std::unique_lock grd(m_mtx);
    m_arr.push_back(val);
}

size_t size() const {
    std::shared_lock grd(m_mtx);  // 符合RAII思想的lock_shared
    return m_arr.size();
}
...
```
