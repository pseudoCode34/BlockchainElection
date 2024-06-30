import json
import os
import unittest

from dotenv import load_dotenv
from web3 import HTTPProvider, Web3

load_dotenv()

web3 = Web3(HTTPProvider(os.getenv("BLOCKCHAIN_ADDRESS")))


class BlockchainModificationTest(unittest.TestCase):
    def setUp(self):
        self.deployer = web3.eth.accounts[0]

        with open(os.getenv("COMPILED_CONTRACT_FILE")) as compile_source:
            contract_json = json.load(compile_source)
            abi = contract_json["abi"]  # fetch contract's abi

        address = web3.to_checksum_address(
                web.to_hex(os.getenv("CONTRACT_ADDRESS")
        )
        self.election = web3.eth.contract(abi=abi, address=address)

    def test_set_the_deployer_account_as_owner(self):
        self.assertEqual(self.election.caller().owner(), self.deployer)

    def modified_vote(self):
        transaction = web3.eth.get_transaction(
            web3.to_hex( # A transaction hash 
                        )
        )

        # Decode the input data
        input_data = transaction["input"]
        function_data = self.election.decode_function_input(input_data)

        function_name = function_data[0].fn_name
        parameters = function_data[1]

        print(f"Decoded Function: {function_name}")
        print(f"Decoded Parameters: {parameters}")

        parameters["_value"] = 100

        # Encode the modified parameters back into transaction data
        modified_input_data = self.election.encodeABI(
            fn_name=function_name, args=[parameters["_value"]]
        )
        print(f"Modified Input Data: {modified_input_data}")

        return {
            "to": self.election.address,
            # "from": transaction["from"],
            "data": modified_input_data,
            "gas": 1_000_000,
            "nonce": web3.eth.get_transaction_count(transaction["from"]),
            "gasPrice": web3.to_wei(100, "gwei"),
            "value": 0,
        }

    def test_voter_cannot_modify_the_content_once_sending(self):
        private_key = "0x601ea09f519d4cc8005697786579d7a64d32b1996cc05bdb19394e77225c892e"
        signed_tx = web3.eth.account.sign_transaction(
            self.modified_vote(),private_key
        )

        with self.assertRaises(ValueError) as context:
            tx_hash = web3.eth.send_raw_transaction(
                signed_tx.raw_transaction
            )
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(tx_receipt)
        self.assertIn("revert Already voted", str(context.exception))

    def test_send_modified_transaction_back(self):
        transaction = web3.eth.get_transaction(
            web3.to_hex(
                # A transaction hash
            )
        )
        print(transaction)
        with self.assertRaises(TypeError) as context:
            # Try modifying the transaction (will fail because immutable)
            transaction["gasUsed"] = 200_000  # Double the transaction value
            print("Attempting to modify transaction (will fail):")
            # This will fail as modifying a confirmed transaction is impossible
            web3.eth.send_transaction(transaction)

        # Optionally, you can also verify the exception message
        self.assertEqual(
            str(context.exception),
            "'AttributeDict' object does not support item assignment",
        )

    def test_other_cannot_modify_my_vote(self):
        signed_tx = web3.eth.account.sign_transaction(
            self.modified_vote(), 
            # A user private key
        )

        with self.assertRaises(ValueError) as context:
            tx_hash = web3.eth.send_raw_transaction(
                signed_tx.raw_transaction
            )
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(tx_receipt)


if __name__ == "__main__":
    unittest.main()
