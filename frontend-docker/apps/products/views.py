from django.shortcuts import render, redirect
from .forms import ProductForm
import requests
from .Car import Car
from .Product import Product
from apps.login.Auth import Auth
from django.contrib import messages


# Create your views here.
def form_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            prince = form.cleaned_data['prince']
            count = form.cleaned_data['count']
            data = {'count': count, 'prince': prince, 'name': name}
            resp = requests.post('http://localhost:3000/products/', data=data)
            if resp.status_code == 201:
                data_response = resp.json()
                print(data_response)

    if request.method == 'GET':
        form = ProductForm()

    return render(request, 'products/products.html', {'form': form})


def list_products(request):
    product = Product(request)
    auth = Auth(request)
    if request.method == 'GET':
        if auth.token is None:
            return redirect('login')
            if request.session.get('products') is None:
                resp = requests.get('http://localhost:3000/products/', headers={
                    'Authorization': f'Bearer {auth.token}',
                    'Content-Type': 'application/json'
                })
                if resp.status_code == 200:
                    data_response = resp.json()
                    products = data_response['result']['results']
                    product.set_list_products(products)
                    request.session.modified = True
                    request.session['car'] = {
                        'total': 0,
                        'products': {}
                    }
        return render(request, 'products/list_products.html', {'products': product.list})


def add_product_to_car(request, product_id):
    car = Car(request)
    product = Product(request)

    car.add_product(product.list[str(product_id)])
    return redirect('product_list')


def subtract_product(request, product_id):
    car = Car(request)
    product = Product(request)
    car.subtract(product.list[str(product_id)])
    return redirect('product_list')


def clean_car(request):
    car = Car(request)
    car.clean()
    return redirect('product_list')


def save_order(request):
    car = Car(request)
    auth = Auth(request)
    products = []
    for p in car.car['products'].values():
        products.insert(len(products) - 1, int(p['id']))
    data = {
        'paid': 0,
        'total': car.car['total'],
        'products': products,
        'payments': [],
        'user': 3
    }
    print(data)
    resp = requests.post('http://localhost:3000/orders/', data=data, headers={
        'Authorization': f'Bearer {auth.token}',
    })
    print(resp.status_code)
    print(resp.json())
    if resp.status_code == 200:
        messages.success(request, ":D")
        car.clean()
    return redirect('product_list')


def create_product(request):
    product = Product(request)
    auth = Auth(request)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            data = {'name': name, 'count': count, 'price': price}
            resp = requests.post('http://localhost:3000/products/', data=data, headers={
                'Authorization': f'Bearer {auth.token}',
                'Content-Type': 'application/json'
            })
            if resp.status_code == 201:
                data_response = resp.json()
                print(data_response)
                product.add_product(data_response)
                return redirect('product_list')

    if request.method == 'GET':
        form = ProductForm()

    return render(request, 'products/products.html', {'form': form, 'update': False})


def delete_product(request, product_id):
    product = Product(request)
    auth = Auth(request)
    token = f'Bearer {auth.token}'
    resp = requests.delete(f'http://localhost:3000/products/{product_id}', headers={
        'Authorization': token,
        'Content-Type': 'application/json'
    })
    if resp.status_code == 200:
        product.delete_product(product_id)
    return redirect('product_list')


def update_product(request, product_id):
    products = Product(request)
    product = products.list[str(product_id)]
    auth = Auth(request)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        name = form['name']
        count = form['count']
        price = form['price']
        data = {'name': name.value(), 'count': count.value(), 'price': price.value(), }
        print(data)
        resp = requests.put(f'http://localhost:3000/products/{product_id}/', data=data, headers={
            'Authorization': f'Bearer {auth.token}'
        })
        print(resp.status_code)
        data_response = resp.json()
        print(data_response)
        if resp.status_code == 200:
            products.add_product(data_response['result'])
            return redirect('product_list')
    elif request.method == 'GET':
        form = ProductForm(product)
    return render(request, 'products/products.html', {'form': form, 'update': True})
