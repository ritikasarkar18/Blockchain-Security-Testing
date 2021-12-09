import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from constants import PRIVATE_KEY, API_KEY

# web3.py instance
url = "https://ropsten.infura.io/v3/"+API_KEY
w3 = Web3(HTTPProvider(url))
print(w3.isConnected())

# compile your smart contract with truffle
truffleFile = json.load(open('./build/contracts/NewContract.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# deployed contract address
contract_address = Web3.toChecksumAddress("<deployed address>")

# Instantiate and deploy contract
#contract = w3.eth.contract(abi = abi, bytecode = bytecode)

# Contract instance
contract_instance = w3.eth.contract(abi = abi, address = contract_address)
print(contract_instance.functions.getexp().call())
