# ST表

通过预处理，解决静态RMQ(区间查询)问题，尤其是可重复贡献问题。
例如区间最值、区间gcd、区间按位与、区间按位和。

> eg: 对于长度为n的数组，询问m次，每次查询区间[l, r]的最值

用二维数组预处理构建ST表：对于数组f[i][k]，表示以下标i为起点，
区间长度为2^k的区间最值。

通过数组实质查表只能查询固定区间(2的整数次幂)，但对于可重复
贡献问题(重合区间不影响查询结果)，限制查询的左右边界之差等于
固定区间长度即可。

> 状态转移方程: f[i][k] = max(f[i][k-1], f[i + f[i + (1 << (k-1))][k-1]);


类似于自底向上建二叉树，预处理时间复杂度**O(nlogn)**，
此后单次查询查表即可，时间复杂度**O(1)**,
因此总体时间复杂度为**O(nlogn)**

```c++
#include <iostream>
#include <cmath>

using namespace std;
const int N = 1e3 + 10, K = 32;
int a[N], f[N][K], n, m;

int main() {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) cin >> a[i];
    init();
    while (m--) {
        int l, r;
        cin >> l >> r;
        cout << ask(l, r) << endl;
    }
}
```

```c++
void init() {
    for (int i = 1; i <= n; i++)
        f[i][0] = a[i];
    // 循环条件：区间长度不超过n
    for (int k = 1; (1 << k) <= n; k++)
        for (int i = 1; i + (1 << k) - 1 <= n; i++)
            f[i][k] = max(f[i][k-1], f[i + (1 << (k-1))][k-1]);
}

int ask(int l, int r) {
    // 向下取整
    int k = log2(r - l + 1);
    return max(f[l][k], f[r - (1 << k) + 1][k]);
}


/*
图例解读查询操作:
假设查询长度区间为7
|1 2 3 4 5 6 7|   l ~ r
|1 2 3 4|5 6 7|   -----> f[l][k]
|1 2 3|4 5 6 7|   -----> f[r - (1 << k) + 1][k]
*/
```
