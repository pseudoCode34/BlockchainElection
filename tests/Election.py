import json

from eth_typing import ChecksumAddress
from web3 import Web3

GANACHE = "HTTP://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(GANACHE))

"Run `brownie compile` to generate .json file from .sol"
truffle_file = json.load(open("../build/contracts/Election.json"))

abi = truffle_file["abi"]
bytecode = truffle_file["bytecode"]


def check_connected():
    print(f"Connected: {web3.is_connected()}")


def deployContract(owner) -> ChecksumAddress:
    election_contract = web3.eth.contract(bytecode=bytecode, abi=abi)
    tx_hash = election_contract.constructor().transact({"from": owner})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt.contractAddress


def get_info_of(contract_addr, id):
    election = web3.eth.contract(address=contract_addr, abi=abi)
    candidate = election.functions.getCandidate(id).call()
    print(
        f"Candidate ID: {candidate[0]}, Name: {candidate[1]}, Vote Count: {candidate[2]}"
    )


def total_vote(contract_addr):
    election = web3.eth.contract(address=contract_addr, abi=abi)
    print(election.functions.totalVote().call())


def vote(from_add, contract_addr, id):
    contract = web3.eth.contract(address=contract_addr, abi=abi)
    # transaction = contract.functions.vote(id).build_transaction(
    #     {
    #         "nonce": web3.eth.get_transaction_count(from_add),
    #         'value': 0,  # Ensure value is 0 for non-payable function
    #         'gas': 3_000_000,
    #         # See https://etherscan.io/gasTracker for setting gas
    #         # The higher gas is, the quicker the transaction happens. The lower, the longer
    #         # Can be applied to our local blockchain in ganache
    #         'gasPrice': web3.to_wei(15, 'gwei'),
    #     })
    # signed_tx = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = contract.functions.vote_for(id).transact(
        {
            "from": from_add,
            "gas": 3_000_000,
        }
    )
    print(f"Transaction successful with hash: {tx_hash.hex()}")


from_addr = web3.to_checksum_address(
    "0xD3e2773d6810E623F8518659DA0C03FFAB278046"
)
pvt = "0x77b5529cf19f180c8b06caac444d0152454a40d63077adc157a71c060338823a"
check_connected()

addr = deployContract(from_addr)
# contract_add = web3.to_checksum_address("0x6ACf886C0a85F5B88d66EA0317aB7a16Fe066b67")
# tx_hash = "0x7e86206bd60836a35884ff3c35bdc28b2f70d39d216387cb77bce0d572523ce6"

# vote(from_addr, contract_add,3)
# for i in range(1, 4):
#     get_info_of(contract_add, i)
# total_vote(contract_add)

import pytest


def test_contract():
    # Load deployed contract (assumes ABI and address are known)
    contract_address = "0x10bed1993de4528da0e1a8D92E0265e61dEd48E4"

    contract = web3.eth.contract(address=contract_address, abi=abi)

    # Perform some tests on the contract
    result = contract.functions.get_candidate(0).call()[2]
    print(result)


if __name__ == "__main__":
    pytest.main()
