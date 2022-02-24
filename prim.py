"""
コードそのものは典型049のもの
Prim法の関数部分まではそのまま最小全域木のライブラリとして利用可能
"""

from heapq import heappush, heappop

INF = 10 ** 15

def Prim(adj, s, n): # (始点, ノード数)
    # 隣接リストadjにおいて, iから出るedgeはadj[i]に格納されており, 
    # 各edgeは(行先, 重み)で表現されている
    cut = [INF] * n # カット辺のコスト
    hq = [(0, s)] # (カット辺のコスト, node)
    cut[s] = 0
    seen = [False] * n # ノードが確定済みかどうか
    while hq:
        v = heappop(hq)[1] # ノードを pop する
        if seen[v]:# 枝刈り: すでに最短距離が確定したノードから出る辺については調べ終わっているので次のループへ
            continue
        seen[v] = True
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if seen[to] == False and cost < cut[to]:
                cut[to] = cost
                heappush(hq, (cost, to))
    return cut

N, M = map(int,input().split())
graph = [[] for _ in range(N+1)]
for i in range(M):
    C, L, R = map(int,input().split())
    graph[L-1].append((R, C))
    graph[R].append((L-1, C))

cut = Prim(graph, 0, N+1)
# print(cut)
if INF in cut:
    print(-1)
else:
    print(sum(cut))