from heapq import heappush, heappop

INF = 10 ** 15

def Dijkstra(adj, s, n): # (始点, ノード数)
    # 隣接リストadjにおいて, iから出るedgeはadj[i]に格納されており, 
    # 各edgeは(行先, 重み)で表現されている
    dist = [INF] * n
    hq = [(0, s)] # (distance, node)
    dist[s] = 0
    seen = [False] * n # ノードが確定済みかどうか
    while hq:
        v = heappop(hq)[1] # ノードを pop する
        if seen[v]:# 枝刈り: すでに最短距離が確定したノードから出る辺については調べ終わっているので次のループへ
            continue
        seen[v] = True
        for to, cost in adj[v]: # ノード v に隣接しているノードに対して
            if seen[to] == False and dist[v] + cost < dist[to]:
                dist[to] = dist[v] + cost
                heappush(hq, (dist[to], to))
    return dist

if __name__ == '__main__':
    N = 8
    adj = [[] for _ in range(8)]
    adj[0] = [(1,5),(2,20)]
    adj[1] = [(2,10),(3,13)]
    adj[2] = [(3,12),(4,14),(5,8),(6,7),(7,9)]
    adj[3] = [(4,1),(5,8)]
    adj[4] = [(5,9)]
    adj[5] = [(6,11),(7,100)]
    adj[6] = [(7,13)]
    adj[7] = [(2,12)]

    dist = Dijkstra(adj,1,N)

    print(dist)