from solders.keypair import Keypair
from config import RPC
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction

wallets = {'8Rqxuo1jqp8KjNZ4p9dFtgg8QfQ2pjpsRAWVfuaXoNz2': {'private_key': b'\xe7\xb9\xd3C\xc5\x12\x00\xb6\t7\xcb\x0c\xbb\xc1YK\x9c\xbf\xf8\xb8e\xecT\t:3\xfc\x96\xfc\xe1\x7f\xed', 'public_key': b'n_\x1c\x94`\x99h \x1a:8\xc9;\xb9\x149J\xa3B\x9b;\xd8\x98\xff\x97\xf7\xcc\xc1\xb3\xd9\xcb\x8f'}, 'Drrd395ACjNc3UBZvthZrLGdPvc3EReiph9GMQezXZC7': {'private_key': b'w-\xcb\x9e\xc8\xea\xa5\xf0h\x05N5\r1\x0b,\xeaC\x0c\xa1f7t9NI\x913\xed\xd0\xb9\x8b', 'public_key': b'\xbf\x11\xcfMA\x87\xf8\x8d\xc6\xeci\x8fs\x907\x1e<\x81\x04\xd9Y\xa5\xae4#_\xc9\xe8Y\xeci$'}}

first = wallets['8Rqxuo1jqp8KjNZ4p9dFtgg8QfQ2pjpsRAWVfuaXoNz2']['private_key']
second = wallets['Drrd395ACjNc3UBZvthZrLGdPvc3EReiph9GMQezXZC7']['private_key']

sender, receiver = Keypair.from_seed(first), Keypair.from_seed(second)


txn = Transaction().add(transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=receiver.pubkey(), lamports=10000000)))

solana_client = Client(RPC)

try:
    result = solana_client.send_transaction(txn, sender).value
    print(f"Transaction confirmed. Transaction hash: {result}")
except Exception as e:
    print(f"Transaction failed: {e}")