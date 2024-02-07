from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View, TemplateView # NOQA E501
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import RestrictedError
from django.contrib import messages
from django.db import IntegrityError, transaction
from webtools.utils import *
from wallets.models import *
from wallets.forms import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.core.serializers import serialize
from django.core.cache import cache


class WalletsList(LoginRequiredMixin, DataMixin, ListView):
    model = Wallets
    template_name = "wallets/wallets_list.html"
    context_object_name = "wallets"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Кошельки")
        return context | c_def

    def get_queryset(self):
        return Wallets.objects.filter(owner_id=self.request.user.id)


class WalletsAdd(LoginRequiredMixin, DataMixin, CreateView):
    form_class = WalletsForm
    template_name = 'wallets/wallets_add.html'
    login_url = reverse_lazy('wallets_list')
    raise_exception = True

    def form_valid(self, form):
        keys_text = form.cleaned_data['key']
        keys_list = keys_text.split('\r\n')
        try:
            with transaction.atomic():
                for key in keys_list:
                    key = key.strip()
                    if key:
                        if len(key) < 87 or len(key) > 88:
                            raise ValueError
                        else:
                            Wallets.objects.create(owner=self.request.user, key=key)

        except IntegrityError:
            messages.warning(
                self.request,
                "Один или несколько кошельков уже используются"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_create'))
        except ValueError:
            messages.warning(
                self.request,
                "Неверный формат одного или нескольких кошельков"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_create'))

        return super().get(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Создание кошельков")
        return context | c_def

    def get_success_url(self):
        messages.success(
            self.request,
            "Wallets was created successfully"
        )
        return reverse_lazy('wallets_list')


class WalletsCreate(DataMixin, TemplateView):
    template_name = 'wallets/wallets_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AmountOfWallets()
        object_list = Wallets.objects.all()

        c_def = self.get_user_context(title="Wallets creating")
        return context | c_def

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = AmountOfWallets(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount_of_wallets']
            return generate_wallets(request, owner=request.user, amount=amount)

        return render(request, self.template_name, {'form': form})


class WalletsTransfer(DataMixin, TemplateView):
    template_name = 'wallets/wallets_transfer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Wallets.objects.all()
        context['object_list'] = object_list
        context['selection_form'] = WalletsSelectionForm()

        c_def = self.get_user_context(title="Добавление кошельков")
        return context | c_def

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        # Обрабатываем данные формы
        selection_form = WalletsSelectionForm(request.POST)

        if selection_form.is_valid():
            sender = selection_form.cleaned_data['selected_objects_1']
            receiver = selection_form.cleaned_data['selected_objects_2']
            amount = selection_form.cleaned_data['sol_amount']

        if len(sender) == 0 or len(receiver) == 0:
            print("and here")
            messages.warning(
                self.request,
                "Не выбраны кошельки"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_transfer'))
        elif len(sender) > 1 and len(receiver) > 1:
            messages.warning(
                self.request,
                "Выбрано больше 1 кошелька из каждого списка"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_transfer'))
        elif list(set(sender) & set(receiver)):
            messages.warning(
                self.request,
                "Один и тот же кошелек не может быть отправителем и получателем"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_transfer'))

        cache.set('sender', sender)
        cache.set('receiver', receiver)
        cache.set('amount', amount)
        return HttpResponseRedirect(reverse('wallets_transfer_confirm'))


class WalletsTransferConfirm(DataMixin, TemplateView):
    template_name = 'wallets/wallets_transfer_confirm.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Подтверждение перевода")

        sender = cache.get('sender')
        receiver = cache.get('receiver')
        amount = cache.get('amount')

        context['sender'] = sender
        context['receiver'] = receiver
        context['amount'] = amount

        return context | c_def


class WalletsTransferAccept(DataMixin, TemplateView):
    template_name = 'wallets/wallets_transfer_confirm.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Подтверждение перевода")

        sender = cache.get('sender')
        receiver = cache.get('receiver')
        amount = cache.get('amount')

        context['sender'] = sender
        context['receiver'] = receiver
        context['amount'] = amount

        return context | c_def

    def get(self, request):
        return sol_transfer(self.request, cache.get('sender'), cache.get('receiver'), cache.get('amount'))


class WalletsDelete(DeleteView, LoginRequiredMixin, DataMixin):
    model = Wallets
    template_name = 'wallets/wallets_delete.html'
    context_object_name = "wallet"
    success_url = reverse_lazy('wallets_list')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Удаление кошелька")
        return context | c_def

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(
                self.request,
                "Кошелек успешно удален"
            )
            return response
        except RestrictedError:
            messages.warning(
                self.request,
                "Невозможно удалить кошелек, так как он используется"
            )
            return HttpResponseRedirect(reverse_lazy('wallets_list'))


@require_POST
def get_wallet_balance(request):
    wallet_id = request.POST.get('wallet_id')
    wallet = Wallets.objects.get(id=wallet_id)
    wallet_balance = wallet.get_wallet_balance()
    return JsonResponse({'wallet_balance': wallet_balance})


def download_txt(request):
    # Получите данные из модели
    data = Wallets.objects.filter(owner_id=request.user.id)

    # Создайте текстовый файл
    content = "\n".join([str(item.key) for item in data])

    # Отправьте файл как ответ
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="data.txt"'
    return response