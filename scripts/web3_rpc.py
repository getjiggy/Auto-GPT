from web3 import Web3

from config import Config
from eth_abi import encode, decode
from  pprint import PrettyPrinter
from etherscan_client import EtherscanClient
pp = PrettyPrinter()
cfg = Config()

#todo refactor so chain id directs which infura url to use
def rpc_request(address: str, rpc_method: str, rpc_method_args: [], rpc_method_arg_types: []):
    w3 = Web3(Web3.HTTPProvider(cfg.infura_url,))
    address = Web3.to_checksum_address(address)
    if rpc_method.find('(') == -1 and rpc_method.find(")") == -1:
        values = ''
        for i in rpc_method_arg_types:
            values += i + ','

        rpc_method = rpc_method + "(" + values[:-1] + ")"
        print(rpc_method)
    else:
        return "only supply the method name"
    sig = Web3.to_hex(Web3.keccak(text=rpc_method)[:4])

    # attempt to get abi
    etherscan = EtherscanClient(cfg.etherscan_key)
    abi = etherscan.getAbi(address=address)
    pp.pprint(abi)

    if abi:
        contract = w3.eth.contract(address=address, abi=abi)
        func = contract.functions[rpc_method[:rpc_method.index('(')]]
        resp = func(rpc_method_args).call() if len(rpc_method_args) else func().call()

    else:
        data = sig + Web3.to_hex(encode(rpc_method_arg_types, rpc_method_args))[2:]
        resp = Web3.to_hex(w3.eth.call({
            "to": address,
            "value": 0,
            "gas": 3000000,
            "data": data
        }))

    return resp



