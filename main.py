import telebot
from web3 import Web3
import time


TELEGRAM_BOT_TOKEN = '6775443880:AAE0RhxESCup7zyyCLnu2hrX7cjPd_-QypY'
stop_flag = False

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/bc2ee063a84741f3babf0e1dacf46e7d'))

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Enter wallet to monitor it')
#getting information about last block using web3 library
def get_latest_block_number():
    return w3.eth.block_number

#filtering useful parameters from all infromation from whole block
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

#getting the wallet balance and updating it if balance is changed
def check_wallet_balance(wallet_address, previous_balance, message):
    current_balance = w3.eth.get_balance(wallet_address)
    
    if current_balance != previous_balance:
        balance_change = current_balance - previous_balance
        balance_change_in_ether = w3.from_wei(abs(balance_change), 'ether')
        bot.send_message(message.chat.id,f"""Balance change detected: {balance_change_in_ether} ether\nCurrent Balance: {w3.from_wei(abs(current_balance), 'ether')} ether""")
        return True
    
        
    return False


def check_wallet_activity(wallet_address):
    latest_block_number = get_latest_block_number()

    for block_number in range(latest_block_number, max(0, latest_block_number - 10), -1):
        transaction_info = get_transaction_info(block_number, wallet_address)
        
        if transaction_info:
            return transaction_info
    return None    
        
#function that allows user to stop monitoring current wallet so user can add another wallet
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    global stop_flag
    bot.reply_to(message, 'Enter a new wallet')
    bot.send_message(message.chat.id, 'Enter adress to monitor it')
    stop_flag = True  


@bot.message_handler(content_types=['text'])   
def main_work(message):
    '''
    Returns: None
    Parameters: - message (telegram.Message): The incoming Telegram message that triggers the wallet monitoring.
                - stop_flag (bool): A global flag indicating whether to stop the monitoring loop.
        
    The function sets up a continuous monitoring loop for an Ethereum wallet. It checks the balance and
    activity of the specified wallet and sends notifications if there are changes. The monitoring loop
    continues until the global stop_flag is set to True.
    '''
    global stop_flag
    stop_flag = False 
    if len(message.text.strip().upper()) != 42:
        bot.send_message(message.chat.id, 'This is not an ETH address')
    bot.reply_to(message, 'Monitoring this wallet')    
    wallet_address = message.text.strip()
    previous_balance = w3.eth.get_balance(wallet_address)
    transaction_info = ''
    while not stop_flag:
            if check_wallet_balance(wallet_address, previous_balance, message):
                previous_balance = w3.eth.get_balance(wallet_address)
            if transaction_info != check_wallet_activity(wallet_address, message) and check_wallet_activity(wallet_address, message) != None:
                transaction_info = check_wallet_activity(wallet_address, message)
                bot.send_message(message.chat.id, f"""Wallet activity detected in block: {transaction_info['block_number']}\nFrom: {transaction_info['from']}\nTo: {transaction_info['to']}\nValue: {transaction_info['value']} Ether""")
            time.sleep(12)
    

if __name__ == "__main__":
    

    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print ("Program has ended by user")