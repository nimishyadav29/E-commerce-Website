from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Customer, Cart,OrderPlaced
from .forms import CustomerRegistrationForm, LoginForm, MyPasswordChangeForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q


def home(request):
    topwear = Product.objects.filter(category='TW')
    bottomwear = Product.objects.filter(category='BW')

    return render(request, 'app/home.html', {'topwear': topwear, 'bottomwear': bottomwear})


def product_detail(request, id):
    item_already_in_cart=False
    item_already_in_cart = Cart.objects.filter(Q(product=id) & Q(user=request.user)).exists()
    details = Product.objects.filter(id=id)
    return render(request, 'app/productdetail.html', {'details': details ,'item_already_in_cart':item_already_in_cart})


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()

    return redirect("showcart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0

    totalamount = 0.0
    if cart:

        for i in cart:
            temp = i.product.discounted_price * i.quantity
            amount = amount + temp

        tal = amount + 70.0
        print(amount)
        return render(request, "app/addtocart.html", {'carts': cart, 'ta': amount, 'tas': tal})

    else:
        return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        ch = Product.objects.get(id=prod_id)
        c = Cart.objects.get(Q(product=ch) & Q(user=request.user))
        c.quantity += 1
        c.save()
    amount = 0.0

    user = request.user
    cart = Cart.objects.filter(user=user)
    for i in cart:
        temp = i.product.discounted_price * i.quantity
        amount = amount + temp
    tal = amount + 70.0
    print(amount)
    data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': tal
    }
    return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        ch = Product.objects.get(id=prod_id)
        c = Cart.objects.get(Q(product=ch) & Q(user=request.user))
        c.quantity -= 1
        c.save()
    amount = 0.0

    user = request.user
    cart = Cart.objects.filter(user=user)
    for i in cart:
        temp = i.product.discounted_price * i.quantity
        amount = amount + temp
    tal = amount + 70.0
    print(amount)
    data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': tal
    }
    return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        ch = Product.objects.get(id=prod_id)

        c = Cart.objects.get(Q(product=ch) & Q(user=request.user))
        c.delete()

    amount = 0.0

    user = request.user
    cart = Cart.objects.filter(user=user)
    for i in cart:
        temp = i.product.discounted_price * i.quantity
        amount = amount + temp
    tal = amount + 70.0
    print(amount)
    data = {
        'amount': amount,
        'totalamount': tal
    }
    return JsonResponse(data)


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    for i in cart_items:
        temp = i.product.discounted_price * i.quantity
        amount = amount + temp
    tal = amount + 70.0

    return render(request, 'app/checkout.html', {'add': add, 'cart_items': cart_items, 'totalcost': tal})


def buy_now(request):
    return render(request, 'app/buynow.html')


def profile(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully.')
            fm = CustomerProfileForm()

            return render(request, 'app/profile.html', {'form': fm, 'active': 'btn-primary'})
        else:
            fm = CustomerProfileForm()
            messages.error(request, "Invalid credentials! Please try again")
            return render(request, 'app/profile.html', {'form': fm, 'active': 'btn-primary'})







    else:

        fm = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': fm, 'active': 'btn-primary'})


def address(request):
    var = Customer.objects.filter(user=request.user)

    return render(request, 'app/address.html', {'var': var, 'active': 'btn-primary'})


def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


def change_password(request):
    if request.method == 'POST':
        fm = MyPasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Congratulations!! Your Password has been updated!!')
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return render(request, 'app/changepassword.html', {'form': fm})


    else:
        fm = MyPasswordChangeForm(user=request.user)
        return render(request, 'app/changepassword.html', {'form': fm})


def mobile(request):
    return render(request, 'app/mobile.html')


def login_user(request):
    if request.method == "POST":
        fm = LoginForm(request=request, data=request.POST)

        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']

            user = authenticate(username=uname, password=upass)
            print(user)

            if user is not None:
                login(request, user)
                messages.success(request, 'Congratulations!! Log In sucessfully!!')
                return redirect("profile")










    else:
        fm = LoginForm()
        return render(request, 'app/login.html', {'form': fm})

    fm = LoginForm()
    return render(request, 'app/login.html', {'form': fm})


def customerregistration(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()

        return redirect("login")
    else:
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')


def payment_done(request):
    custid = request.GET.get('custid')

    user = request.user
    cartid = Cart.objects.filter(user=user)
    customer = Customer.objects.get(id=custid)
    print(customer)
    for cid in cartid:
        OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
        print("Order Saved")
        cid.delete()
        print("Cart Item Deleted")
    return redirect("orders")
