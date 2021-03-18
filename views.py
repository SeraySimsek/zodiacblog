from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
import self as self
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as dj_login
from .forms import *
from .models import *
from .properties import *
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')


def homepage(request):
    if request.user.is_anonymous:
        return render(request, 'blog/homepage.html', {})

    customer = Customer.objects.get(user=request.user)
    requested_user_type = user_type.objects.get(customer=customer)
    is_there_any_fortune_telling_entry = FortuneTelling.objects.filter(is_ok='N').count()
    fortune_telling_counter = 0

    if int(is_there_any_fortune_telling_entry) != 0:
        fortune_telling_counter = int(is_there_any_fortune_telling_entry)

    return render(request, 'blog/homepage.html', {"context" : requested_user_type.user_type, "fortune_telling_counter" : fortune_telling_counter})


def astrolojitarihi(request):
    return render(request, 'blog/astrolojitarihi.html')

def tarot(request):
    return render(request, 'blog/tarot.html')

def yukselenhesapla(request):
    return render(request, 'blog/yukselenhesaplama.html')

def burchesaplama(request):
    return render(request, 'blog/burchesaplama.html')

def burcuyumu(request):
    return render(request, 'blog/burcuyumu.html')

def testler(request):
    return render(request, 'blog/testler.html')

def burclar(request):
    return render(request, 'blog/burclar.html')

def koc(request):
    return render(request, 'blog/koc.html')

def boga(request):
    return render(request, 'blog/boga.html')

def akrep(request):
    return render(request, 'blog/akrep.html')

def aslan(request):
    return render(request, 'blog/aslan.html')

def balık(request):
    return render(request, 'blog/balık.html')

def başak(request):
    return render(request, 'blog/başak.html')

def ikizler(request):
    return render(request, 'blog/ikizler.html')

def kova(request):
    return render(request, 'blog/kova.html')

def oglak(request):
    return render(request, 'blog/oglak.html')

def terazi(request):
    return render(request, 'blog/terazi.html')

def yay(request):
    return render(request, 'blog/yay.html')

def yengeç(request):
    return render(request, 'blog/yengeç.html')

def login(request):
    context = {}
    return render(request, 'blog/login.html', context)

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            name = request.POST['name']
            lastname = request.POST['lastname']
            email = request.POST['email']
            job = request.POST['job']
            zodiac = request.POST['zodiac']
            gender = request.POST['gender']
            relationship = request.POST['relationship']

            customer = Customer(name=name, lastname=lastname, email=email, job=job, zodiac=zodiac, gender=gender,
                                relationship=relationship, user=user)
            customer.save()

            new_user_type = user_type(customer=customer, user_type='U')
            new_user_type.save()

            dj_login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def iletişim(request):
    user = request.user.customer
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            comment = request.POST['comment']

            contact = Contact(comment=comment, customer=user)
            contact.save()
            return redirect('homepage')
    else:
        form =ContactForm()
    return render(request, 'blog/iletişim.html' ,{'form': form, 'user':user})

@login_required()
def shopping(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'blog/shopping.html', context)


@login_required()
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer  # one to one relationship
        order, created = Order.objects.get_or_create(customer=customer, complete=False)  # finding or creating order
        items = order.orderitem_set.all()  # get all items
    else:
        items = []
        order = {'get_cart_total': 0,
                 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'blog/cart.html', context)


@login_required()
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer  # one to one relationship
        order, created = Order.objects.get_or_create(customer=customer, complete=False)  # finding or creating order
        items = order.orderitem_set.all()  # get all items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'blog/checkout.html', context)

