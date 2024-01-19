from web3 import Web3
import time
from decimal import Decimal


w3 = Web3(Web3.HTTPProvider('key'))


wallet_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

def get_latest_block_number():
    return w3.eth.block_number

def get_transaction_info(block_number, wallet_address):
    block = w3.eth.get_block(block_number, full_transactions=True)
    
    for tx in block.transactions:
        if (tx['to'] and wallet_address.lower() == tx['to'].lower()) or \
           (tx['from'] and wallet_address.lower() == tx['from'].lower()):
            return {
                'from': tx['from'],
                'to': tx['to'],
                'value': w3.from_wei(tx['value'], 'ether'),
                'block_number': block_number
            }

    return None

def check_wallet_balance(wallet_address, previous_balance):
    current_balance = w3.eth.get_balance(wallet_address)
    
    if current_balance != previous_balance:
        balance_change = current_balance - previous_balance
        print(f"Balance change detected: {balance_change} Wei")
        print(f"Current Balance: {current_balance} Wei")
    
    return current_balance


def check_wallet_activity(wallet_address):
    latest_block_number = get_latest_block_number()

    for block_number in range(latest_block_number, max(0, latest_block_number - 10), -1):
        transaction_info = get_transaction_info(block_number, wallet_address)
        
        if transaction_info:
            print(f"Wallet activity detected in block {transaction_info['block_number']}:")
            print(f"From: {transaction_info['from']}")
            print(f"To: {transaction_info['to']}")
            print(f"Value: {transaction_info['value']} Ether")
            return
        else:
            print("none activity detected in block")
            return

    print("No recent activity found for the wallet.")

if __name__ == "__main__":
    try:
        previous_balance = w3.eth.get_balance(wallet_address)

        while True:
            check_wallet_activity(wallet_address)
            previous_balance_wei = check_wallet_balance(wallet_address, previous_balance)
            time.sleep(12) 
    except KeyboardInterrupt:
        print("Program stopped by user.")
