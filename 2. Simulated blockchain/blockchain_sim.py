import hashlib
import time

#each block’s hash will be a cryptographic hash of the block’s index, timestamp, data, and the hash of the previous block’s hash
class Block:
    # type annotations have been used to force data types
    def __init__(self, index: int, timestamp: int, data: str, previous_hash):
        """
        :param index: block index
        :param timestamp: millisecond
        :param data: block real data
        :param previous_hash: previous block hash
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256() #creating a SHA-256 hash object
        seq = [
            str(x) for x in [self.index, self.timestamp, self.data, self.previous_hash]
        ]
        #feed this object with bytes-like objects (normally bytes) using the update() method
        sha.update("".join(seq).encode("utf8"))
        return sha.hexdigest() #rendering the hash value(message digest) as hex

    #called when the block object is passed to print() method
    def __str__(self):
        return f"Block:index={self.index}&timestamp={self.timestamp}&data={self.data}&hash={self.hash}"


def get_cur_millisecond():
    return int(round(time.time() * 1000))


# the first block - special - index 0
def create_genesis_block():
    return Block(0, get_cur_millisecond(), "genesis block", "0")


#generating the other blocks
def next_block(previous_block: Block):
    # using previous hash as this chain of hashes acts as cryptographic proof 
    # and helps ensure that once a block is added to the blockchain it cannot be replaced or removed.
    index = previous_block.index + 1
    return Block(
        index = index,
        timestamp = get_cur_millisecond(),
        data = f"this is block #{index}",
        previous_hash = previous_block.hash,
    )


#creating the blockchain as a list
def make_test_block_chain():
    block_chain = [create_genesis_block()]
    previous_block = block_chain[0]
    for _ in range(20): #creating 20 blocks
        block = next_block(previous_block)
        block_chain.append(block)
        previous_block = block
        # broadcast to others
        print(f"Block #{block.index} has been added to the blockchain! detail: {block}")
        time.sleep(1)


if __name__ == "__main__":
    make_test_block_chain()
