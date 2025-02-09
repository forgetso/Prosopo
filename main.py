import requests
from account import ProsopoAccount
from fingerprint import generate_token
from sign import custom_hex
from nonce_gen import generate_nonce

sitekey = "5C7bfXYwachNuvmasEFtWi9BMS41uBvo6KpYHVSQmad4nWzw"

account = ProsopoAccount()

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/120.0",
    "Accept": "*/*",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://prosopo.io/",
    "Content-Type": "application/json",
    "Prosopo-Site-Key": sitekey,
    "Prosopo-User": account.public_key,
    "Origin": "https://prosopo.io",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=4"
}

payload = {
    "token": generate_token(),
    "dapp": sitekey,
    "user": account.public_key,
}

res = session.post("https://pronode12.prosopo.io/v1/prosopo/provider/client/captcha/frictionless", json=payload)

print(res.text)

payload = {
    "user": account.public_key,
    "dapp": sitekey,
    "sessionId": res.json()["sessionId"],
}

res = session.post("https://pronode12.prosopo.io/v1/prosopo/provider/client/captcha/pow", json=payload)
print(res.text)
pow_challenge = res.json()

timestamp = pow_challenge["timestamp"]

hexed = custom_hex(list(timestamp.encode('utf-8')))

solved = account.signMessage(hexed)
print(account.public_key)

payload = {
    "challenge": pow_challenge["challenge"],
    "difficulty": pow_challenge["difficulty"],
    "timestamp": pow_challenge["timestamp"],
    "signature": {
        "user": {
            "timestamp": custom_hex(solved),
        },
        "provider": {
            "challenge": pow_challenge["signature"]["provider"]["challenge"]
        },
    },
    "user": account.public_key,
    "dapp": sitekey,
    "nonce": generate_nonce(pow_challenge["challenge"], pow_challenge["difficulty"]),
    "verifiedTimeout": 120000
}
print(payload)
res = session.post("https://pronode12.prosopo.io/v1/prosopo/provider/client/pow/solution", json=payload)
print(res.text)
