from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib.auth.views import LoginView
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
# from .forms import SignUpForm, LoginForm
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, logout
from django.urls import reverse_lazy, reverse
import random
from .backends import EmailBackend

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        print(form.fields)
        print(form.is_valid())
        print(form.errors)
        remember_me = form.cleaned_data['remember_me']
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = EmailBackend().authenticate(request=self.request, email=email, password=password)
        if user is not None:
            auth_login(self.request, user, backend='ecommerce.backends.EmailBackend')
            user.backend = EmailBackend.__module__ + "." + EmailBackend.__qualname__
            if not remember_me:
                self.request.session.set_expiry(0)
            return JsonResponse({'success': True, 'redirect_url': reverse('main_page')})

        return self.form_invalid(form)
    
    def form_invalid(self, form):
        print(form.fields)
        print(form.is_valid())
        print(form.errors)
        print(form.data)
        print("HELLO/")
        messages.error(self.request, 'Неправильний email чи пароль.')
        print(self.get_context_data(form=form))
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
class CustomRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('main_page')
    success_message = 'Реєстрація успішна. Ви зареєструвалися як %(username)s.'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        form.instance.username = form.instance.email
        password = form.cleaned_data.get('password1')
        username = form.cleaned_data.get('username')
        user = form.save()
        auth_login(self.request, user, backend='ecommerce.backends.EmailBackend')
        user.backend = EmailBackend.__module__ + "." + EmailBackend.__qualname__
        return JsonResponse({'success': True, 'redirect_url': reverse('main_page')})

    def form_invalid(self, form):
        messages.error(self.request, 'Помилка при реєстрації. Будь ласка, перевірте введені дані.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


# def registration_form(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.instance.username = form.instance.email
#             user = form.save()
#             auth_login(request, user, backend='ecommerce.backends.EmailBackend')
#             return JsonResponse({'success': True, 'redirect_url': reverse('main_page')})
#         else:
#             print("FORM IS INVALID")
#             errors = form.errors.as_json()
#             print(errors)
#             return JsonResponse({'success': False, 'errors': errors, 'form': str(form)})
#     else:
#         form = UserRegistrationForm()
#     return render(request, "register.html", {"form": form})




# def registration_form(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         print(form.errors.as_data())
#         print(form.is_valid)
#         if form.is_valid():
#             form.instance.username = form.instance.email
#             user = form.save()
#             print(user)
#             auth_login(request, user, backend='ecommerce.backends.EmailBackend')
#             return redirect('main_page')
#     else:
#         form = UserRegistrationForm()

#     # context = {'form': form}
#     # if form.errors:
#     #     context['errors'] = form.errors.as_data()

#     return render(request, "register.html", {"form": form})




# def login_view(request):
#     if request.method == 'POST':
#         print(request.POST)
#         form = CustomAuthenticationForm(request.POST)
#         print(form.errors.as_data())
#         print(form.is_valid)
#         print(form.declared_fields)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user, backend='ecommerce.backends.EmailBackend')
#             return redirect('main_page')
#     else:
#         form = CustomAuthenticationForm()

#     # context = {'form': form}
#     # if form.errors:
#     #     context['errors'] = form.errors.as_data()

#     return render(request, 'login.html', {'form': form})

# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         return redirect('main_page')

# def login(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('main_page')
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# def login_or_register(request):
#     if request.method == 'POST':
#         if 'login' in request.POST:
#             form = CustomAuthenticationForm(request.POST)
#             if form.is_valid():
#                 username = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password')
#                 user = authenticate(request, username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     return redirect('home')
#                 else:
#                     messages.error(request, 'Invalid username or password.')
#                     return redirect('login_or_register')
#         elif 'register' in request.POST:
#             form = UserRegistrationForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 username = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password1')
#                 user = authenticate(request, username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     return redirect('home')
#                 else:
#                     messages.error(request, 'An error occurred while trying to register.')
#                     return redirect('login_or_register')
#     else:
#         form = CustomAuthenticationForm()

#     return render(request, 'login_or_register.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('main_page')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration.html', {'form': form})

# def login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('main_page')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})


def landing_page(request):
    return render(request, 'index.html')


def main_page(request):
    return render(request, 'main.html')


def product_page(request):
    return render(request, 'item_page.html')

def cart(request):
    return render(request, 'cart.html')

def liked_items(request):
    return render(request, 'liked.html')