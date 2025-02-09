import random

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64, time, math, json


# RSA-OAEP

def encrypt(plaintext: str) -> str:
    public_key_b64 = """
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoa1QCkVvFAfv+fgFpjfq
    9/YrtGzDYull6V0oiy1XPuTCQeb4uptHEmCepnZPmKaP/akp5wS7UTGYw+or//gd
    IER2Cs58q7tVvqxTe68mx901oSw61VOt7mqDVhIsnJlH6yo2Kd9a5rClU/xr618K
    Ry0wuoD2i6mq4fE3uKZZBNrxJ57Jg0EXEsMIvYHxk0kKO8i0YIxEVP84tUuZiq9T
    dcponzr4ny6lqn0YlOSu67kRVL8O0ryHvRJomNN4OcUgq/rUfzJxonqvvmHd75n4
    4r8n4Y7I8/DmVe9cpDWDgv6vk2djRkAQDiLfDEMfq8C7S+/8RPyLTCxXUrR2ouUG
    6QIDAQAB
    """
    public_key_b64 = "".join(public_key_b64.split())
    key_der = base64.b64decode(public_key_b64)

    public_key = serialization.load_der_public_key(key_der)

    ciphertext = public_key.encrypt(
        plaintext.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(ciphertext).decode("utf-8")


def generate_token():
    current_time = int(time.time() * 1000)
    tmp = ((int(str(current_time)[-3:]) + (random.random() * 0.3)) / 999) * math.pi - math.pi / 2
    out = json.dumps([current_time, math.sin(tmp) * 1000], separators=(',', ':'))
    return encrypt(out)
