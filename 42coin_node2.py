import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []

        self.transactions = []
        self.create_block(proof=1, previous_hash='0')

        self.nodes = set()
        

    def add_nodes(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        print(parsed_url.netloc)
    def replace_chain(self):        
        network = self.nodes
        print(len(network))        
        longest_chain = None        
        max_length = len(self.chain)    
        print(max_length)
        for node in network:            
            response = requests.get(f'http://{node}/chain')            
            print(node)
            print(response.status_code)            
            json_obj = response.json()
            if isinstance(json_obj,dict):
                print("hey")
                if "length" in json_obj:
                    print(json_obj["length"])
                if "chain" in json_obj:
                    print(json_obj["chain"])
            if response.status_code == 200:                
                length = json_obj["length"]
                print(length)                
                chain = json_obj["chain"]
                print(chain)

                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            if longest_chain:
                self.chain =longest_chain
                return True
            return False
            
            
    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chain)+1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash,
                 'transactions':self.transactions}
        self.transactions = []
        self.chain.append(block)

        return block
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender':sender,'receiver':receiver,'amount':amount})
        previous_block = self.get_previous_block()
        
        return previous_block['index']+1

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation.endswith('4242'):
                
                hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

                
                check_proof = True
                
            else:
                
                new_proof +=1            
        return new_proof
        
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, block):
        previous_block = self.chain[0]
        block_index=1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if not hash_operation.endswith('4242'):
                return False
            
            previous_block=block
            block_index +=1

        return True
   
app = Flask(__name__)

node_address = str(uuid4()).replace('-','')


blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender= node_address, receiver='Ale', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message':'Felicidades, has minado un bloque!',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash'],
                'transactions':block['transactions']}
    for node in blockchain.nodes:
        print(type(node))
        requests.get(url=f'http://{node}/replace_chain')    
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message':'Todo bien. El Blockchain es valido'}
    else:
        response = {'message':'Something went wrong. El Blockchain no es valido'}
    return jsonify(response), 200

@app.route('/transactions/new', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender','receiver','amount']
    
    if not all (key in json for key in transaction_keys):
        return 'Some elements are missing', 400
        
    index = blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'message':f'The transaction will be added to the block {index}'}
    return jsonify(response), 201

@app.route('/connect_node',methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node', 401
    for node in nodes:
        blockchain.add_nodes(node)
    response = {'message':'The connection of the nodes is established.','total_nodes':list(blockchain.nodes)}
    return jsonify(response), 201 
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message':'The nodes had diferents chains so the chain was replaced by the longest one',
                    'new_chain':blockchain.chain}
    else:
        response = {'message':'Everything is ok. The chain is the longest one',
                    'actual_chain':blockchain.chain}
    return jsonify(response), 200
app.run(host='0.0.0.0', port='5002',debug=True)
