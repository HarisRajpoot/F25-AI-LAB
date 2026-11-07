import math
c = 0   # leaf counter

def minimax(d, i, mx, s, t):
    global c
    if d == t:
        c += 1
        return s[i]
    a = minimax(d+1, i*2, not mx, s, t)
    b = minimax(d+1, i*2+1, not mx, s, t)
    return max(a, b) if mx else min(a, b)

def alphabeta(d, i, mx, s, t, al, be):
    global c
    if d == t:
        c += 1
        return s[i]
    v = -math.inf if mx else math.inf
    for k in range(2):
        r = alphabeta(d+1, i*2+k, not mx, s, t, al, be)
        if mx:
            v = max(v, r); al = max(al, v)
        else:
            v = min(v, r); be = min(be, v)
        if al >= be:
            break
    return v

for s in ([3,5,2,9,3,5,2,9], [5,3,9,2,5,3,9,2], [2,9,3,5,2,9,3,5], [4]*8):
    t = int(math.log2(len(s)))
    c = 0
    m = minimax(0, 0, True, s, t)

    c1 = c
    c = 0
    a = alphabeta(0, 0, True, s, t, -math.inf, math.inf)
    print(s, m, c1, a, c)