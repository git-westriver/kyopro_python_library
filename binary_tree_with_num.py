"""
接点に番号をつけた2分探索木
追加順とかも知りたい時は便利かも
いやでもその場合もnodeにnumberとかの情報持たせればいいのでいらないかも

未完成
"""

class binary_tree():
    """
    「以下」の場合は左へ, 「より大きい」の場合は右へ
    """

    def __init__(self, root_key):
        # 接点の数
        self.N = 1
        self.nodes = {0: node(root_key)}

    def insert(self, key):
        # 挿入する節点の番号
        num = self.N
        self.nodes[num] = node(key)

        # 節点数を1増やす
        self.N += 1

        # 現在のノード
        x = self.nodes[0]
        while True:
            if key <= x.key and x.left == None:
                x.left = num
                break
            elif key <= x.key:
                x = self.nodes[x.left]
            elif key > x.key and x.right == None:
                x.right = num
                break
            else:
                x = self.nodes[x.right]



class node():

    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right