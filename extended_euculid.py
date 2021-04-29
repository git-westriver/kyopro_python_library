'''
https://qiita.com/DaikiSuyama/items/3687e9f2fa3ed097e2fc#fnref3
よりコピペ
＜注意＞
一般解を求めるとき, mの係数はもとのa, bではなく, a/g, b/gになる
LDE.a, LDE.bを用いれば良い
'''

'''
二元一次不定方程式 ax+by=c(a≠0かつb≠0) を解く
初期化すると、x=x0+m*b,y=y0-m*aで一般解が求められる(m=0で初期化)
'''
from math import gcd
class LDE:
    #初期化
    def __init__(self,a,b,c):
        self.a,self.b,self.c=a,b,c
        self.m,self.x,self.y=0,[0],[0]
        #解が存在するか
        self.check=True
        g=gcd(self.a,self.b)
        if c%g!=0:
            self.check=False
        else:
            #ax+by=gの特殊解を求める
            self.extgcd(abs(self.a),abs(self.b),self.x,self.y)
            if a<0:self.x[0]=-self.x[0]
            if b<0:self.y[0]=-self.y[0]
            #ax+by=cの特殊解を求める
            self.x=self.x[0]*c//g
            self.y=self.y[0]*c//g
            #一般解を求めるために
            self.a//=g
            self.b//=g

    #拡張ユークリッドの互除法
    #返り値:aとbの最大公約数
    def extgcd(self,a,b,x0,y0):
        if b==0:
            x0[0],y0[0]=1,0
            return a
        d=self.extgcd(b,a%b,y0,x0)
        y0[0]-=(a//b)*x0[0]
        return d

    #パラメータmの更新(書き換え)
    def m_update(self,m):
        self.x+=(m-self.m)*self.b
        self.y-=(m-self.m)*self.a
        self.m=m

if __name__ == '__main__':
    L = LDE(2, 3, 1)
    print(L.check)
    # L.x, L.y: 特殊解
    # 一般解はx = L.x + m * L.b,y = L.y - m * L.a
    print(L.x, L.y, L.a, L.b)

    L = LDE(5, 25, 8)
    print(L.check)
    print(L.x, L.y, L.a, L.b)

    L = LDE(5, 25, 10)
    print(L.check)
    print(L.x, L.y, L.a, L.b)