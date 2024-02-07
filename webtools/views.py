from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from webtools.utils import DataMixin
from webtools.forms import LoginUserForm


class MainPage(DataMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sol Manager")
        return context | c_def


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login_form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return context | c_def

    def get_success_url(self):
        messages.success(self.request, 'Вы успешно вошли')
        return reverse_lazy('main_page')


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли')
    return redirect('main_page')