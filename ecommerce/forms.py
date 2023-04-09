from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Review


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101, label='Ім\'я')
    last_name = forms.CharField(max_length=101, label='Прізвище')
    email = forms.EmailField(required=True, label='Електронна пошта')
    password1 = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердження паролю', strip=False, widget=forms.PasswordInput)

    error_messages = {
        'password_mismatch': 'Паролі не співпадають.'
    }

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Ім`я',
            'last_name': 'Прізвище',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Повторно пароль',
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Електронна пошта занята.")
            raise forms.ValidationError("Електронна пошта занята.")

        return self.cleaned_data
    

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label='Електронна пошта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    error_messages = {
        'invalid_login': 'Введіть коректну адресу ел. пошти і пароль',
        'inactive': 'Цей аккаунт неактивний.',
        'invalid_password': 'Невірно введений пароль'
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields.pop('username', None)
        self.fields['remember_me'].widget.attrs.update({'class': 'form-check-input'})


    def clean(self):
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                self.add_error('email', 'Неправильна адреса ел. пошти')
                return cleaned_data

            if not user.check_password(password):
                self.add_error('password', 'Неправильний пароль')
                return cleaned_data

        return cleaned_data

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True, label='Електронна пошта')

    def clean(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            self.add_error('email', "За даною електронною поштою не знайдено користувача.")
            raise forms.ValidationError("За даною електронною поштою не знайдено користувача.")


class SetPasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Пароль',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-reset',
                'placeholder': 'Введіть пароль',
                'type': 'password',
                'id': 'user_password',
            }
        ))

    new_password2 = forms.CharField(
        label='Підтвердіть пароль',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-reset',
                'placeholder': 'Введіть пароль ще раз',
                'type': 'password',
                'id': 'user_password2',
            }
        ))
        
    error_messages = {
        'password_mismatch': 'Паролі не співпадають.'
    }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['item', 'user', 'rating', 'message']
    rating = forms.IntegerField(min_value=1, max_value=5, widget=forms.RadioSelect(attrs={'class': 'rating'}))
    message = forms.CharField(label="Опишіть якість товару", widget=forms.Textarea(attrs={'class': 'form__textarea'}), required=False)


class ContactForm(forms.Form):
    country_code = forms.ChoiceField(choices=[('38', '+38'), ('48', '+48')], label='Country code', widget=forms.Select(attrs={'class':'county-code-select'}))
    phone_number = forms.CharField(label='Номер телефону', widget=forms.TextInput(attrs={'type': 'tel'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise ValidationError('Номер телефону повинен містити лише цифри.')
        if len(phone_number) != 10:
            raise ValidationError('Номер телефону повинен мати 10 цифр.')
        return phone_number