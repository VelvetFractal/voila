from web3 import Web3
import time

w3 = Web3(Web3.HTTPProvider('key'))

wallet_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

def get_latest_block_number():
    return w3.eth.block_number

def get_transaction_info(block_number, wallet_address):
    block = w3.eth.get_block(block_number, full_transactions=True)
    
    for tx in block.transactions:
        if wallet_address.lower() == tx['to'].lower() or wallet_address.lower() == tx['from'].lower():
            return {
                'from': tx['from'],
                'to': tx['to'],
                'value': w3.from_wei(tx['value'], 'ether'),
                'block_number': block_number
            }

    return None

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
            print(f"none activity detected in block {transaction_info['block_number']}")
            return

    print("No recent activity found for the wallet.")

if __name__ == "__main__":
    try:
        while True:
            check_wallet_activity(wallet_address)
            time.sleep(12)  
    except KeyboardInterrupt:
        print("Program stopped by user.")

def 