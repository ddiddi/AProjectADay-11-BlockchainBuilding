
import hashlib
import json
from time import time
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block in the Blockchain
        :param proof: <int> The proof from the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous block
        :return: <dict> New block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # Reset the current transaction list
        self.current_transactions = []
        # Append block
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction for the next mined block
        :param sender: <str> Sender address
        :param recipient: <str> Recipient address
        :param amount: <int> Amount
        :return: <int> Transaction block index
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        - Find proof p' such that (with proof  p as previous p'), hash(pp') has leading '1234'
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates proof
        :param last_proof: <int> Previous proof
        :param proof: <int> Proof
        :return: <bool> True if valid
        """
        guess=f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] = "1234"

    @staticmethod
    def hash(block):
        # Compute hash of a block
        pass

    @property
    def last_block(self):
        # Return the last block
        return self.chain[-1]
