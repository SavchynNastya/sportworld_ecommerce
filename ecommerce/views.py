from decimal import Decimal
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponse
from .forms import ContactForm, ReviewForm, UserRegistrationForm, CustomAuthenticationForm, PasswordResetForm, SetPasswordResetForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
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
import re
from .models import Category, Order, OrderItem, Profile, Review, Subcategory, Item, Cart, CartItem, Producer


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
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
        messages.error(self.request, 'Неправильний email чи пароль.')
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


def landing_page(request):
    bestsellers = Item.objects.filter(id__lte=12)
    return render(request, 'index.html', {'bestsellers': bestsellers})


def main_page(request):
    producers = Producer.objects.all()
    categories = Category.objects.all()
    subcategories = ''
   
    items = Item.objects.all()

    search_query = request.GET.get('search', '')

    if search_query:
        items = items.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    

    active_category = request.GET.get('category', '')

    if active_category != '':
        subcategories = Subcategory.objects.filter(category=active_category)
        items = Item.objects.filter(subcategory__in=subcategories)
        subcategories = list(Subcategory.objects.filter(category=categories.filter(id=active_category).first().id))
        print(subcategories)


    active_subcategory = request.GET.get('subcategory', '')

    if active_subcategory != '':
        active_subcategory = int(active_subcategory)
        subcategory = Subcategory.objects.get(id=active_subcategory)
        items = Item.objects.filter(subcategory=subcategory)

    if request.method == 'POST':
        min_price = request.POST.get('price__min')
        max_price = request.POST.get('price__max')

        if min_price.isdigit() and max_price.isdigit():
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


    username = request.COOKIES.get('username', '')

    context = {
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

    reviews = Review.objects.filter(item=item)
    print(reviews)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        liked_items = profile.liked_items.all()
        return render(request, 'item_page.html', {'item': item, 'reviews': reviews, 'liked_items': liked_items})

    return render(request, 'item_page.html', {'item': item, 'reviews': reviews})


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


        for item in cart_items:
            request.session['cart'].append(item)

        return redirect('cart')


def delete_from_cart_session(request, item_id):
    request.session['cart'] = list(request.session['cart'])
    request.session['cart'] = [x for x in request.session['cart'] if x['id'] != item_id]

    return redirect('cart')


def increment_cart_item(request, item_id):
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


@login_required
def delete_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, item=item)
    cart_item.delete()
    print(cart)
    cart.save()

    return redirect('cart')
 

def cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        profile, created = Profile.objects.get_or_create(user=request.user)
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

        contact_form = ContactForm()
        return render(request, 'cart.html', {'cart_items': cart_items, 'contact_form': contact_form})

    return render(request, 'cart.html', {'cart_items': list(cart_items), 'liked_items': liked_items})


def liked_items(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
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


def profile(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
        if request.method == "POST":
            request_body = request.body.decode('utf-8')
            data = json.loads(request_body)

            updated_request = request.POST.copy()
            updated_request.update({     
                'user': request.user, 
                'item': Item.objects.get(id=data.get("item_id")),
                'rating': data.get("rating"),
                'message': data.get("message"),
            })
            rating_form = ReviewForm(updated_request)
            print(rating_form.is_valid())
            print(rating_form.errors)
            if rating_form.is_valid():
                rating_form.save()
                messages.success(request, f'Your review has been accepted.')
                return HttpResponseRedirect(reverse('profile'))

            context = {'user': request.user, 'orders': orders, 'rating_form': rating_form, 'profile': profile}
        else:
            rating_form = ReviewForm()
            contact_form = ContactForm()
            context = {'user': request.user, 'orders': orders, 'rating_form': rating_form, 'profile': profile, 'contact_form': contact_form}
    else:
        return HttpResponseBadRequest('You can not access this page')
        
    return render(request, 'profile.html', context)


def add_contact_number_to_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            request_body = request.body.decode('utf-8')
            data = json.loads(request_body)
            country_code = data.get('country_code')
            number = data.get('contact_number')
            print(country_code)
            print(number)
            contact_number = country_code + number
            profile = Profile.objects.get(user=request.user)

            profile.contact_number = contact_number
            profile.save()

        return HttpResponseRedirect(reverse('profile'))

    else:
        return HttpResponseBadRequest('You can not access this page')


def form_order(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = Decimal('0.00')

        order = Order.objects.create(user=request.user, total_price=0)
        order_items = []

        for cart_item in cart_items:
            total += cart_item.item.price * cart_item.quantity
            item = Item.objects.get(id=cart_item.id)
            order_item = OrderItem.objects.create(item=item, order=order, quantity=cart_item.quantity)
            order_items.append(order_item)
            print(order_item)

        print(total)
        print(order_items)
        order.total_price = total
        order.save()
        order_item_ids = [order_item.item.id for order_item in order_items]
        for id in order_item_ids:
            print('id ', id)
        order.items.add(*order_item_ids)
        order.save()

        return redirect('profile')
    
    else:
        if request.method == 'POST':
            request_body = request.body.decode('utf-8')
            data = json.loads(request_body)
            country_code = data.get('country_code')
            number = data.get('contact_number')
            contact_number = country_code + number

            session_key = request.session.session_key

            order = Order.objects.create(session_key=session_key, total_price=0, contact_number=contact_number)

            order_items = []
            total = Decimal('0.00')
            request.session['cart'] = list(request.session['cart'])
            for item in request.session['cart']:
                item_object = Item.objects.get(id=item['id'])
                total += item_object.price * int(item['quantity'])
                order_item = OrderItem.objects.create(item=item_object, order=order, quantity=int(item['quantity']))
                order_items.append(order_item)

            order.total_price = total
            order.save()
            order_item_ids = [order_item.item.id for order_item in order_items]

            order.items.add(*order_item_ids)
            order.save()

        return redirect('cart')




