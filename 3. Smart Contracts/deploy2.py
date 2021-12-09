import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from constants import PRIVATE_KEY, API_KEY

# web3.py instance
url = "https://ropsten.infura.io/v3/"+API_KEY
w3 = Web3(HTTPProvider(url))
print(w3.isConnected())

key = PRIVATE_KEY
acct = w3.eth.account.privateKeyToAccount(key)

# compile your smart contract with truffle
truffleFile = json.load(open('./build/contracts/NewContract.json'))

# initiating contract instance of truffle for deploying
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
contract = w3.eth.contract(bytecode = bytecode, abi = abi)

#building transaction
construct_txn = contract.constructor().buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 100000,
    'gasPrice': w3.toWei('1', 'gwei'),
    'chainId': 3})

# sign transaction with private key
signed = acct.signTransaction(construct_txn)

# send transaction on network
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash.hex())

# obtaining the deployed transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Deployed At:", tx_receipt['contractAddress'])
