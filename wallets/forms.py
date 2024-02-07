from django import forms
from wallets.models import Wallets


class WalletsForm(forms.ModelForm):
    key = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'rows': 5}),
        help_text="Введите кошельки, каждый с новой строки."
    )

    class Meta:
        model = Wallets
        fields = ['key']


class AmountOfWallets(forms.Form):
    amount_of_wallets = forms.IntegerField(
        label='',
        help_text="Укажите, сколько кошельков вы хотите создать."
    )


class WalletsSelectionFormForBalanceChecking(forms.Form):
    selected_objects_1 = forms.ModelMultipleChoiceField(
        queryset=Wallets.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class WalletsSelectionForm(forms.Form):
    selected_objects_1 = forms.ModelMultipleChoiceField(
        queryset=Wallets.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    selected_objects_2 = forms.ModelMultipleChoiceField(
        queryset=Wallets.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    sol_amount = forms.IntegerField(
        label='Количество соланы',
        initial=0,
        help_text="Введите кошельки, каждый с новой строки."
    )

