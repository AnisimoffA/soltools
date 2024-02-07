from django.db import models
from users.models import CustomUsers
from base58 import b58encode, b58decode
from webtools.settings import RPC
from solders.pubkey import Pubkey
from solana.rpc.api import Client

# Create your models here.
class Wallets(models.Model):
    owner = models.ForeignKey(
        CustomUsers,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        related_name="owner",
        null=True
    )
    key = models.CharField(max_length=100000, verbose_name="key", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    def get_private_key(self):
        decoded_keypair = b58decode(self.key)
        private_key = decoded_keypair[:32]
        return private_key

    def get_public_key(self):
        decoded_keypair = b58decode(self.key)
        public_key = decoded_keypair[32:]
        return public_key

    def get_wallet_address(self):
        wallet_address = b58encode(self.get_public_key()).decode()
        return wallet_address

    def get_wallet_balance(self):
        client = Client(RPC)
        balance = client.get_balance(Pubkey(self.get_public_key())).value / 1000000000
        return balance

    def __str__(self):
        return self.get_wallet_address()