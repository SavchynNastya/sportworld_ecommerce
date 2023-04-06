from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponse
from .forms import UserRegistrationForm, CustomAuthenticationForm, PasswordResetForm, SetPasswordResetForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.sessions.models import Session
from django.contrib.auth import login as auth_login, logout
from django.urls import reverse_lazy, reverse
from django.contrib.sites.shortcuts import get_current_site
from .backends import EmailBackend
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token.token import account_activation_token, password_reset_token
from django.core.mail import send_mail, EmailMessage
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
# import json
import re
from urllib import parse
from .models import Category, Profile, Subcategory, Item, Cart, CartItem, Producer


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        # print(form.fields)
        # print(form.is_valid())
        # print(form.errors)
        remember_me = form.cleaned_data['remember_me']
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = EmailBackend().authenticate(request=self.request, email=email, password=password)
        if user is not None:
            auth_login(self.request, user, backend='ecommerce.backends.EmailBackend')
            user.backend = EmailBackend.__module__ + "." + EmailBackend.__qualname__
            if not remember_me:
                self.request.session.set_expiry(0)
            response = JsonResponse({'success': True, 'redirect_url': reverse('main_page')})
            response.set_cookie('username', user.username)
            return response

        return self.form_invalid(form)
    
    def form_invalid(self, form):
        # print(form.fields)
        # print(form.is_valid())
        # print(form.errors)
        # print(form.data)
        messages.error(self.request, 'Неправильний email чи пароль.')
        # print(self.get_context_data(form=form))
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

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # auth_login(self.request, user, backend='ecommerce.backends.EmailBackend')
        # user.backend = EmailBackend.__module__ + "." + EmailBackend.__qualname__
        # return JsonResponse({'success': True, 'redirect_url': reverse('main_page')})
        current_site = get_current_site(self.request)  
        mail_subject = 'Посилання для активації акаунта SPORTWORLD'

        message = render_to_string('acc_active_email.html', {  
            'user': user,  
            'domain': current_site.domain,  
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })  

        to_email = form.cleaned_data.get('email')  
        email_letter = EmailMessage(  
            mail_subject, message, to=[to_email]  
        )  
        print(email_letter)
        email_letter.send()  
        return JsonResponse({'success': True, 'message': 'Будь ласка, підтвердіть вашу електронну адресу, щоб завершити реєстрацію.'})
        # return HttpResponse('Будь ласка, підтвердіть вашу електронну адресу, щоб завершити реєстрацію.')

    def form_invalid(self, form):
        messages.error(self.request, 'Помилка при реєстрації. Будь ласка, перевірте введені дані.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
def activate(request, uidb64, token):  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        return redirect('main_page')
    else:  
        return HttpResponse('Посилання неактивне')


def reset_password(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    user.is_active = False
                    user.save()

                    subject = "SPORTWORLD Скидання паролю"
                    email_template_name = "password_reset_email.html"
                    current_site = get_current_site(request) 
                    email_message = {
                        'user': user,  
                        'domain': current_site.domain,  
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': password_reset_token.make_token(user),
                    }
                    email = EmailMessage(  
                        subject, render_to_string(email_template_name, email_message), to=[user.email]
                    )  
                    email.send()  
                    user.is_active = False
                    return JsonResponse({'success': True, 'redirect_url': reverse('main_page')})
    password_reset_form = PasswordResetForm()
    return render(request, "password_reset.html", context={"password_reset_form": password_reset_form})



def reset_password_confirm(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            form = SetPasswordResetForm(user=user, data=request.POST)
            print(form.is_valid())
            if form.is_valid():

                form.save()
                update_session_auth_hash(request, form.user)
                user.is_active = True
                user.save()

                messages.add_message(request, messages.SUCCESS, 'Password reset successfully.')
                return redirect("password_reset_complete")
            else:
                context = {
                    'form': form,
                    'uid': uidb64,
                    'token': token
                }
                messages.add_message(request, messages.WARNING, 'Пароль не може бути змінений')
                return render(request, 'password_reset_form.html', context)
        else:
            messages.add_message(request, messages.WARNING, 'Посилання для скидання паролю не активне.')
            messages.add_message(request, messages.WARNING, 'Будь ласка, спробуйте отримати його ще раз')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        context = {
            'form': SetPasswordResetForm(user),
            'uid': uidb64,
            'token': token
        }
        return render(request, 'password_reset_form.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'Посилання для скидання паролю не активне.')
        messages.add_message(request, messages.WARNING, 'Будь ласка, спробуйте отримати його ще раз.')

    return redirect("landing_page")
            

def reset_password_complete(request):
    return render(request, 'password_reset_complete.html')


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

    producers = Producer.objects.all()
    categories = Category.objects.all()
    subcategories = ''
   
    items = Item.objects.all()

    search_query = request.GET.get('search', '')

    if search_query:
        items = items.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    

    active_category = request.GET.get('category', '')
    print(active_category)
    if active_category != '':
        subcategories = Subcategory.objects.filter(category=active_category)
        items = Item.objects.filter(subcategory__in=subcategories)
        subcategories = list(Subcategory.objects.filter(category=categories.filter(id=active_category).first().id))
        print(subcategories)


    active_subcategory = request.GET.get('subcategory', '')
    print(active_subcategory)
    if active_subcategory != '':
        active_subcategory = int(active_subcategory)
        subcategory = Subcategory.objects.get(id=active_subcategory)
        items = Item.objects.filter(subcategory=subcategory)

    # min_price = request.GET.get('price__min')
    # max_price = request.GET.get('price__max')
    # if min_price and max_price:
    #     items = items.filter(price__gte=min_price, price__lte=max_price)
    #     print(items)
    #     data = {'items': list(items.values())}
    #     return JsonResponse(data)
    if request.method == 'POST':
        min_price = request.POST.get('price__min')
        max_price = request.POST.get('price__max')

        if min_price and max_price:
            items = items.filter(price__gte=min_price, price__lte=max_price)
            if active_category != '':
                subcategories = Subcategory.objects.filter(category=active_category)
                items =items.filter(subcategory__in=subcategories)
                if active_subcategory != '':
                    active_subcategory = int(active_subcategory)
                    subcategory = Subcategory.objects.get(id=active_subcategory)
                    items = items.filter(subcategory=subcategory)


    choosen_producers = request.GET.getlist('producer')
    if choosen_producers:
        choosen_producers_objects = Producer.objects.filter(name__in=choosen_producers)
        items = items.filter(producer__in=choosen_producers_objects)
        print(active_category)
        print(active_subcategory)
        if active_category != '':
            subcategories = Subcategory.objects.filter(category=active_category)
            items =items.filter(subcategory__in=subcategories)
            if active_subcategory != '':
                active_subcategory = int(active_subcategory)
                subcategory = Subcategory.objects.get(id=active_subcategory)
                items = items.filter(subcategory=subcategory)

        data = {'items': list(items.values())}
        return JsonResponse(data)
    
    if not choosen_producers and not re.search(r'^text/html', request.META.get('HTTP_ACCEPT')):
        if active_category != '':
            subcategories = Subcategory.objects.filter(category=active_category)
            items = Item.objects.filter(subcategory__in=subcategories)
            if active_subcategory != '':
                subcategory = Subcategory.objects.get(id=active_subcategory)
                items = items.filter(subcategory=subcategory)
        data = {'items': list(items.values())}
        return JsonResponse(data)

    print(items)

    username = request.COOKIES.get('username', '')

    context = {
        # 'categories': categories,
        'items': items,
        'subcategories': subcategories,
        'active_category': active_category,
        'active_subcategory': active_subcategory,
        'username': username,
        'producers' : producers,
        'choosen_producers': choosen_producers,
    }

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        liked_items = profile.liked_items.all()
        context['liked_items'] = liked_items

    return render(request, 'main.html', context)


def product_page(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        liked_items = profile.liked_items.all()
        return render(request, 'item_page.html', {'item': item, 'liked_items': liked_items})

    return render(request, 'item_page.html', {'item': item})


def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')
    else:
        if not request.session.get('cart'):
            request.session['cart'] = list()
        else:
            request.session['cart'] = list(request.session['cart'])
        cart_items = []
        item_exist = next((item for item in request.session['cart'] if item['id'] == item_id), False)
        if not item_exist:
            cart_items.append({
                'id': item.id,
                'quantity': 1
            })

        # for item in request.session['cart']:
        #     # item_exist = next((item for item in request.session['cart'] if item['id'] == item_id), False)
        #     # print(item_exist)
        #     # if item_exist:
        #     #     continue
        #     item = get_object_or_404(Item, id=item_id)
        #     cart_items.append(CartItem(item=item, quantity=quantity))
        
        for item in cart_items:
            request.session['cart'].append(item)

        return redirect('cart')

        # print(cart_items)
        # print(request.session['cart'])


def delete_from_cart_session(request, item_id):
    request.session['cart'] = list(request.session['cart'])
    request.session['cart'] = [x for x in request.session['cart'] if x['id'] != item_id]

    return redirect('cart')

def increment_cart_item(request, item_id):
    # item = get_object_or_404(Item, id=item_id)
    if request.user.is_authenticated:
        item = get_object_or_404(Item, id=item_id)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, item=item)
        
        cart_item.quantity += 1
        cart_item.save()

        return redirect('cart')
    else:
        cart_items = list(request.session['cart'])

        for item in cart_items:
            if item['id'] == item_id:
                item['quantity'] += 1

        request.session['cart'] = cart_items

        return redirect('cart')

def decrement_cart_item(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, id=item_id)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, item=item)
        
        cart_item.quantity -= 1
        cart_item.save()

        return redirect('cart')
    else:
        cart_items = list(request.session['cart'])

        for item in cart_items:
            if item['id'] == item_id:
                item['quantity'] -= 1

        request.session['cart'] = cart_items

        return redirect('cart')


# def create_order_session(request):
#     if not request.session.get('cart'):
#         request.session['cart'] = list()
#     else:
#         request.session['cart'] = list(request.session['cart'])

#     session_key = request.session.session_key
#     email = request.POST.get('email')
#     phone = request.POST.get('phone')
#     address = request.POST.get('address')
#     order = Order.objects.create(session_key=session_key, email=email, phone=phone, address=address, total_price=0)

#     for item_id, quantity in cart.items():
#         item = Item.objects.get(id=item_id)
#         price = item.price
#         order_item = OrderItem.objects.create(item=item, order=order, quantity=quantity, price=price)

#     order.total_price = order.get_total()
#     order.save()

#     # Clear the cart
#     request.session['cart'] = {}

#     return render(request, 'orders/order_created.html', {'order': order})


@login_required
def delete_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, item=item)
    cart_item.delete()
    print(cart)
    cart.save()

    return redirect('cart')


# @login_required
# def add_to_liked(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if profile.liked_items.filter(id=item_id).exists():
#         profile.liked_items.remove(item)
#     else:
#         profile.liked_items.add(item)
#     profile.save()
#     # return redirect('liked_items')
#     previous_url = request.META.get('HTTP_REFERER')
#     if previous_url is not None:
#         return HttpResponseRedirect(previous_url)
#     else:
#         return HttpResponseRedirect(reverse('liked_items'))
    

def cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        profile = Profile.objects.get(user=request.user)
        liked_items = profile.liked_items.all()
    else:
        cart_items = []
        if not request.session.get('cart'):
            request.session['cart'] = list()
        else:
            request.session['cart'] = list(request.session['cart'])
            print(request.session['cart'])
            for item in request.session['cart']:
                item_object = Item.objects.get(id=item['id'])
                print(item)
                cart_items.append({'item': item_object, 'quantity': int(item['quantity'])})
        return render(request, 'cart.html', {'cart_items': cart_items})

    return render(request, 'cart.html', {'cart_items': list(cart_items), 'liked_items': liked_items})


def liked_items(request):
    profile = Profile.objects.get(user=request.user)
    liked_items = profile.liked_items.all()
    return render(request, 'liked.html', {'liked_items': liked_items})


def add_to_liked(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    profile, created = Profile.objects.get_or_create(user=request.user)

    liked = False

    if profile.liked_items.filter(id=item_id).exists():
        profile.liked_items.remove(item)
    else:
        profile.liked_items.add(item)
        liked = True
    profile.save()
    print(profile.liked_items.all())

    return JsonResponse({'liked': liked})