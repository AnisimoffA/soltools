from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from webtools.utils import DataMixin, CustomUserPermisionsMixin
from users.forms import CustomUserCreationForm
from users.models import CustomUsers


# Create your views here.
class UserRegister(DataMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "register_form.html"
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return context | c_def

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно зарегистрированы")
        form.save()
        return redirect('login')


class UserUpdate(CustomUserPermisionsMixin, DataMixin, UpdateView):
    model = CustomUsers
    template_name = 'users/users_update.html'

    form_class = CustomUserCreationForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обновление пользователя")
        return context | c_def

    def get_success_url(self):
        messages.success(
            self.request,
            "User was updated successfully"
        )
        return reverse_lazy('users_list')


class UserDelete(DataMixin, DeleteView, LoginRequiredMixin): # CheckUsersTasksMixin потом надо впихнуть
    model = CustomUsers
    template_name = 'users/users_delete.html'
    success_url = reverse_lazy('main_page')
    context_object_name = "user"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Удаление пользователя")
        return context | c_def

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, "Пользователь успешно удален")
        return response

