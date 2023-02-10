# 平衡二分木
# Left-Leaning Red Black Tree

# 「以下」の場合は左へ, 「より大きい」の場合は右へ

import copy

class node():
    
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

        # 赤をTrue, 黒をFalseとする
        self.color = True

        # 親
        self.par = None

        # この節点を根とする部分木の総和。自分のkeyの値。
        self.total = key

        # この接点を根とする部分木の大きさ。生成時は0。
        self.size = 1

def right_rotate(root, x):
    # xがx.parの左の子である場合に, xが親になるように回転
    # xがx.parの左の子でないとバグるので注意
    p = x.par
    if p == None or x != p.left:
        raise Exception

    a = x.left
    b = x.right
    c = p.right

    

def normal_insert(root, key):
    # 通常の2分木におけるinsert

    # 探索するノード
    x = root
    # 追加するノード
    y = node(key)

    while True:
        # yはかならずxを根とする部分木に入るので
        # yのkeyをxのtotalに加算
        x.total += key
        # xのサイズを+1
        x.size += 1

        if key <= x.key and x.left == None:
            x.left = y
            y.par = x
            break
        elif key <= x.key:
            x = x.left
        elif key > x.key and x.right == None:
            x.right = y
            y.par = x
            break
        else:
            x = x.right

def Nth_largest(root, N):
    """
    N番目に大きい要素を返す
    """
    if N > root.size:
        return None
    
    x = root

    while True:
        if x.right == None:
            # 右部分木なし
            # N = 1の場合はx.keyが答え(除外しないとx.leftでNoneを指定して次のループでエラーになる)
            if N == 1:
                return x.key
            # そうでない場合、左部分木の中に答えあり
            N -= 1
            x = x.left
        elif N == x.right.size + 1:
            # xの値が答え
            return x.key
        elif N > x.right.size + 1:
            # 左部分技の中に答えあり
            N -= x.right.size + 1
            x = x.left
        elif N <= x.right.size:
            # 右部分木のなかに答えあり
            x = x.right

def partial_sum_Nth_larger(root, N):
    """
    N番目に大きい要素以上の和
    """
    N = min(N, root.size)

    x = root
    S = 0

    while True:
        if x.right == None:
            if N == 1:
                return S + x.key
            else:
                S += x.key
                N -= 1
                x = x.left
        elif N == x.right.size + 1:
            return S + x.key + x.right.total
        elif N > x.right.size + 1:
            S += x.key + x.right.total
            N -= x.right.size + 1
            x = x.left
        else:
            x = x.right

def successor(root, x):
    """
    与えられたノードxに対し、そのノードの次に大きい値を持つノードを返す
    """
    if x.right == None:
        # 右の子がいないときは, xの先祖で、xより大きい（xを左部分木にもつ）ところまで遡る
        xx = copy.copy(x)
        # xxの親ノードp
        p = xx.par
        while xx == p.right:
            xx = p
            p = xx.par

        # 親pが答え
        return p
    
    # 右の子がいるなら, xの右部分木の最小値を与えるノードが答え
    xx = x.right
    while xx.left != None:
        xx = xx.left
    
    return xx

def delete(root, x):
    """
    ノードxを削除する
    """
    # 子を持たない場合
    if x.left == None and x.right == None:
        if x.par == None:
            return
        p = x.par
        if p.left == x:
            p.left = None
        elif p.right == x:
            p.right = None
        x.par = None

        # pから根まで遡り, sizeを1減らし, totalをx.key減らす
        while p.par != None:
            p.size -= 1
            p.total -= x.key
            p = p.par
    
    # 子が一つだけある場合
    elif x.left == None or x.right == None:
        if x.left == None:
            y = x.right
        else:
            y = x.left

        if x.par == None:
            root = y
            return
        
        p = x.par
        if p.left == x:
            p.left = y
        elif p.right == x:
            p.right = y
        x.par = None
        y.par = p

        # pから根まで遡り, sizeを1減らし, totalをx.key減らす
        while p.par != None:
            p.size -= 1
            p.total -= x.key
            p = p.par
    
    # 子が2つともある場合
    else:
        # 次節点yを持ってくる. yはその定義から左の子を持たない. 
        y = successor(root, x)
        delete(root, y)

        # xのところをyで置き換える.
        # keyはyの値にする
        x.key = y.key
        # totalはx,yの差分とx.totalで再構成
        x.total += y.key - x.key
        # sizeはそのまま

if __name__ == '__main__':

    import time

    start = time.time()

    # rootが決まればそこから出るleft, rightへのポインタで木全体が定まるとする. 
    # 木全体をもし何かのオブジェクトにしたくなったらそれは後からできる. 
    # (すでに作ったものに上から被せればよいので)

    root = node(3)
    root.color = False# 根は初期状態で黒

    insert(root, 2)
    insert(root, 5)
    insert(root, 7)
    insert(root, 0)
    insert(root, -4)
    insert(root, -100)
    insert(root, 24)
    insert(root, 6)
    insert(root, 1)
    insert(root, 4)
    insert(root, 3)
    print(Nth_largest(root, 9))

    print(partial_sum_Nth_larger(root, 4))
    print(partial_sum_Nth_larger(root, 9))

    print(successor(root, root.left).key)
    print(successor(root, root.right).key)
    print(successor(root, root.left.left).key)

    delete(root, root.right.right.right)
    print(Nth_largest(root, 9))
    print(partial_sum_Nth_larger(root, 9))

    delete(root, root.right.right)
    print(Nth_largest(root, 2))
    print(partial_sum_Nth_larger(root, 2))
    print(Nth_largest(root, 3))
    print(partial_sum_Nth_larger(root, 3))

    delete(root, root.left)
    print(Nth_largest(root, 5))
    print(partial_sum_Nth_larger(root, 5))
    print(Nth_largest(root, 6))
    print(partial_sum_Nth_larger(root, 6))

    end = time.time()
    print(end-start)# 0.0001499652862548828
