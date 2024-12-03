# 朴素dijkstra

基于贪心求解单源最短路，不能用于负权边

> eg: 给出编号1~n个点，m条边以及权值，随机询问某点到1号点的最短距离.

初始化起点到其他点的距离为正无穷，到源点的距离为0，循环n次，**每次寻找
未访问过的距离源点最近的点(权值最小的点)，并用该点更新源点到其他点的距离。**
dijkstra预处理源点到各点的距离，查表即可。

朴素dijkstra每次暴力搜索最近的点，需要计算n个点到源点的距离,
时间复杂度为**O(n^2)**；代码简单，适合稠密图。

```c++
const int N = 1e3 + 10;
// d数组记录源点到节点的最短距离，f数组邻接矩阵存图
int n, m, d[N], f[N][N], x, y, z;
bool vis[N];
int main() {
    cin >> n >> m;
    while (m--) {
        cin >> x >> y >> z;
        f[x][y] = f[y][x] = z; // 有向图、无向图视题目而定
    }
    dijkstra();
}
```

```c++
void dijkstra() {
    memset(d, 127, sizeof(d));
    d[1] = 0;
    for (int i = 1; i <= n; i++) {
        int t = -1;
        // 寻找未访问过的距离最近的点
        for (int j = 1; j <= n; j++)
            if (!vis[j] && (t == -1 || d[t] < d[j]))
                t = j;
        vis[t] = true;
        // 更新到其他点的距离
        for (int j = 1; j <= n; j++)
            if (!vis[j] && f[t][j])
                d[j] = min(d[j], d[t] + f[t][j]);
    }
}
```

# 堆优化dijkstra

可用优先队列维护点的距离，使得每次取最近的点时间复杂度为O(logn)，
总体时间复杂度为O(nlogn)

```c++

```
