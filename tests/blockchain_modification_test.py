import unittest

from web3 import Web3


class BlockchainModificationTest(unittest.TestCase):
    def setUp(self):
        # Connect to Ganache
        ganache_url = "http://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        self.tx_hash = "0xda835209813acc8b160abd86a8c65a78f9e65386ab5d412e0af2c20a9f524172"

    def test_send_modified_transaction_back(self):
        # Get transaction information
        try:
            tx = self.web3.eth.get_transaction_receipt(self.tx_hash)
            if tx is None:
                print("Transaction not found")
            else:
                print("Transaction hash:", tx.transactionHash.hex())
                print("Block number:", tx.blockNumber)

        except Exception as e:
            print("Error fetching transaction:", e)

        with self.assertRaises(TypeError) as context:
            # Try modifying the transaction (will fail because immutable)
            tx["gasUsed"] = tx["gasUsed"] * 2  # Double the transaction value
            print("Attempting to modify transaction (will fail):")
            # This will fail as modifying a confirmed transaction is impossible
            self.web3.eth.send_transaction(tx)

            # Optionally, you can also verify the exception message
            self.assertEqual(str(context.exception),
                             "'AttributeDict' object does not support item assignment")


if __name__ == '__main__':
    unittest.main()
