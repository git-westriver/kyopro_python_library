"""
赤黒木
rootが変更されると困るのでやっぱりclassとして用意しておいたほうが良さそう. 
total, sizeがいらない場合

TODO:　left_rotateとright_rotateは統一できそう
"""
import copy

class RBT():
    """
    「以下」の場合は左へ, 「より大きい」の場合は右へ
    """

    def __init__(self, root_key):
        self.root = node(root_key)
    
    def check(self):
        """
        赤黒木条件が壊れていないかを判定する
        :return: 0(壊れていない)/1(「赤の子は黒」が壊れている)/2(黒深さ条件が壊れている)
        """
        if self.root == None:
            return 0

        if self.root.color:
            stack = [(self.root, 0)]
        else:
            stack = [(self.root, 1)]

        depth = -1

        # 子がいないときはNone(共通で黒)であることに注意
        while stack:
            x, y = stack.pop()
            if x.left != None:
                if x.color and x.left.color:
                    return 1
                if x.left.color:
                    stack.append((x.left, y))
                else:
                    stack.append((x.left, y+1))
            else:
                # そのパスは探索終了なので, 黒深さが問題ないか調べる
                if depth == -1:
                    depth = y
                elif depth != y:
                    return 2
            
            if x.right != None:
                if x.color and x.right.color:
                    return 1
                if x.right.color:
                    stack.append((x.right, y))
                else:
                    stack.append((x.right, y+1))
            else:
                # そのパスは探索終了なので, 黒深さが問題ないか調べる
                if depth == -1:
                    depth = y
                elif depth != y:
                    return 2
        
        return 0


    def search(self, value):
        """
        指定されたkeyをもつノードを返す
        """
        x = self.root
        while x.key != value:
            if x.key > value:
                x = x.left
            else:
                x = x.right
            if x == None:
                return None
        
        return x
    
    def tree_max(self):
        x = self.root
        while x.right != None:
            x = x.right
        return x.key
    
    def tree_min(self):
        x = self.root
        while x.left != None:
            x = x.left
        return x.key

    def right_rotate(self, x):
        """
        xがx.parの左の子である場合に, xが親になるように回転
        xがx.parの左の子でないとバグるので注意
        """
        y = x.par
        if y == None or x != y.left:
            raise Exception
        
        b = x.right

        if y == self.root:
            self.root = x
            # xが根になったので, yの親はNoneになる
            x.par = None
        else:
            p = y.par
            x.par = p
            if y == p.left:
                p.left = x
            else:
                p.right = x
        
        x.right = y
        y.par = x

        y.left = b
        if b != None:
            b.par = y
        

    def left_rotate(self, y):
        """
        yがy.parの右の子である場合に, yが親になるように回転
        yがy.parの右の子でないとバグるので注意
        """
        x = y.par
        if x == None or y != x.right:
            raise Exception
        
        b = y.left

        if x == self.root:
            self.root = y
            # yが根になったので, yの親はNoneになる
            y.par = None
        else:
            p = x.par
            y.par = p
            if x == p.left:
                p.left = y
            else:
                p.right = y
        
        y.left = x
        x.par = y

        x.right = b
        if b != None:
            b.par = x
        
    
    def insert(self, key):

        if self.root == None:
            self.root = node(key)
            return

        # 挿入したノードx, xの親z
        x, z = self.normal_insert(key)

        while z.color:
            # zは常にx.parになるようにする
        
            # zが根の場合はzを黒にして終了
            if z == self.root:
                z.color = False
                break
            
            w = z.par

            # zの兄弟yを求める
            if z == w.left:
                y = w.right
            else:
                y = w.left
            
            # yはNoneかもしれない. Noneは黒であることに注意
            # yが赤の場合
            if y != None and y.color:
                w.color = True
                z.color = False
                y.color = False

                x = w
                # xが根の場合は親が定義できない(ため赤黒木条件を満たす)から終了
                if x == self.root:
                    break
                z = x.par
                continue # zが赤かもしれないので繰り返す
            
            # yが黒でzがwの左の子の場合
            elif z == w.left:
                # xが右の子の場合
                if x == z.right:
                    self.left_rotate(x)
                    x = z
                    z = x.par
                    # 次の場合に移る
                
                # xが左の子の場合(前の場合から移る可能性があるのでここはif)
                if x == z.left:
                    self.right_rotate(z)
                    z.color = False
                    w.color = True
            
            # yが黒でzがwの右の子の場合
            else:
                # xが左の子の場合
                if x == z.left:
                    self.right_rotate(x)
                    x = z
                    z = x.par
                    # 次の場合に移る

                # xが右の子の場合(前の場合から移る可能性があるのでここはif)
                if x == z.right:
                    self.left_rotate(z)
                    z.color = False
                    w.color = True

    def normal_insert(self, key):
        """
        :return: 挿入したノードのポインタy, yの親x
        """
        # 探索するノード
        x = self.root
        # 追加するノード
        y = node(key)

        while True:
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
        
        return y, x
    
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

    def rb_fix_delete(self, x):
        """
        子を1つノードもしくは持たないノードが削除された時に赤黒木条件を保つために処理を行う
        子を持たないノードを削除したときはxはNoneではなく, keyをNoneとしたノードになっているので, 
        あとでxを削除し, xの親からxへのポインタをNoneに変更する

        xは参照渡しで引数として渡されているが, 関数を出た後使わないのでコピーする必要なし
        (なんかコピーしたらバグった(?))
        """

        while True:
            # xが赤ならxを黒にして終了
            if x.color:
                x.color = False
                return

            # xの兄弟を求める
            p = x.par
            if x == p.left:
                w = p.right
            else:
                w = p.left
            
            # wがNoneだと仮定すると, 削除前の木が赤黒木条件を満たさないので, wはNoneではない

            # wが赤の場合
            if w.color:
                if x == p.left:
                    self.left_rotate(w)
                else:
                    self.right_rotate(w)
                w.color = False
                p.color = True

                # 2/17修正
                # xがpの左の子の場合(これはrotateしても変わってない)pの新しい右の子をwとして, 以下のいずれかの場合に推移する
                if x == p.left:
                    w = p.right
                # xがpの右の子の場合, pの新しい左の子をwとして, 以下のいずれかの場合に推移する
                else:
                    w = p.left
            
            # wの左右の子が黒
            if (w.left == None or (not w.left.color)) and (w.right == None or (not w.right.color)):
                w.color = True

                # x.keyがNoneだった場合, もう使わないのでpからxへのポインタをNoneにする
                if x.key == None:
                    if x == p.left:
                        p.left = None
                    else:
                        p.right = None
                    x.par = None

                # pを新たなxとして繰り返す
                # pが赤の場合は次のループで黒にされて即終了となる
                x = p
                continue
            
            # wの左の子が赤かつ右の子が黒
            if w.right == None or (not w.right.color):
                l = w.left
                l.color = False
                w.color = True

                self.right_rotate(l)
                # 場合4へ
            
            # wの右の子が赤
            if w.right != None and w.right.color:
                p = x.par
                w.color = p.color
                p.color = False
                w.right.color = False
                
                if x == p.left:
                    self.left_rotate(w)
                else:
                    self.right_rotate(w)
                
                # x.keyがNoneだった場合, もう使わないのでpからxへのポインタをNoneにする
                if x.key == None:
                    if x == p.left:
                        p.left = None
                    else:
                        p.right = None
                    x.par = None

                return

    
    def delete(self, x):
        """
        ノードxを削除する
        """
        # 子を持たない場合
        if x.left == None and x.right == None:
            if x.par == None:
                # 木の根がなくなり, 終了
                self.root = None
                return

            p = x.par
            # rb_fix_deleteをうまく動かすため, keyをNoneとした空のノードを用意する
            empty_node = node(None)
            empty_node.par = p
            empty_node.color = False
            if p.left == x:
                p.left = empty_node
            elif p.right == x:
                p.right = empty_node
            x.par = None
            
            # この場合で, かつ削除したノードの色が黒の場合は赤黒木条件を保存するようにする必要がある.
            if not x.color:
                self.rb_fix_delete(empty_node)
        
        # 子が一つだけある場合
        elif x.left == None or x.right == None:
            if x.left == None: 
                y = x.right
            else:
                y = x.left

            if x.par == None:
                self.root = y
                # xの子はyのみだったので, 赤黒木条件のための処理も必要ない
                return
            
            p = x.par
            if p.left == x:
                p.left = y
            elif p.right == x:
                p.right = y
            x.par = None
            y.par = p

            
            # この場合で, かつ削除したノードの色が黒の場合は赤黒木条件を保存するようにする必要がある. 
            if not x.color:
                self.rb_fix_delete(y)# yは根ではないので兄弟がいることに注意

        # 子が2つともある場合
        else:
            # 次節点yを持ってくる. yはその定義から左の子を持たない. 
            y = self.successor(x)
            self.delete(y)

            # xのところをyで置き換える.
            # keyはyの値にする
            pre_x_key = x.key
            x.key = y.key

            # 値の入れ替えを行うだけなので, 赤黒木条件を保存するための処理も必要ない
                
