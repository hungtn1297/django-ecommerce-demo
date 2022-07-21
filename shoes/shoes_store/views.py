from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.cache import cache
from .models import Shoes, Categories, Customer, Cart, CartItem, Order, OrderItem
from .form import RegisterForm, PaymentForm, LoginForm


# Create your views here.
def index(request):
    if 'customer_id' in request.session:
        items = Shoes.objects.values()
        context = {
            'items': items,
        }
        template = loader.get_template('index.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect(login)


def contact(request):
    template = loader.get_template('contact.html')
    return HttpResponse(template.render({}, request))


def collection(request):
    template = loader.get_template('collection.html')
    return HttpResponse(template.render({}, request))


def shoes(request):
    template = loader.get_template('shoes.html')
    return HttpResponse(template.render({}, request))


def racing_boots(request):
    template = loader.get_template('racing boots.html')
    return HttpResponse(template.render({}, request))


def search(request):
    searchString = request.GET['q']
    items = Shoes.objects.filter(name__contains=searchString)
    context = {
        'items': items,
        'search_str': searchString
    }
    template = loader.get_template('search.html')
    return HttpResponse(template.render(context, request))


def detail(request, id):
    item = Shoes.objects.get(id=id)
    context = {
        'item': item
    }
    template = loader.get_template('detail.html')
    return HttpResponse(template.render(context, request))


def login(request):
    username = request.POST['username']
    password = request.POST['password']


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = request.POST['user_name']
            full_name = request.POST['full_name']
            phone = request.POST['phone']
            password = request.POST['password']
            email = request.POST['email']
            oCustomer = Customer(user_name=user_name, full_name=full_name, phone=phone, email=email, password=password)
            oCustomer.save()

            oCart = Cart(user_id=oCustomer)
            oCart.save()

            request.session['customer_id'] = oCustomer.id
            return redirect(index)
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


def add_to_cart(request):
    if is_ajax(request=request) and request.method == 'POST':
        customer_id = request.session['customer_id']
        cart_obj = Cart.objects.get(user_id=customer_id)
        if cart_obj and cart_obj.id:
            item_id = request.POST['item_id']
            item = Shoes.objects.get(id=item_id)
            cart_item_obj = CartItem.objects.filter(cart_id=cart_obj, item_id=item).first()
            if cart_item_obj:
                cart_item_obj.quantity += 1
            else:
                cart_item_obj = CartItem(cart_id=cart_obj, item_id=item)
            cart_item_obj.save()
            return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'error': 'error'}, status=400)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def cart(request):
    template = loader.get_template('cart.html')
    customer_obj = Customer.objects.get(id=request.session['customer_id'])
    cart_obj = Cart.objects.get(user_id=customer_obj)
    cart_item = CartItem.objects.filter(cart_id=cart_obj)
    total = 0
    form = PaymentForm(request=request, order='')
    for item in cart_item:
        total += item.item_id.price * item.quantity
    context = {
        'cart_item': cart_item,
        'total': total,
        'form': form
    }
    return HttpResponse(template.render(context, request))


def payment(request):
    if request.method == 'POST':
        customer_obj = Customer.objects.get(id=request.POST['customer_id'])
        cart_ojb = Cart.objects.get(user_id=customer_obj.id)
        cart_item_obj = CartItem.objects.filter(cart_id=cart_ojb)

        full_name = request.POST['full_name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']

        order_obj = Order(user_id=customer_obj, full_name=full_name, phone=phone, email=email, address=address)
        order_obj.save()

        for item in cart_item_obj:
            order_item_obj = OrderItem(
                order_id=order_obj,
                item_id=item.item_id,
                quantity=item.quantity,
                price=item.item_id.price)
            order_item_obj.save()
            item.delete()

        return redirect('payment_success')



def payment_success(request):
    template = loader.get_template('payment_success.html')
    return HttpResponse(template.render({}, request))


def order(request):
    template = loader.get_template('order.html')
    customer_obj = Customer.objects.get(id=request.session['customer_id'])
    order_obj = Order.objects.filter(user_id=customer_obj)
    results = []
    for order in order_obj:
        cart_item = OrderItem.objects.filter(order_id=order)
        total = 0
        form = PaymentForm(request=request, order=order)
        for item in cart_item:
            total += item.item_id.price * item.quantity
        results.append({
            'order_id': order.id,
            'cart_item': cart_item,
            'total': total,
            'form': form
        })

    context = {
        'results': results
    }
    return HttpResponse(template.render(context, request))


def logout(request):
    del request.session['customer_id']
    return redirect('index')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = request.POST['user_name']
            password = request.POST['password']
            oCustomer = Customer.objects.filter(user_name=user_name, password=password).first()

            if (oCustomer):
                request.session['customer_id'] = oCustomer.id
            return redirect(index)
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})



