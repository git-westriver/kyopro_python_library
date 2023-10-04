"""
コード：https://tjkendev.github.io/procon-library/python/convex_hull_trick/li_chao_tree.html
参考：https://smijake3.hatenablog.com/entry/2018/06/16/144548
"""
class LiChaoTree:
    """
    X: 参照する座標 N 個を入れる
    """
    def __init__(self, X):
        N = len(X)
        self.N0 = 2**(N-1).bit_length()
        self.data = [None]*(2*self.N0+1)
        self.X = [10**10]*self.N0 # N0に持つ座標N個を入れる
        for i in range(N):
            self.X[i] = X[i]

    def _f(self, line, x):
        p, q = line
        return p*x + q

    def _add_line(self, line, k, l, r):
        m = (l + r) // 2
        if self.data[k] is None:
            self.data[k] = line
            return
        lx = self.X[l]; mx = self.X[m]; rx = self.X[r-1]
        left = (self._f(line, lx) < self._f(self.data[k], lx))
        mid = (self._f(line, mx) < self._f(self.data[k], mx))
        right = (self._f(line, rx) < self._f(self.data[k], rx))
        if left and right:
            self.data[k] = line
            return
        if not left and not right:
            return
        if mid:
            self.data[k], line = line, self.data[k]
        if left != mid:
            self._add_line(line, 2*k+1, l, m)
        else:
            self._add_line(line, 2*k+2, m, r)

    def add_line(self, line, a=None, b=None):
        if a is None:
            # 直線のみに対応する場合のadd_line: O(log N)
            return self._add_line(line, 0, 0, self.N0)
        else:
            # 線分に対応する場合のadd_line: O(log^2 N)
            L = a + self.N0; R = b + self.N0
            a0 = a; b0 = b
            sz = 1
            while L < R:
                if R & 1:
                    R -= 1
                    b0 -= sz
                    self._add_line(line, R-1, b0, b0+sz)
                if L & 1:
                    self._add_line(line, L-1, a0, a0+sz)
                    L += 1
                    a0 += sz
                L >>= 1; R >>= 1
                sz <<= 1

    def query(self, k):
        x = self.X[k]
        k += self.N0-1
        s = 1e30
        while k >= 0:
            if self.data[k]:
                s = min(s, self._f(self.data[k], x))
            k = (k - 1) // 2
        return s

### EDPC-Z ###
N, C = map(int, input().split())
H = list(map(int, input().split()))

lct = LiChaoTree(H)
dp = [0]*N
lct.add_line((-2*H[0], dp[0] + H[0]**2 + C))
for i in range(1, N):
    dp[i] = H[i] ** 2 + lct.query(i)
    lct.add_line((-2*H[i], dp[i] + H[i]**2 + C))

print(dp[-1])