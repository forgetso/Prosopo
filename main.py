import requests, binascii
from utils import ProsopoAccount, generate_nonce
from fingerprint import generate_token


class Prosopo:
    def __init__(self, host: str, site_key: str):
        self.site_key = site_key
        self.account = ProsopoAccount()

        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/120.0",
            "Accept": "*/*",
            "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
            "Referer": f"{host}/",
            "Content-Type": "application/json",
            "Prosopo-Site-Key": self.site_key,
            "Prosopo-User": self.account.public_key,
            "Origin": host,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=4"
        }

    def solve(self):
        # response = self.session.get("https://https://pronode4old.prosopo.io.prosopo.io/test")

        payload = {
            "token": generate_token(),
            "dapp": self.site_key,
            "user": self.account.public_key,
        }

        res = self.session.post("https://staging-pronode2.prosopo.io/v1/prosopo/provider/client/captcha/frictionless",
                                json=payload)

        print(res.text)

        if(res.status_code != 200):
            print(res.status_code)
            return

        payload = {
            "user": self.account.public_key,
            "dapp": self.site_key,
            "sessionId": res.json()["sessionId"],
        }

        res = self.session.post("https://staging-pronode2.prosopo.io/v1/prosopo/provider/client/captcha/pow", json=payload)

        if(res.status_code != 200):
            print(res.status_code)
            return

        pow_challenge = res.json()

        solved = self.account.signMessage(pow_challenge["timestamp"])

        payload = {
            "challenge": pow_challenge["challenge"],
            "difficulty": pow_challenge["difficulty"],
            "signature": {
                "user": {
                    "timestamp": "0x" + binascii.hexlify(solved).decode(),
                },
                "provider": {
                    "challenge": pow_challenge["signature"]["provider"]["challenge"]
                },
            },
            "user": self.account.public_key,
            "dapp": self.site_key,
            "nonce": generate_nonce(pow_challenge["challenge"], pow_challenge["difficulty"]),
            "verifiedTimeout": 120000
        }

        res = self.session.post("https://staging-pronode2.prosopo.io/v1/prosopo/provider/client/pow/solution", json=payload)
        print(res.text)


if __name__ == "__main__":
    Prosopo("https://prosopo.io", "5GYr811LSaCUP4JmDDKBaY56ZSCAXDkQXxoBdnmuwurHThvP").solve()
