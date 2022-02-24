"""
典型029のまんま
segfuncとide_eleの変更は可能
ただし，区間更新クエリではなく区間加算クエリの場合には若干書き換えが必要
具体的には，is_pendedが不要になり（lazyが0なら保留されてないことがわかるので），遅延評価で子に遅延する値を伝搬するときに半分の値にする必要がある．
詳しくは https://tsutaj.hatenablog.com/entry/2017/03/30/224339 参照．
"""

# 単位元ide_eleを設定する必要あり
# segfuncが
#   gcd なら 0
#   min なら INT_MAX
#   max なら -INT_MAX(正の値だけなら0)
#   add なら 0

segfunc = max
ide_ele = 0

W, N = map(int,input().split())
a = [0]*W
n = W

#num:n以上の最小の2のべき乗
num =2**(n-1).bit_length()
seg=[ide_ele]*2*num # 2*num-1でも大丈夫(多分)
lazy = [ide_ele]*2*num # 遅延配列
is_pended = [False]*2*num # 「区間更新」の場合，遅延配列だけではそれが空かどうか判定できないので，遅延配列のフラグを建てるためのboolが必要

#####segfunc######
#def segfunc(x,y):
#    return 

def init(init_val):
    #set_val
    for i in range(n):
        seg[i+num-1]=init_val[i]    
    #built
    for i in range(num-2,-1,-1) :
        seg[i]=segfunc(seg[2*i+1],seg[2*i+2]) 
    
def update(k,x):
    k += num-1
    seg[k] = x
    while k:
        k = (k-1)//2
        seg[k] = segfunc(seg[k*2+1],seg[k*2+2])

def lazy_eval(k, l, r):
    """
    k番目のノードについて遅延評価を行う
    k番目のノードは区間[l, r)に対応する
    << 遅延評価をすればそのノードの値も正しい値になる >>
    """
    # 遅延配列の値が空でない(=単位元に等しくない)場合は，自ノードの値および子ノードへ値を伝播する
    if is_pended[k]:
        seg[k] = lazy[k]
    
        # k番目のノードが最下段でない場合は，子ノードの遅延配列へ伝播する
        if r - l > 1:
            lazy[2*k+1] = lazy[k]
            lazy[2*k+2] = lazy[k]
            # 子のフラグを立てる
            is_pended[2*k+1] = True
            is_pended[2*k+2] = True
        
        # 伝播が終わったので，フラグを外す
        is_pended[k] = False

def seg_update(p, q, change):
    """
    区間[p, q)に対して，区間の値すべてを区間の最大値に更新する
    更新に子ノードの（更新後の）値が必要になる箇所を保管しておき，すべての子が調べ終わった後に順次更新
    """
    stack = [(0, 0, num)]
    need_update = []
    while stack:
        x = stack.pop()

        # ノードxの遅延評価
        lazy_eval(x[0], x[1], x[2])

        # ノードxが区間[p, q)の範囲と交わりを持たなければ何もしない
        if x[2] <= p or q <= x[1]:
            continue

        # 区間[p, q)がノードxの区間を完全に被覆している場合は遅延配列に値を入れた後に評価
        if (p <= x[1] and x[2] <= q):
            lazy[x[0]] = change
            is_pended[x[0]] = True
            lazy_eval(x[0], x[1], x[2])
        
        # そうでなければ，子ノードの値先に計算する必要がある
        else:
            # 注意：x[1]とx[2]の偶奇が異なるのはx[1]=x[2]+1のときだけで，このとき[p, q)がノードxの区間を完全に被覆している．したがってここにくるときはx[1]+x[2]は偶数
            # stackに2つの子を追加し，自身はneed_updateの末尾に追加
            stack.append((2*x[0]+1, x[1], (x[1]+x[2])//2))
            stack.append((2*x[0]+2, (x[1]+x[2])//2, x[2]))
            need_update.append(x)
    
    # need_updateに追加されたのと逆順にsegの値を更新
    for i in range(len(need_update)-1, -1, -1):
        k = need_update[i][0]
        seg[k] = segfunc(seg[2*k+1], seg[2*k+2])

def query(p, q):
    """
    ここは普通にstackをつかったDFSでOK
    """
    stack = [(0, 0, num)]
    ret = ide_ele
    while stack:
        x = stack.pop()

        # ノードxの遅延評価
        lazy_eval(x[0], x[1], x[2])

        # ノードxが区間[p, q)の範囲と交わりを持たなければ何もしない
        if x[2] <= p or q <= x[1]:
            continue

        # 区間[p, q)がノードxの区間を完全に被覆している場合
        if (p <= x[1] and x[2] <= q):
            ret = segfunc(ret, seg[x[0]])
        
        # そうでなければ，子ノードを調べに行く
        else:
            # 注意：x[1]とx[2]の偶奇が異なるのはx[1]=x[2]+1のときだけで，このとき[p, q)がノードxの区間を完全に被覆している．したがってここにくるときはx[1]+x[2]は偶数
            stack.append((2*x[0]+1, x[1], (x[1]+x[2])//2))
            stack.append((2*x[0]+2, (x[1]+x[2])//2, x[2]))
    return ret

Q = []
ans = []
for i in range(N):
    L, R = map(int,input().split())
    L -= 1
    R -= 1
    Q.append((L, R))

for L, R in Q:
    x = query(L, R+1)
    ans.append(x+1)
    seg_update(L, R+1, x+1)

print("\n".join(map(str, ans)))
