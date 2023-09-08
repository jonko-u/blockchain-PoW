# Development of a Simple Blockchain

## Introduction

This project focuses on creating a simple blockchain that allows transactions and block mining. A basic Proof of Work (PoW) algorithm is used to ensure the integrity of the blockchain. The blockchain is kept in memory and is not connected to a specific database. Users can interact with the blockchain through HTTP requests to add transactions and mine new blocks.


## Screenshots

![intro](/screenshots/screenshot.png)


## Development in Python and Used Modules

To develop this blockchain, the Python programming language was used along with various modules that facilitated the creation of the application. The modules used include:

- **Blinker (1.6.2)**: It was used for event and signal management in the Flask application, facilitating communication between different components of the blockchain.

- **Certifi (2023.7.22)**: This module ensures security in communication through SSL/TLS by including trusted certificates.

- **Charset-Normalizer (3.2.0)**: Used to normalize and manage characters in blockchain transactions and data.

- **Click (8.1.7)**: Used to create custom command-line commands and the command-line interface of the application.

- **Flask (2.3.3)**: Flask is the web development framework used to build the blockchain's interface and handle HTTP requests.

- **Idna (3.4)**: Aids in managing internationalized domain names in transactions.

- **Itsdangerous (2.1.2)**: Used to generate and verify security tokens in the Flask application.

- **Jinja2 (3.1.2)**: Template engine used to render web pages for the user interface.

- **MarkupSafe (2.1.3)**: Ensures security in HTML content generation and prevents code injection attacks.

- **Requests (2.31.0)**: Used to make HTTP requests when interacting with the blockchain through the API.

- **Urllib3 (2.0.4)**: Used to manage HTTP connections in requests made through the API.

- **Werkzeug (2.3.7)**: This module is a fundamental component of Flask and is responsible for handling routes, requests, and HTTP responses.

## Usage/Examples

## Screenshots

![postman](/screenshots/screenshot1.png)


Its loaded on python 3.11.4
Firstly, download the repo
```
git clone https://github.com/jonko-u/blockchain-PoW
```

```
cd blockchain-PoW
```
Install the modules
```
pip install -r requirements.txt
```
Deploy 3 nodes as default
```
python exec.py
```
Connect the nodes between them
```
python node_connection.py
```
Done.

- /chain - gets the length of the chain and its values.
- /mine - mine a new block.
- /add_transaction - add a new transaction to the next block.
- /is_valid - checks if the blockchain is valid.
- /replace_chain - it replaces all the chains by the longest one


## Bonus - Impact of Blockchain on the World

Blockchain has had a significant impact on the world in key areas such as cryptography and cybersecurity. Its influence extends beyond cryptocurrencies and has become a disruptive technology in the following aspects:

### 1. Cryptography

Blockchain employs strong cryptographic principles to ensure data security and integrity. It has driven advancements in cryptography, including:

- **Secure Cryptocurrencies**: Cryptocurrencies like Bitcoin have demonstrated the viability of secure and decentralized digital money systems based on cryptographic algorithms.

- **Digital Signatures**: Digital signatures are crucial in blockchain to verify the authenticity of transactions. This technology has increased trust in digital transactions.

- **Consensus Algorithms**: Consensus algorithms like PoW and PoS use cryptography to ensure the integrity of the blockchain and prevent malicious attacks.

### 2. Cybersecurity

Blockchain has improved cybersecurity in several ways:

- **Data Immutability**: Once a block is added to the chain, it is extremely difficult to modify. This ensures that data stored in the chain is immutable and resistant to tampering.

- **Decentralization**: The inherent decentralization of blockchain reduces vulnerability points and makes it more challenging for attackers to compromise the network.

- **Transaction Security**: Transactions on the blockchain are transparent and auditable, making it easier to detect fraudulent activity.

In summary, blockchain has transformed how we store and share data, driven advances in cryptography, and enhanced cybersecurity. As it continues to evolve, it is likely to have a significant impact on various industries and applications worldwide.
