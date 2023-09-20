"""
全方位木DP
参考：https://qiita.com/Kiri8128/items/a011c90d25911bdb3ed3
"""
def rerooting_dp(graph):
    N = len(graph)
    root = 0

    ## トポロジカルソート．木なので DFS の訪問順でOK．##
    stack = [root]
    tree = [[] for _ in range(N)] # あとで順序があったほうが良いので set ではなく list
    par = [None] * N
    topo_sort = [root]
    while stack:
        v = stack.pop()
        for u in graph[v]:
            if u == par[v]:
                continue
            stack.append(u)
            tree[v].append(u)
            par[u] = v
            topo_sort.append(u)

    ## Bottom-Up 部分：普通に木dpみたいなのをやる． ##
    dp = [None] * N
    ME = [unit] * N
    for i in topo_sort[1:][::-1]:
        dp[i] = adj_bu(ME[i], i)
        p = par[i]
        ME[p] = merge(ME[p], dp[i])
    dp[0] = adj_fin(ME[root], root)

    ## Top-Down 部分：累積和（？）を使いながら周りのノードの情報を merge する．##
    TD = [unit] * N # 自分の部分木ではない，上の部分を計算．
    for i in topo_sort:
        ac = TD[i]
        for j in tree[i]:
            TD[j] = ac
            ac = merge(ac, dp[j])
        ac = unit
        for j in tree[i][::-1]:
            TD[j] = adj_td(merge(TD[j], ac), j, i)
            ac = merge(ac, dp[j])
            dp[j] = adj_fin(merge(ME[j], TD[j]), j)
    
    return dp

##### EDPC V #####
N, M = map(int, input().split())
graph = [set() for i in range(N)]
for i in range(N-1):
    x, y = map(int, input().split())
    graph[x-1].add(y-1)
    graph[y-1].add(x-1)

### Settings ###
unit = 1
# あるノードまわりの各部分木を集約するとき： adj_bu(merge(・, ・)) / adj_td(merge(・, ・))
# あるノードまわりのすべての部分木を集約するとき：adj_fin(merge(・, ・))
merge = lambda a, b: (a * b) % M 
adj_bu = lambda a, i: a + 1 
adj_td = lambda a, i, p: a + 1
adj_fin = lambda a, i: a

dp = rerooting_dp(graph)
print(*dp, sep = "\n")

##### ABC160 E #####
# mod = 10**9 + 7
# #### 2項係数 ####
# num = 10 ** 6  # num は必要分だけ用意する
# fact = [1, 1]  # fact[n] = (n! % mod)
# factinv = [1, 1]  # factinv[n] = ((n!)^(-1) % mod)
# inv = [0, 1]  # factinv 計算用

# def cmb(n, r):
#     if (r < 0) or (n < r):
#         return 0
#     r = min(r, n - r)
#     return fact[n] * factinv[r] * factinv[n-r] % mod
 
# for i in range(2, num + 1):
#     fact.append((fact[-1] * i) % mod)
#     inv.append((-inv[mod % i] * (mod // i)) % mod)
#     factinv.append((factinv[-1] * inv[-1]) % mod)
# ###############

# N = int(input())
# graph = [set() for i in range(N)]
# for i in range(N-1):
#     x, y = map(int, input().split())
#     graph[x-1].add(y-1)
#     graph[y-1].add(x-1)

# ### Settings ###
# unit = (1, 0) # 場合の数，部分木のサイズ
# # あるノードまわりの各部分木を集約するとき： adj_bu(merge(・, ・)) / adj_td(merge(・, ・))
# # あるノードまわりのすべての部分木を集約するとき：adj_fin(merge(・, ・))
# merge = lambda a, b: ((cmb(a[1] + b[1], a[1]) * a[0] * b[0])%mod, a[1] + b[1])
# adj_bu = lambda a, i: (a[0], a[1]+1)
# adj_td = lambda a, i, p: (a[0], a[1]+1)
# adj_fin = lambda a, i: (a[0], a[1]+1)

# dp = rerooting_dp(graph)
# for i in range(N):
#     print(dp[i][0])