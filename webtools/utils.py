from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction
from solana.rpc.api import Client
from webtools.settings import RPC, FEE
from wallets.models import Wallets
import base58


menu = [
    {'title': 'Создать кошельки', 'url_name': 'wallets_create'},
    {'title': 'Добавить кошельки', 'url_name': 'wallets_add'},
    {'title': 'Список кошельков', 'url_name': 'wallets_list'},
    {'title': 'Отправить солану', 'url_name': 'wallets_transfer'},
    {'title': "Вход", 'url_name': 'login'},
    {'title': "Регистрация", 'url_name': 'register'},
    {'title': "Профиль", 'url_name': 'user_page'},
    {'title': "Выход", 'url_name': 'logout'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        if self.request.user.is_authenticated:
            user_menu.pop(4)
            user_menu.pop(4)

        if not self.request.user.is_authenticated:
            user_menu.pop(0)
            user_menu.pop(0)
            user_menu.pop(0)
            user_menu.pop(0)
            user_menu.pop(3)

        context['menu'] = user_menu
        return context


class CustomUserPermisionsMixin:
    def has_permissions(self):
        print(self.get_object().username)
        return self.get_object().username == self.request.user.username

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            messages.warning(
                request,
                "У вас нет прав для изменения другого пользователя."
            )
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


def sol_transfer(request, sender, receiver, amount):
    solana_client = Client(RPC)

    if len(sender) == 1 and len(receiver) >= 1:
        sender_1 = Keypair.from_seed(sender[0].get_private_key())

        if sender[0].get_wallet_balance() * 1000000000 < (FEE + 50000):
            messages.warning(
                request,
                "Кошелек пустой"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_transfer'))

        if amount == 0:
            amount = int(sender[0].get_wallet_balance()*1000000000 / len(list(receiver))) - FEE

        try:
            for rec in receiver:
                receiver_1 = Keypair.from_seed(rec.get_private_key())
                txn = Transaction().add(transfer(TransferParams(
                    from_pubkey=sender_1.pubkey(),
                    to_pubkey=receiver_1.pubkey(),
                    lamports=amount)
                ))
            result = solana_client.send_transaction(txn, sender_1).value
            print(f"[TRANS ONE2MANY] Transaction confirmed. Transaction hash: {result}")
        except Exception as e:
            messages.warning(
                request,
                "Что-то пошло не так"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_transfer'))
        else:
            messages.success(
                request,
                "Переводы успешно осуществлены"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_transfer'))

    elif len(sender) > 1 and len(receiver) == 1:
        receiver_1 = Keypair.from_seed(receiver[0].get_private_key())

        try:
            for send in list(sender):
                if amount != 0:
                    if send.get_wallet_balance() * 1000000000 < amount + FEE:
                        continue
                if amount == 0:
                    if send.get_wallet_balance() * 1000000000 < FEE + 500000:
                        continue
                    amount = int(send.get_wallet_balance() * 1000000000 - FEE)

                sender_1 = Keypair.from_seed(send.get_private_key())
                txn = Transaction().add(transfer(TransferParams(
                    from_pubkey=sender_1.pubkey(),
                    to_pubkey=receiver_1.pubkey(),
                    lamports=amount)
                ))
                result = solana_client.send_transaction(txn, sender_1).value
                print(f"[TRANS MANY2ONE] Transaction confirmed. Transaction hash: {result}")
        except Exception as e:
            print(e)
            messages.warning(
                request,
                "Что-то пошло не так"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_transfer'))
        else:
            messages.success(
                request,
                "Переводы успешно осуществлены"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_transfer'))

def generate_wallets(request, owner, amount):
    try:
        for x in range(amount):
            key = Keypair()
            Wallets.objects.create(owner=owner, key=str(key))
    except:
        messages.warning(
            request,
            "Что-то пошло не так"
        )
        return HttpResponseRedirect(reverse_lazy('wallets_list'))
    else:
        messages.success(
            request,
            "Кошельки успешно созданы"
        )
        return HttpResponseRedirect(reverse_lazy('wallets_list'))


