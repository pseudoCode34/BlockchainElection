import os

from dotenv import load_dotenv
from solcx import compile_source
from web3 import Web3
load_dotenv()
# Connect to Ganache
web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_ADDRESS")))

# Check if connected
if web3.is_connected():
    print("Connected to Ethereum node")
else:
    print("Failed to connect")

# Set default account
web3.eth.default_account = web3.eth.accounts[0]
with open("../contracts/Election.sol", "r") as contract_file:
    contract_source_code = contract_file.read()

    compiled_sol = compile_source(source=contract_source_code)
    contract_interface = compiled_sol["<stdin>:Election"]

    # Get the bytecode and ABI
    bytecode = contract_interface["bin"]
    abi = contract_interface["abi"]

    # Set up the account
    account = web3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

    # Deploy contract
    Election = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Election.constructor().transact(
        {"nonce": web3.eth.get_transaction_count(account)}
    )
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Contract deployed at address: {tx_receipt}")
