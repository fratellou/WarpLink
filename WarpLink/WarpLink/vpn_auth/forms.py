from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import User


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'autofocus': True}),
        error_messages={
            'required': 'Пожалуйста, введите корректное имя пользователя'}
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Пожалуйста, введите корректный пароль'}
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        errors = []
        if not username:
            errors.append(forms.ValidationError(
                'Пожалуйста, введите имя пользователя.'))
        if not password:
            errors.append(forms.ValidationError('Пожалуйста, введите пароль.'))
        if errors:
            raise ValidationError(errors)
        return super().clean()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                       'class': 'portal-input',
                                       'placeholder': 'Ваш email'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'portal-input',
                'placeholder': 'Придумайте логин'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'portal-input',
                'placeholder': 'Пароль'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'portal-input',
                'placeholder': 'Повторите пароль'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убедимся, что все поля имеют правильные атрибуты
        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update({
                'class': 'portal-input'
            })

        # Кастомизация сообщений об ошибках
        self.fields['username'].error_messages = {
            'required': 'Пожалуйста, введите имя пользователя'
        }
        self.fields['password1'].error_messages = {
            'required': 'Пожалуйста, введите пароль'
        }
        self.fields['password2'].error_messages = {
            'required': 'Пожалуйста, подтвердите пароль'
        }
        self.fields['email'].error_messages = {
            'required': 'Пожалуйста, введите email'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email
