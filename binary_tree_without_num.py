"""
接点に番号をつけていない2分探索木
binary_treeがrootだけしか保持しないオブジェクトなら定義せずにrootだけで木を識別すればいい気がしてきた
"""
import copy

class binary_tree():
    """
    「以下」の場合は左へ, 「より大きい」の場合は右へ
    """

    def __init__(self, root_key):
        self.root = node(root_key)

    def insert(self, key):
        # 探索するノード
        x = self.root
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
    
    def Nth_largest(self, N):
        """
        N番目に大きい要素を返す
        """
        if N > self.root.size:
            return None
        
        x = self.root

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
    
    def partial_sum_Nth_larger(self, N):
        """
        N番目に大きい要素以上の和
        """
        N = min(N, self.root.size)

        x = self.root
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
    
    def successor(self, x):
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
    
    def delete(self, x):
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
            while True:
                p.size -= 1
                p.total -= x.key
                if p.par == None:
                    break
                p = p.par
        
        # 子が一つだけある場合
        elif x.left == None or x.right == None:
            if x.left == None:
                y = x.right
            else:
                y = x.left

            if x.par == None:
                self.root = y
                return
            
            p = x.par
            if p.left == x:
                p.left = y
            elif p.right == x:
                p.right = y
            x.par = None
            y.par = p

            # pから根まで遡り, sizeを1減らし, totalをx.key減らす
            while True:
                p.size -= 1
                p.total -= x.key
                if p.par == None:
                    break
                p = p.par
        
        # 子が2つともある場合
        else:
            # 次節点yを持ってくる. yはその定義から左の子を持たない. 
            y = self.successor(x)
            self.delete(y)

            # xのところをyで置き換える.
            # keyはyの値にする
            pre_x_key = x.key
            x.key = y.key

            # totalはxのkeyの増加分とx.totalで再構成
            x.total += x.key - pre_x_key
            # totalを根に向かって更新
            p = x.par
            if p == None:
                return
            while p != None:
                p.total += x.key - pre_x_key
                p = p.par

            # sizeはそのまま
                
class node():

    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.par = None

        # この節点を根とする部分木の総和。自分のkeyの値。
        self.total = key

        # この接点を根とする部分木の大きさ。生成時は0。
        self.size = 1


if __name__ == '__main__':

    import time

    start = time.time()

    T = binary_tree(3)
    T.insert(2)
    T.insert(5)
    T.insert(7)
    T.insert(0)
    T.insert(-4)
    T.insert(-100)
    T.insert(24)
    T.insert(6)
    T.insert(1)
    T.insert(4)
    T.insert(3)
    print(T.Nth_largest(9))# 1

    print(T.partial_sum_Nth_larger(4))# 42
    print(T.partial_sum_Nth_larger(9))# 55

    print(T.successor(T.root.left).key)# 3
    print(T.successor(T.root.right).key)# 6
    print(T.successor(T.root.left.left).key)# 1

    T.delete(T.root.right.right.right)
    print(T.Nth_largest(9))# 0
    print(T.partial_sum_Nth_larger(9))# 31

    T.delete(T.root.right.right)
    print(T.Nth_largest(2))# 5
    print(T.partial_sum_Nth_larger(2))# 11
    print(T.Nth_largest(3))# 4
    print(T.partial_sum_Nth_larger(3))# 15

    T.delete(T.root.left)
    print(T.Nth_largest(5))# 3
    print(T.partial_sum_Nth_larger(5))# 21
    print(T.Nth_largest(6))# 1
    print(T.partial_sum_Nth_larger(6))# 22

    print(T.root.size) # 9
    print(T.root.total) # ???<-手計算せよ

    end = time.time()
    print(end-start)# 0.0001499652862548828