@login_required()
def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)


    total = float(data['form']['total'])
    order.transaction_id = transaction_id



    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
     )



    return JsonResponse('Payment submitted..', safe=False)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('ProductId: ', productId)
    print('Action: ', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@login_required
def kahveFalı(request):
    return render(request, 'blog/kahveFalı.html')

@login_required
def hesapayarları(request):
    customer = request.user.customer
    form = Hesabım(instance=customer)

    if request.method == 'POST':
        form = Hesabım(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/homepage')
    context = {'form': form}

    return render(request, 'blog/hesapayarları.html', context)

def evethayır(request):
    return render(request, 'blog/evethayır.html')

def hakkımızda(request):
    return render(request, 'blog/hakkımızda.html')


def bilgitesti(request):
    return render(request, 'blog/bilgitesti.html')

def meslek(request):
    return render(request, 'blog/meslek.html')

@login_required()
def add_new_post_page(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    requested_user_type = user_type.objects.get(customer=customer)

    if requested_user_type.user_type == 'F' or requested_user_type.user_type == 'B':
        form = PostForm(request.POST)
        randomly_fortune_telling = FortuneTelling.objects.all().filter(is_ok='N').first()
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            zodiac_type = request.POST.get('zodiac_type')
            if requested_user_type.user_type == 'F':
                post_type = 'F'
                FortuneTelling.objects.filter(id=randomly_fortune_telling.id).update(is_ok='Y', to_user=customer,
                                                                                     date_review=datetime.datetime.now())
                new_post = post(title=title, content=content, customer=customer, post_type=post_type,
                                date_added=datetime.datetime.now(), zodiac_type=zodiac_type,
                                post_for=randomly_fortune_telling)

            elif requested_user_type.user_type == 'B':
                post_type = 'B'
                new_post = post(title=title, content=content, customer=customer, post_type=post_type,
                                date_added=datetime.datetime.now(), zodiac_type=zodiac_type)
            else:
                return redirect('/error')
            new_post.save()
            return redirect('/homepage')
        else:
            form = PostForm()

        if randomly_fortune_telling is not None:
            return render(request, 'blog/add_new_post.html',
                          {'form': form, 'content_type': requested_user_type.user_type,
                           'fortune_telling': randomly_fortune_telling})
        elif requested_user_type.user_type == 'B':
            return render(request, 'blog/add_new_post.html',
                          {'form': form, 'content_type': requested_user_type.user_type})
        else:
            return redirect('/homepage')
    return redirect('/error')


@login_required()
def view_zodiac(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    requested_post = post.objects.filter(post_type='B', zodiac_type=str(customer.zodiac)).order_by('date_added')
    return render(request, 'blog/burçpost.html', {'context': requested_post})


@login_required()
def view_fortune_telling(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    #eğer fortune telling yoksa requested user için->error page
    if not FortuneTelling.objects.filter(from_user=customer).exists():
        logging.error(str(FAL_BILGISI_BULUNAMADI).format(str(customer)))
        return redirect('/error')

    fortune_telling = FortuneTelling.objects.all().filter(from_user=customer)
    requested_post = []

    for current_fortune_telling in fortune_telling:
        current_post = get_object_or_404(post, post_for=current_fortune_telling)
        requested_post.append(current_post)

    return render(request, 'blog/falpost.html', {'context': requested_post})


@login_required()
def error_page(request):
    logging.warning(str(HATA_MESAJI))
    return HttpResponse(str(HATA_MESAJI))


# fal istegi gondermek icin:
@login_required()
def send_fortune_telling_request(request):
    form = FortuneTellingForm(request.POST)
    if request.method == 'POST':
        pic = request.POST.get('pic')
        user = request.user
        customer = Customer.objects.get(user=user)
        from_user = customer
        date_added = datetime.datetime.now()
        new_fortune_telling = FortuneTelling(from_user=from_user, pic=pic, date_added=date_added)
        new_fortune_telling.save()
        logging.info(str(YENI_GIRDI_EKLENDI).format(
            str(new_fortune_telling.from_user.name) + " " + str(new_fortune_telling.from_user.lastname)))
    else:
        form = FortuneTellingForm()
        logging.info(str(FORM_YENILEME))
    return render(request, 'blog/homepage.html', {'form': form})
