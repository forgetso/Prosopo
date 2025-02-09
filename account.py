from substrateinterface import Keypair
from mnemonic import Mnemonic
from sr25519_utils import *

class ProsopoAccount:
    def __init__(self):
        mnemo = Mnemonic("english")
        mnemonic_phrase = mnemo.generate(strength=256)

        self.keypair = Keypair.create_from_mnemonic(mnemonic_phrase, crypto_type=KeypairType.SR25519)
        self.sender_keypair: Keypair = Keypair.create_from_mnemonic(
            mnemonic=mnemonic_phrase,
            crypto_type=KeypairType.SR25519
        )

    @property
    def public_key(self):
        return self.sender_keypair.ss58_address

    def signMessage(self, message: str) -> list[int]:
        """
        Signs the provided message using the account's SR25519 private key.

        Args:
            message (str): The message to be signed.

        Returns:
            str: The signature as a hexadecimal string.
        """
        # Encode the message to bytes (assuming UTF-8 encoding)
        message_bytes = message.encode('utf-8')

        # Sign the message. Depending on the implementation,
        # `sign` may return bytes or a hex string.
        signature = self.sender_keypair.sign(message_bytes)


        return list(signature)