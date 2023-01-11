from django import forms
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Fill your email here', 'class': 'form-control'}),
        label='Email Address'
    )

    password = forms.CharField(max_length=30, widget=forms.PasswordInput(
        attrs={'placeholder': 'Fill your password here', 'class': 'form-control'}),
        label='Password'
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={'placeholder': 'Podaj hasło', 'class': 'form-control'}),
        label='Podaj hasło'
    )

    confirm_password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło', 'class': 'form-control'}),
        label='Powtórz hasło'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Podaj imię', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Podaj nazwisko', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'placeholder': 'Podaj nazwę użytkownika', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Podaj email', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Podaj numer telefonu', 'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'username': 'Nazwa użytkownika',
            'email': 'Email',
            'phone_number': 'Numer telefonu',
        }

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password does not match!')
