import os

from dotenv import load_dotenv
from solcx import compile_source
from web3 import Web3
from requests.exceptions import ConnectionError
load_dotenv()
web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_ADDRESS")))

if web3.is_connected():
    print("Connected to Ethereum node")
else:
    raise ConnectionError("Failed to connect")

with open("contracts/Election.sol", "r") as contract_file:
    contract_source_code = compile_source(contract_file.read())
    contract_id, contract_interface = contract_source_code.popitem()

    bytecode = contract_interface["bytecode"]
    abi = contract_interface["abi"]

    w3 = Web3(Web3.EthereumTesterProvider())
    w3.eth.default_account = w3.eth.accounts[0]
    Election = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx_hash = Election.constructor().transact()

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
