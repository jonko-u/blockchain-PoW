Here's the Python code with comments translated to English:

```python
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Press the green button in the gutter to run the script.
# class Block
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
class Blockchain:
    def __init__(self):
        self.chain = []
        # First, add transactions to create the blockchain
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        # Second, add nodes
        self.nodes = set()

    def get_nodes(self):
        return self.nodes

    # address will be the address and port of our node
    def add_nodes(self, address):
        # Using the URL parser from the urllib library to verify that the address is correct
        parsed_url = urlparse(address)
        # Then, add it to our nodes set using .add()
        self.nodes.add(parsed_url.netloc)
        print(parsed_url.netloc)

    def replace_chain(self):
        # We define the network as the set of nodes we obtained when adding nodes
        network = self.nodes
        print(len(network))
        # Set the longest_chain variable to None because we haven't checked the length of each node's blockchain yet
        longest_chain = None
        # Define the maximum length of our blockchain
        max_length = len(self.chain)
        # Iterate through all nodes using a for loop within our network
        print(max_length)
        for node in network:
            # Send a request to get the chain status as follows
            response = requests.get(f'http://{node}/chain')

            print(node)
            print(response.status_code)
            # print(response.json(['length']))
            json_obj = response.json()
            if isinstance(json_obj, dict):
                if "length" in json_obj:
                    print(json_obj["length"])
                if "chain" in json_obj:
                    print(json_obj["chain"])
                # for key in response.json:

            # print(response.json(['chain']))
            # If we get a 200 status code, we are on the right track
            if response.status_code == 200:
                # Response is a JSON type in which we will look for the values
                # length and chain to check which one is the longest and then replace all nodes with the predominant one

                length = json_obj["length"]
                print(length)

                chain = json_obj["chain"]
                print(chain)
                # If the length is greater than max_length and the chain is valid
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            # If there is a longest chain
            if longest_chain:
                self.chain = longest_chain
                return True
            return False

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        # Reset this list to be empty to avoid duplicates
        self.transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})

        # Get the index of the previous block
        previous_block = self.get_previous_block()

        return previous_block['index'] + 1

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:

            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # print(hash_operation)
            if hash_operation.endswith('4242'):

                hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

                check_proof = True

            else:

                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, block):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]

            # Check if the previous hash in the current block does not match the original hash of the previous block
            if block['previous_hash'] != self.hash(previous_block):
                return False

            # Check if the resultant hash of the proof**2 - previous_proof**2 does not have 4 leading 0s
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if not hash_operation.endswith('4242'):
                return False

            # Update the block and increase the index
            previous_block = block
            block_index += 1
        return True

app = Flask(__name__)

node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']

    proof = blockchain.proof_of_work(previous_proof)

    previous_hash = blockchain.hash(previous_block)
    # Now we'll add one more key to our blockchain dictionary that will hold our transactions
    blockchain.add_transaction(sender=node_address, receiver='jon', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you have mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}


    for node in blockchain.nodes:
        print(type(node))
        requests.get(url=f'http://{node}/replace_chain')
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Check the validity of the blockchain
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Everything is fine. The Blockchain is valid'}
    else:
        response = {'message': 'Something went wrong. The Blockchain is not valid'}
    return jsonify(response), 200

# Add a new transaction to the blockchain.
@app.route('/transactions/new', methods=['POST'])
def add_transaction():
    # Get the JSON from our request
    json_data = request.get_json()
    # Then, through a predefined list (transaction key), we will parse the JSON and get the sender, receiver, and amount
    transaction_keys = ['sender', 'receiver', 'amount']
    # We will parse the JSON and get the sender, receiver, and the amount (amount)
    if not

 all(key in json_data for key in transaction_keys):
        return 'Some elements are missing', 400

    index = blockchain.add_transaction(json_data['sender'], json_data['receiver'], json_data['amount'])
    response = {'message': f'The transaction will be added to the block {index}'}
    return jsonify(response), 201

# Connect the new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json_data = request.get_json()
    nodes = json_data.get('nodes')
    print(nodes)
    # Let's check that our nodes are not empty
    if nodes is None:
        return 'No node', 401
    for node in nodes:
        blockchain.add_nodes(node)
    response = {'message': 'The connection of the nodes is established.', 'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# We will replace the chain with the longest chain we have obtained
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    print(is_chain_replaced)
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains, so the chain was replaced by the longest one',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'Everything is ok. The chain is the longest one',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200

app.run(host='0.0.0.0', port='5001', debug=True)
```

Please note that the code comments have been translated to English, and no code modifications have been made. If you have any questions or need further assistance, feel free to ask!