"""
強連結成分分解，典型021のまま
visitedだけでいいところをgrayとblackに分けて管理しているのでこちらのほうが冗長
DFSの部分がトポロジカルソートしたいときとか行きがけ順を使うときに使える？
"""

N, M = map(int,input().split())

graph = [[] for _ in range(N)]
inv = [[] for _ in range(N)]
value_sorted = []# 帰りがけ順に頂点を格納．

for i in range(M):
    a, b = map(int,input().split())
    a -= 1
    b -= 1
    graph[a].append(b)
    inv[b].append(a)

# 帰りがけ順を記録するための深さ優先探索
rev = [-1]*N # 探索し終わった頂点(=番号をつけ終わった頂点)が帰るべき頂点
idx = [0]*N # idx[i]：次に頂点iから探索するときにgraph[i]の何番目の頂点にいけばよいか
count = 0 # 次に付けるべき番号(value)
"""
＜注意＞
探索済みもしくはグラフ上でそこから頂点が進める頂点がない頂点x:  idx[x] >= len(graph[x])
"""
gray = [0]*N # 探索中の頂点, その頂点がcurになった時点で1になる
black = [0]*N # 探索済みの頂点．全ての子が探索済みになった時点で1になる．
for start in range(N): # 始点を変えて深さ優先探索
    if gray[start] == 1 or black[start] == 1:
        continue
    cur = start# curは現在の頂点．
    gray[start] = 1
    while True:
        if idx[cur] >= len(graph[cur]):
            # その頂点は探索終了なので番号をつけてかえる
            # もしくは，curがstartに一致していれば，ループを終了
            value_sorted.append(cur)
            black[cur] = 1
            count += 1
            if cur == start:
                break
            else:
                cur = rev[cur]
        # まだいけるところがあるが，次に行くべきとされている頂点が探索中の場合
        elif gray[graph[cur][idx[cur]]] == 1 or black[graph[cur][idx[cur]]] == 1:
            idx[cur] += 1
        # まだいけるところがある場合
        else:
            pre = cur
            cur = graph[cur][idx[cur]]
            rev[cur] = pre
            idx[pre] += 1 # preのidxを1増やす
            gray[cur] = 1

value_sorted.reverse()
    
# valueが大きい順にinv上で深さ優先探索を行い，各連結成分の大きさを求める
visited = [0]*N
sizes = []
for i in value_sorted:
    if visited[i] == 1:
        continue
    visited[i] = 1
    stack = [i]
    count = 1 # iを始点とした深さ優先探索木の大きさ
    while stack:
        x = stack.pop()
        for y in inv[x]:# inv[x]をvalueでソートする必要はない...はず
            if visited[y] == 1:
                continue
            visited[y] = 1
            stack.append(y)
            count += 1
    sizes.append(count)

ans = 0
for x in sizes:
    ans += (x*(x-1))//2

print(ans)