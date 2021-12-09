from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date


node = Flask(__name__)


# The Block class to define the structure of the block
class Block:
  def __init__(self, index, timestamp, data, previous_hash):
      self.index = index
      self.timestamp = timestamp
      self.data = data
      self.previous_hash = previous_hash
      self.hash = self.hash_block()
  
  def hash_block(self):
      sha = hasher.sha256()
      seq = [
              str(x) for x in [self.index, self.timestamp, self.data, self.previous_hash]
          ]
      sha.update("".join(seq).encode("utf8"))
      return sha.hexdigest()



def create_genesis_block():
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), {
      "proof-of-work": 9,
      "transactions": None
    }, "0")



#-------------Global variables needed------------------#
# Generate genesis block
# A completely random address of the owner of this node
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
# This node's blockchain copy
blockchain = []
blockchain.append(create_genesis_block())
# Store the transactions that
# this node has in a list
this_nodes_transactions = [] 
# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []
# A variable to deciding if we're mining or not
mining = True
#-------------------------------------------------------#


# to make a new transaction, use this route
@node.route('/txion', methods=['POST'])
def transaction():
    # On each new POST request,
    # we extract the transaction data from request object
    new_txion = request.get_json()
    # Then store the transaction
    this_nodes_transactions.append(new_txion)
    # Because the transaction was successfully
    # submitted, we log it to server console
    print("New transaction")
    print("FROM: {}".format(new_txion['from'].encode('ascii','replace')))
    print("TO: {}".format(new_txion['to'].encode('ascii','replace')))
    print("AMOUNT: {}\n".format(new_txion['amount']))
    # Then we let the client know it worked out
    return "Transaction submission successful\n"


# to get a list of all the blocks in the blockchain, use this route
@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = consensus()
    chain = []
    # Convert our blocks into dictionaries
    # so we can send them as json objects later
    for i in range(len(chain_to_send)):
        block = chain_to_send[i] # extracting a block object
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        chain.append({
          "index": block_index,
          "timestamp": block_timestamp,
          "data": block_data,
          "hash": block_hash
        })
    chain_to_send = json.dumps(chain, indent=4, sort_keys=True)
    return chain_to_send



#-------------------Helper functions-------------------#
def find_new_chains():
    # Get the blockchains of every
    # other node
    # other_chains = []
    # for node_url in peer_nodes:
    #     # Get their chains using a GET request
    #     block = requests.get(node_url + "/blocks").content
    #     # Convert the JSON object to a Python dictionary
    #     block = json.loads(block)
    #     # Add it to our list
    #     other_chains.append(block)
    # return other_chains

    ret = []
    for peer in peer_nodes:
        response = requests.get('http://%s/blocks' % peer)
        if response.status_code == 200:
            print("blocks from peer: " + response.content)
            ret.append(json.loads(response.content))
    return ret


def consensus():
    global blockchain
    # Get the blocks from other nodes
    other_chains = find_new_chains()
    # If our chain isn't longest,
    # then we store the longest chain
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    # If the longest chain isn't ours,
    # then we stop mining and set
    # our chain to the longest one
    
    blockchain = longest_chain
    return blockchain


def proof_of_work(last_proof):
    # Create a variable that we will use to find
    # our next proof of work
    incrementor = last_proof + 1
    # Keep incrementing the incrementor until
    # it's equal to a number divisible by 9
    # and the proof of work of the previous
    # block in the chain
    while not (incrementor % 18 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    # Once that number is found,
    # we can return it as a proof
    # of our work
    return incrementor

#-------------End of Helper functions---------------#


@node.route('/add_peer', methods=['GET'])
def add_peer():
    host = request.args['host'] if 'host' in request.args else 'localhost'
    port = request.args['port']
    peer = host + ':' + port
    peer_nodes.append(peer)
    print("Peer added: %s" % peer)
    return ""


# to mine a new a block, use this route
@node.route('/mine', methods = ['GET'])
def mine():
    # Get the last proof of work
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']
    # Find the proof of work for
    # the current block being mined
    # Note: The program will hang here until a new
    #       proof of work is found
    proof = proof_of_work(last_proof)
    # Once we find a valid proof of work,
    # we know we can mine a block so 
    # we reward the miner by adding a transaction
    this_nodes_transactions.append(
      { "from": "network", "to": miner_address, "amount": 1 }
    )
    # Now we can gather the data needed
    # to create the new block
    new_block_data = {
      "proof-of-work": proof,
      "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    # Empty transaction list
    this_nodes_transactions[:] = []
    # Now create the
    # new block!
    mined_block = Block(
      new_block_index,
      new_block_timestamp,
      new_block_data,
      last_block_hash
    )
    
    blockchain.append(mined_block)
    # Let the client know we mined a block
    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }, indent=4, sort_keys=True) + "\n"



if __name__ == "__main__":
    # will listen on localhost 5000
    port = 5000
    node.run(port = port)
