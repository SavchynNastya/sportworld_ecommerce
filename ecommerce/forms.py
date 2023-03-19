from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .backends import EmailBackend


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
        fields = ['first_name', 'last_name', 'email', 'password1', 'password1']
        labels = {
            'first_name': 'Ім`я',
            'last_name': 'Прізвище',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Повторно пароль'
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Електронна пошта занята.")
            raise forms.ValidationError("Електронна пошта занята.")

        return self.cleaned_data
    

# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean_username(self):
#         email = self.cleaned_data.get('username')
#         if email:
#             self.cleaned_data['username'] = email.lower()
#         return email.lower()


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

    # def clean(self):
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     username = self.changed_data.get('email')

    #     if email is not None and password:
    #         UserModel = get_user_model()
    #         try:
    #             user = UserModel.objects.get(email=email)
    #         except UserModel.DoesNotExist:
    #             raise forms.ValidationError(
    #                 self.error_messages['invalid_login'],
    #                 code='invalid_login',
    #                 params={'email': self.username_field.verbose_name},
    #             )

    #         if not user.check_password(password):
    #             raise forms.ValidationError(
    #                 self.error_messages['invalid_login'],
    #                 code='invalid_login',
    #                 params={'email': self.username_field.verbose_name},
    #             )

    #         if not self.user_can_authenticate(user):
    #             raise forms.ValidationError(
    #                 self.error_messages['inactive'],
    #                 code='inactive',
    #             )

    #     return self.cleaned_data
    # def clean(self):
    #     user = User.objects.get(email=self.cleaned_data.get('email'))
    #     self.cleaned_data['username'] = user.email
    #     return super(CustomAuthenticationForm, self).clean()
    def clean(self):
        cleaned_data = super().clean()
        
        # email = cleaned_data.get('username')
        # password = cleaned_data.get('password')
        
        # if email and password:
        #     UserModel = get_user_model()
        #     try:
        #         user = UserModel.objects.get(email=email)
        #     except UserModel.DoesNotExist:
        #         self.add_error('username', 'Invalid email or password')
        #         return cleaned_data

        #     if not user.check_password(password):
        #         self.add_error('username', 'Invalid email or password')
        #         return cleaned_data

        #     if not self.user_can_authenticate(user):
        #         self.add_error('username', 'This account is inactive')
        #         return cleaned_data

        return cleaned_data

# class PasswordResetForm(PasswordResetForm):
#     email = forms.EmailField(required=True, label='Електронна пошта')


#     def clean(self):
#         email = self.cleaned_data.get('email')
#         if not User.objects.filter(email=email).exists():
#             self.add_error('email', "За даною електронною поштою не знайдено користувача.")
#             raise forms.ValidationError("За даною електронною поштою не знайдено користувача.")


# class SetPasswordResetForm(SetPasswordForm):
#     new_password1 = forms.CharField(
#         label='Пароль',
#         help_text=False,
#         max_length=100,
#         required=True,
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-reset',
#                 'placeholder': 'Введіть пароль',
#                 'type': 'password',
#                 'id': 'user_password',
#             }
#         ))

#     new_password2 = forms.CharField(
#         label='Підтвердіть пароль',
#         help_text=False,
#         max_length=100,
#         required=True,
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-reset',
#                 'placeholder': 'Введіть пароль ще раз',
#                 'type': 'password',
#                 'id': 'user_password',
#             }
#         ))
        
#     error_messages = {
#         'password_mismatch': 'Паролі не співпадають.'
#     }


# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=False, help_text='')
#     last_name = forms.CharField(max_length=30, required=False, help_text='')
#     email = forms.EmailField(max_length=254, help_text='Введіть електронну адресу')

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

# class LoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password',)