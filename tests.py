import unittest
from unittest.mock import MagicMock, patch
from main import get_latest_block_number, check_wallet_balance

class TestYourCode(unittest.TestCase):

    def test_get_latest_block_number(self):
        # Test if get_latest_block_number returns a valid block number
        with patch('main.w3') as mock_w3:
            mock_w3.eth.block_number = 123
            block_number = get_latest_block_number()
            self.assertIsInstance(block_number, int)
            self.assertGreater(block_number, 0)


    def test_check_wallet_balance(self):
        # Test check_wallet_balance function with mocked web3 calls
        with patch('main.w3') as mock_w3, patch('main.bot.send_message') as mock_send_message:
            mock_w3.eth.get_balance.return_value = 200
            previous_balance = 100
            message = MagicMock()
            result = check_wallet_balance('0x123', previous_balance, message)
            self.assertTrue(result)
            mock_send_message.assert_called_once()



if __name__ == '__main__':
    unittest.main()
