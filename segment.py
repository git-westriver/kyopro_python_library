def init(init_val):
    seg = [IDE_ELE] * (2 * NUM)
    #set_val
    for i in range(len(init_val)):
        seg[i+NUM-1]=init_val[i]    
    #built
    for i in range(NUM-2,-1,-1) :
        seg[i]=segfunc(seg[2*i+1],seg[2*i+2]) 
    return seg
    
def update(seg, k, x):
    k += NUM-1
    seg[k] = x
    while k:
        k = (k-1)//2
        seg[k] = segfunc(seg[k*2+1],seg[k*2+2])
    
def query(seg, p, q):
    # 半開区間[p,q)に対するクエリ
    if q<=p:
        return IDE_ELE
    p += NUM-1
    q += NUM-2
    res=IDE_ELE
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

import math

A = [2, 3, 4, 13, 9, 1, 100, 96, 33, 15, 12]
N = len(A)

IDE_ELE = 0
NUM = 1 << (N-1).bit_length()
segfunc = math.gcd

seg = init(A)

print(query(seg, 4, 5))# 9
print(query(seg, 7,11))# 3
update(seg, 5, 50)
print(query(seg, 5, 7))# 50
