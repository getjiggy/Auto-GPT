import requests
from web3 import Web3

class EtherscanClient:
    key: str
    def __init__(self, key: str):
        self.key = key

    def getAbi(self, address: str):
        abi = None
        url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={Web3.to_checksum_address(address)}&apikey={self.key}"
        res = requests.get(url).json()
        if res["message"] == "OK":
            abi = res["result"]

        return abi
