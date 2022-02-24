"""
赤黒木
rootが変更されると困るのでやっぱりclassとして用意しておいたほうが良さそう. 
デバッグ用問題: ARC033 C 

TODO:　left_rotateとright_rotateは統一できそう
TODO: ノードを木から消去する時に消去ノードxの子yに対してy.parを消去するのを忘れてる, かも
        -> 根かどうかの判定は == self.rootでやったほうがよい
TODO: totalの計算で根の判定を.par == Noneでやっているところがある. 

更新履歴
    2021/09/05
    * successorのバグを修正（赤黒木に対する操作は問題ないが，外部から利用するとバグった）
    * checkをcheck_redblackに名前変更，check_binary_treeを追加
"""
import copy

class RBT():
    """
    「以下」の場合は左へ, 「より大きい」の場合は右へ
    """

    def __init__(self, root_key=0, empty_tree=False):
        if empty_tree:
            self.root = None
            return
        self.root = node(root_key)
    
    def check_redblack(self):
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
    
    def check_binary_tree(self):
        """
        2分木条件（大小に関する条件がこわれていないかを確認する．
        :return: 壊れていればFalse, 壊れていなければTrueを出力
        """
        x = self.root
        stack = []
        while stack:
            y = stack.pop()
            if y.left != None:
                if y.left.key > y.key:
                    return False
                stack.append(y.left)
            if y.right != None:
                if y.right.key < y.key:
                    return False
                stack.append(y.right)
        return True


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
        if self.root == None:
            return None
        x = self.root
        while x.right != None:
            x = x.right
        return x.key
    
    def tree_min(self):
        if self.root == None:
            return None
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
            p = x.par
            if x == p.left:
                pass
            else:
                xx = p
                p = xx.par
                while xx == p.right:
                    assert p.key <= xx.key# WA
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

                    # x.keyがNoneだった場合, もう使わないのでx.parからxへのポインタをNoneにする
                    if x.key == None:
                        p = x.par
                        if x == p.left:
                            p.left = None
                        else:
                            p.right = None
                        x.par = None

                    return
                
                # xが根の場合も, xを含む葉へのパスは全てのパスだから, 黒深さが1減っていても
                # 問題ないので終了
                if x == self.root:
                    return

                # xの兄弟を求める
                p = x.par
                if x == p.left:
                    w = p.right
                else:
                    w = p.left
                
                # wがNoneだと仮定すると, 削除前の木が赤黒木条件を満たさないので, wはNoneではない
                # wがNoneになるときがあるとすれば, そのときはxもNone(empty_node)
                # empty_nodeを消去し, x.parを新たなxとして繰り返す
                if w == None:
                    if x.key != None:
                        raise Exception
                    elif x == p.left:
                        p.left = None
                    else:
                        p.right = None
                    x.par = None
                    x = p
                    continue

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
                
                # xが左の子のとき
                if x == x.par.left:
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
                        
                        self.left_rotate(w)
                        
                        # x.keyがNoneだった場合, もう使わないのでpからxへのポインタをNoneにする
                        if x.key == None:
                            if x == p.left:
                                p.left = None
                            else:
                                p.right = None
                            x.par = None

                        return
                
                # xが右の子のとき
                if x == x.par.right:
                    # wの右の子が赤かつ左の子が黒
                    if w.left == None or (not w.left.color):
                        r = w.right
                        r.color = False
                        w.color = True

                        self.left_rotate(r)
                        # 場合4へ
                    
                    # wの左の子が赤
                    if w.left != None and w.left.color:
                        p = x.par
                        w.color = p.color
                        p.color = False
                        w.left.color = False
                        
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
            if x == self.root:
                # 木の根がなくなり, 終了
                self.root = None
                return

            p = x.par
            # 削除するノードが赤の場合は, xとpの間のエッジを削除して終了
            if x.color:
                if p.left == x:
                    p.left = None
                else:
                    p.right = None
                x.par = None

            else:

                # 削除するノードの色が黒の場合は赤黒木条件を保存するようにする必要がある.
                # rb_fix_deleteをうまく動かすため, keyをNoneとした空のノードを用意する
                empty_node = node(None)
                empty_node.par = p
                empty_node.color = False
                if p.left == x:
                    p.left = empty_node
                elif p.right == x:
                    p.right = empty_node
                x.par = None
            
                self.rb_fix_delete(empty_node)
        
        # 子が一つだけある場合
        elif x.left == None or x.right == None:
            if x.left == None: 
                y = x.right
            else:
                y = x.left

            if x == self.root:
                self.root = y
                y.par = None
                if x.left == y:
                    x.left = None
                else:
                    x.right = None
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

def display_rbt(T, depth = 4):
    """
    赤黒木をいい感じに出力する
    :param depth: 推測される高さ。実際には1段余分に出力. 
    """
    from collections import deque
    q = deque([T.root])
    count = 1
    line = 1
    
    while count <= 2**(depth+1)-1:
        if count == 2**(line-1):
            print('--- line {} ---'.format(line))
            line += 1
        x = q.popleft()
        try:
            print(x.key, x.color)
            q.append(x.left)
            q.append(x.right)
        except:
            print(None)
            q.append(None)
            q.append(None)
        count += 1


if __name__ == '__main__':

    import time

    num = 55

    import random
    import time
    seed1 = pow(2, int(time.time()), 1093646546841)
    random.seed(seed1)
    I = list(range(num))
    random.shuffle(I)

    T = RBT(I[0])

    for x in I[1:]:
        T.insert(x)

    display_rbt(T)

    for x in range(num):
        print('DELETE: ', x)
        T.delete(T.search(x))
        print('CONDITION CHECK: ', T.check_redblack(), T.check_binary_tree())
        assert T.check_redblack() == 0 and T.check_binary_tree()
        display_rbt(T)
        T.insert(x)

    for x in range(num):
        for y in range(x+1, num):
            print('-- before delete --')
            display_rbt(T)
            
            print('DELETE: ', x, y)
            T.delete(T.search(x))
            T.delete(T.search(y))

            print('-- after delete --')
            display_rbt(T)

            print('CONDITION CHECK: ', T.check_redblack(), T.check_binary_tree())
            if T.check_redblack() > 0:
                print('SEED: ', seed1)
                raise Exception
            assert T.check_binary_tree()
            T.insert(x)
            T.insert(y)
    
    for x in range(num):
        for y in range(x):
            print('-- before delete --')
            display_rbt(T)

            print('DELETE: ', x, y)
            T.delete(T.search(x))
            T.delete(T.search(y))

            print('-- after delete --')
            display_rbt(T)

            print('CONDITION CHECK: ', T.check_redblack(), T.check_binary_tree())
            if T.check_redblack() > 0:
                print('SEED: ', seed1)
                raise Exception
            assert T.check_binary_tree()
            T.insert(x)
            T.insert(y)
    
    seed2 = pow(2, int(time.time()), 936435837)
    random.seed(seed2)
    random.shuffle(I)
    for x in I:
        print('DELETE: ', x)
        T.delete(T.search(x))
        display_rbt(T)
        print('CONDITION CHECK: ', T.check_redblack(), T.check_binary_tree())
        if T.check_redblack() > 0:
            print('SEED: ', seed1, seed2)
        assert T.check_binary_tree()
    
    print('Check has finished correctly. ')
    print('SEED: ', seed1, seed2)
