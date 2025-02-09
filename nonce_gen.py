import hashlib

def le(n: bytes) -> bytes:
    return hashlib.sha256(n).digest()

def ue(c: bytes) -> str:
    return ''.join(f'{b:02x}' for b in c)

def generate_nonce(c: str, e: int) -> int:
    s = 0
    d = '0' * e
    while True:
        n = f"{s}{c}".encode()
        if ue(le(n)).startswith(d):
            return s
        s += 1

