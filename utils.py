import binascii

from mnemonic import Mnemonic
from substrateinterface import Keypair, KeypairType
import hashlib


class ProsopoAccount:
    def __init__(self):
        mnemo = Mnemonic("english")
        mnemonic_phrase = mnemo.generate(strength=256)
        self.keypair = Keypair.create_from_mnemonic(mnemonic_phrase, crypto_type=KeypairType.SR25519)

    @property
    def public_key(self):
        return self.keypair.ss58_address

    def signMessage(self, message: str) -> bytes:
        message_bytes = message.encode('utf-8')
        signature = self.keypair.sign(message_bytes)

        return signature


def generate_nonce(c: str, e: int) -> int:
    s = 0
    d = '0' * e
    while True:
        n = f"{s}{c}".encode()
        hashed = hashlib.sha256(n).digest()
        hexed = binascii.hexlify(hashed).decode()

        if hexed.startswith(d):
            return s

        s += 1
