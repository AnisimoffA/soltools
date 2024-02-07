from django.urls import path
from wallets.views import *


urlpatterns = [
    path('list/', WalletsList.as_view(), name="wallets_list"),
    path('<int:pk>/delete/', WalletsDelete.as_view(), name="wallets_delete"),
    path('show_private_key/', get_wallet_balance, name='get_wallet_balance'),
    path('add/', WalletsAdd.as_view(), name="wallets_add"),
    path('create/', WalletsCreate.as_view(), name="wallets_create"),
    path('transfer/', WalletsTransfer.as_view(), name='wallets_transfer'),
    path('transfer-confirm/', WalletsTransferConfirm.as_view(), name='wallets_transfer_confirm'),
    path('transfer-confirm/accept/', WalletsTransferAccept.as_view(), name='wallets_transfer_accept'),
    path('download/', download_txt, name='download_txt'),
]
