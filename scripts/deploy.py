import json
import os

from web3 import Web3

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_ADDRESS")))

# Check if connected
if w3.is_connected():
    print("Connected to Ethereum node")
else:
    print("Failed to connect")

# Set default account
w3.eth.default_account = w3.eth.accounts[0]

# Read ABI and Bytecode

with json.load(open(os.getenv("COMPILED_CONTRACT_FILE"), 'r')) as contract_json:
    abi = contract_json["abi"]  # fetch contract's abi
    bytecode = contract_json["bytecode"]

# Deploy contract
Storage = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Storage.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract deployed at address: {tx_receipt.contractAddress}")

# Interact with the contract
storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
