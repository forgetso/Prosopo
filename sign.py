import math

yi = [f"{i:02x}" for i in range(256)]

Tp = [None] * (256 * 256)
for e in range(256):
    base = e << 8  # equivalent to e * 256
    for n in range(256):
        Tp[base | n] = yi[e] + yi[n]


def Hs(e, t):
    n = len(e) % 2
    r = len(e) - n
    for o in range(0, r, 2):
        t += Tp[(e[o] << 8) | e[o + 1]]
    if n:
        t += yi[e[r]]
    return t


def custom_hex(e, t=-1):
    prefix = "0x"
    if e is not None and len(e):
        if t > 0:
            o = math.ceil(t / 8)
            if len(e) > o:
                first_part = Hs(e[:int(o / 2)], prefix)
                second_part = Hs(e[len(e) - int(o / 2):], "")
                return first_part + "…" + second_part
    else:
        return prefix
    return Hs(e, prefix)

