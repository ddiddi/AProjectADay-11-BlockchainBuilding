
import hashlib
import json
from textwrap import dodent
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

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

app = Flask(__name__)

# Generate unique address
node_id = str(uuid4()).replace('-', '')

# Instantiate blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_id,
        amount=1,
    )

    # Forge the new block and append to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New block forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check required fields
    required = ['sender', 'recipient', 'amount']
    if not all(i in values for i in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def chain():
    response = {
    'chain':blockchain.chain,
    'length':len(blockchain.chain)
    }
return jsonify(response), 200

if __name__ = '__main__':
    app.run(host='0.0.0.0', port=5000)
