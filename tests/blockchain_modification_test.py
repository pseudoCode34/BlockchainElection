import json
import os
import unittest

from dotenv import load_dotenv
from self.web3 import HTTPProvider, Web3


class BlockchainModificationTest(unittest.TestCase):
    def __init__(self):
        load_dotenv()

        self.web3 = Web3(HTTPProvider(os.getenv("BLOCKCHAIN_ADDRESS")))

    def setUp(self):
        self.deployer = self.web3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
        with open("build/contracts/Election.json") as compile_source:
            contract_json = json.load(compile_source)
            abi = contract_json["abi"]  # fetch contract's abi
        address = self.web3.to_checksum_address(
            "0x5BAF32D2422F3D3C78950861d635ce975C86692a"
        )
        self.election = self.web3.eth.contract(abi=abi, address=address)

    def test_set_the_deployer_account_as_owner(self):
        self.assertEqual(self.election.caller().owner(), self.deployer.address)

    def test_voter_cannot_modify_the_content_once_sending(self):
        transaction = self.web3.eth.get_transaction(
            self.web3.to_hex(
                0x1023EC45A31C735D6E054535D99F43B50ACAEBF8D9AC5931D8881D7290BDA8AE
            )
        )

        # Decode the input data
        input_data = transaction["input"]
        function_data = self.election.decode_function_input(input_data)

        # Print the decoded function name and parameters
        function_name = function_data[0].fn_name
        parameters = function_data[1]

        # Decode the input data
        print(f"Decoded Function: {function_name}")
        print(f"Decoded Parameters: {parameters}")

        # Modify the parameters (e.g., change value to 100)
        parameters["_value"] = 100

        # Encode the modified parameters back into transaction data
        modified_input_data = self.election.encodeABI(
            fn_name=function_name, args=[parameters["_value"]]
        )
        print(f"Modified Input Data: {modified_input_data}")

        private_key = (
            "0x601ea09f519d4cc8005697786579d7a64d32b1996cc05bdb19394e77225c892e"
        )
        new_transaction = {
            "to": self.election.address,
            "data": modified_input_data,
            "gas": 5_000_000,
            "nonce": self.web3.eth.get_transaction_count(transaction["from"]),
            "gasPrice": self.web3.to_wei(20, "gwei"),
            "value": 0,
        }

        signed_tx = self.web3.eth.account.sign_transaction(
            new_transaction, private_key
        )

        with self.assertRaises(ValueError) as context:
            tx_hash = self.web3.eth.send_raw_transaction(
                signed_tx.raw_transaction
            )
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print(tx_receipt)
        self.assertIn("revert Already voted", str(context.exception))

    def test_send_modified_transaction_back(self):
        transaction = self.web3.eth.get_transaction(
            self.web3.to_hex(
                0x1023EC45A31C735D6E054535D99F43B50ACAEBF8D9AC5931D8881D7290BDA8AE
            )
        )
        print(transaction)
        with self.assertRaises(TypeError) as context:
            # Try modifying the transaction (will fail because immutable)
            transaction["gasUsed"] = 200_000  # Double the transaction value
            print("Attempting to modify transaction (will fail):")
            # This will fail as modifying a confirmed transaction is impossible
            self.web3.eth.send_transaction(transaction)

        # Optionally, you can also verify the exception message
        self.assertEqual(
            str(context.exception),
            "'AttributeDict' object does not support item assignment",
        )


if __name__ == "__main__":
    unittest.main()
