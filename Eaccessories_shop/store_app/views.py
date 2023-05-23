from django.shortcuts import render, redirect
from store_app.models import Product, Categories, Filter_Price, Color, Brand, Tag, Order, OrderItem,Wishlist
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest



from django.views.decorators.csrf import csrf_exempt

import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required(login_url="user_app/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("")


@login_required(login_url="user_app/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="user_app/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="user_app/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="user_app/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="user_app/login/")
def cart_detail(request):
    return render(request, 'store_app/cart_details.html')






# Create your views here.

def BASE(request):

    return render(request, 'store_app/base.html')


def INDEX(request):
    product = Product.objects.filter(status='Publish')

    context = {
        'product': product
    }

    return render(request, 'store_app/index.html', context)


def PRODUCT(request):

    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLORID = request.GET.get('color')
    BRANDID = request.GET.get('brand')

    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')
    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')

    if CATID:
        product = Product.objects.filter(categories=CATID, status='Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(
            filter_price=PRICE_FILTER_ID, status='Publish')

    elif COLORID:
        product = Product.objects.filter(color=COLORID, status='Publish')

    elif BRANDID:
        product = Product.objects.filter(brand=BRANDID, status='Publish')

    elif ATOZID:
        product = Product.objects.filter(status='Publish').order_by('name')

    elif ZTOAID:
        product = Product.objects.filter(status='Publish').order_by('-name')

    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status='Publish').order_by('price')

    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status='Publish').order_by('-price')

    elif NEW_PRODUCTID:
        product = Product.objects.filter(
            status='Publish', condition='New').order_by('-id')

    elif OLD_PRODUCTID:
        product = Product.objects.filter(
            status='Publish', condition='old').order_by('-id')

    else:
        product = Product.objects.filter(status='Publish')

    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
        'color': color,
        'brand': brand

    }
    return render(request, 'store_app/product.html', context)


def SEARCH(request):
    query = request.GET.get('query')
    if query:
        product = Product.objects.filter(name__icontains=query)

    else:
        product = Product.objects.all()

    context = {
        'product': product
    }

    return render(request, 'store_app/index.html', context)


def PRODUCT_DETAIL_PAGE(request,id):
    prod = Product.objects.filter(id = id).first()

    context = {
        'prod': prod
    }
    return render(request, 'store_app/product_single.html', context)


def Check_out(request):
    amount = int(float(request.POST.get("amount"))*100)
    
    payment = client.order.create({
        "amount": amount,
        
        "currency": "INR",
        "payment_capture": "1"
    })

    order_id = payment['id']
    context = {
        'order_id': order_id,
        'payment': payment,
    }
    
    return render(request, 'store_app/checkout.html', context)


def PLACE_ORDER(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        amount = request.POST.get('amount')
        

        

        context = {
            'order_id' : order_id,
        }
        order = Order(
            user=user,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            payment_id=order_id,
            amount=amount
        )
    
        order.save()


        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a * b
            item = OrderItem(
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total
                
            )
            item.save()

        return render(request, 'store_app/placeorder.html',context)


@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                
                break
        user = Order.objects.filter(payment_id = order_id).first()
        
        user.paid = True
        user.save()

        

    return render(request, 'store_app/thankyou.html')


def WISHLIST(request):

    return render(request, 'store_app/wishlist.html')


def Aboutus(request):

    return render(request, 'store_app/aboutus.html')