class node():

    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

        # 赤をTrue, 黒をFalseとする
        self.color = True

        # 親
        self.par = None


if __name__ == '__main__':

    import time

    start = time.time()

    T = RBT(4)
    T.insert(3)
    T.insert(5)
    T.insert(7)
    T.insert(6)
    T.insert(2)
    T.insert(1)
    T.insert(12)
    T.insert(8)

    r = T.root
    
    
    """
    # insertの検証
    r = T.root
    print(r.key)
    print(r.left.key)
    print(r.right.key)
    print(r.left.left.key)
    print(r.left.right.key)
    print(r.right.left.key)
    print(r.right.right.key)
    print(r.right.right.left.key)
    print(r.right.right.right.key)
    """

    T.delete(r.right)
    T.delete(r)

    # deleteの検証
    print(r.key)
    print(r.left.key)
    print(r.right.key)
    print(r.left.left.key)
    print(r.left.right.key)
    print(r.right.left.key)
    print(r.right.right.key)
    # print(r.right.right.right.key)

    T.insert(11)
    T.insert(4)
    T.delete(T.root.left.right)
    T.delete(T.root.right.right)

    print(r.key)
    print(r.left.key)
    print(r.right.key)
    print(r.left.left.key)
    print(r.left.right.key)
    print(r.right.left.key)
    print(r.right.right.key)

    # end = time.time()
    # print(end-start)# 0.0001499652862548828
