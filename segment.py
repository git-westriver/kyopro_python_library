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
    
def query(p,q):
    # 半開区間[p,q)に対するクエリ
    if q<=p:
        return ide_ele
    p += num-1
    q += num-2
    res=ide_ele
    while q-p>1:
        if p&1 == 0:
            res = segfunc(res,seg[p])
        if q&1 == 1:
            res = segfunc(res,seg[q])
            q -= 1
        p = p//2
        q = (q-1)//2
    if p == q:
        res = segfunc(res,seg[p])
    else:
        res = segfunc(segfunc(res,seg[p]),seg[q])
    return res

# 単位元ide_eleを設定する必要あり
# segfuncが
#   gcd なら 0
#   min なら INT_MAX
#   max なら -INT_MAX(正の値だけなら0)

import math
segfunc = math.gcd
ide_ele = 0

a = [2, 3, 4, 13, 9, 1, 100, 96, 33, 15, 12]
n = len(a)

#num:n以上の最小の2のべき乗
num =2**(n-1).bit_length()
seg=[ide_ele]*2*num # 2*num-1でも大丈夫(多分)

init(a)


# 以下, 実行例
print(query(4,5))# 9
print(query(7,11))# 3

update(5, 50)

print(query(5,7))# 50
print(seg)
