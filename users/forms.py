from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUsers


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUsers
        fields = [
            'username',
            'password1',
            'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        unique_username = CustomUsers.objects.exclude(
            username=username
        ).filter(username=username).exists()
        if unique_username:
            raise forms.ValidationError(
                'Пользователь с таким именем уже существует.'
            )
        else:
            return username