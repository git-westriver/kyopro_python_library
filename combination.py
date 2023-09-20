def cmb(n, r):
    if (r < 0) or (n < r):
        return 0
    r = min(r, n - r)
    return fact[n] * factinv[r] * factinv[n-r] % mod

mod = 10 ** 9 + 7
num = 10 ** 6  # num は必要分だけ用意する
fact = [1, 1]  # fact[n] = (n! % mod)
factinv = [1, 1]  # factinv[n] = ((n!)^(-1) % mod)
inv = [0, 1]  # factinv 計算用
 
for i in range(2, num + 1):
    fact.append((fact[-1] * i) % mod)
    inv.append((-inv[mod % i] * (mod // i)) % mod)
    factinv.append((factinv[-1] * inv[-1]) % mod)

print(cmb(100, 10, mod))