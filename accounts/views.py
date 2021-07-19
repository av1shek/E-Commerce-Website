from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from .forms import SignupForm
from .models import Customer, User
from shop.models import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django import forms

@login_required
def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('shop:shop')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        # print(user.password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.GET.get('next', "shop:shop"))
            else:
                messages.error(request, "Username not Active")
                return redirect('accounts:login')
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, 'shop/index.html', {'user_login':True})
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect("shop:shop")

def regUser(form):
    '''
    It will save Django user and student/teacher/assistant depending upon their choice.
    If user with given email id or username exists and their email is not
    verified then it deletes them.
    It recieves form.cleaned_data as argument
    '''
    user = None
    customer = None
    cart = None
    try:
        user = User.objects.get(username=form['username'])
        customer = Customer.objects.get(user = user)
        cart = Cart.objects.get(customer=customer)
    except ObjectDoesNotExist as e:
        pass
    except Exception as e:
        raise e
    if user and (not user.is_active):
        print("debug =>", user)
        user.delete()
        customer.delete()
        cart.delete()
        user = None
        customer = None
        cart = None
    # elif user and user.is_active:  # this case is handled in forms.py
    #     raise forms.ValidationError("This Username Already Exists")

    try:
        user = User.objects.get(email=form['email'])
        customer = Customer.objects.get(user = user)
        cart = Cart.objects.get(customer=customer)
    except ObjectDoesNotExist as e:
        pass
    except Exception as e:
        raise e
    if user and (not user.is_active):
        user.delete()
        customer.delete()
        cart.delete()
        user = None
        customer = None
        cart = None
    # elif user and user.is_active:  # this case is handled in forms.py
    #     raise forms.ValidationError("This Email Already Exists")

    # Note that we have deleted the inactive user with these username and email
    user = User.objects.create_user(username=form['username'],
                                     email=form['email'], 
                                     password=form['password1'],
                                     is_active=False,
                                    )
    # notice is_active = False, becuase we will activate account if user will
    # verify the email
    user.save()
    customer = Customer(user=user, 
                        fname=form['fname'], 
                        lname=form['lname'], 
                        mobno=form['mobno'], 
                        address=form['address'],
                        city=form['city'],
                        zip_code=form['city'],
                        state=form['state'])
    customer.save()
    cart = Cart(customer=customer, items_json='{}')
    cart.save()
    return user

def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = regUser(form.cleaned_data)
            current_site = get_current_site(request)
            message = render_to_string('accounts/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'accounts/signup.html', {'email_sent': True})
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            return redirect("accounts:signup")

    return render(request, 'accounts/signup.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # comment this line if you don not want to log in user after account activation
        return render(request, 'accounts/signup.html', {'email_verified': True})
    else:
        return render(request, 'accounts/signup.html', {'invalid_link': True})

