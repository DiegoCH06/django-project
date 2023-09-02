from django.shortcuts import render, redirect
from .Payment import Payment
from .Order import Order
from .forms import PaymentForm
from apps.login.Auth import Auth
from requests import get, post, delete
import asyncio
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def list_payments(request):
    payment = Payment(request)
    auth = Auth(request)
    if request.method == 'GET':
        #if request.session.get('payments') is None:
        resp = get('http://localhost:3000/payments/', headers={
                'Authorization': f'Bearer {auth.token}',
                'Content-Type': 'application/json'
            })
        asyncio.run(get_orders(request))
        print(resp.status_code)
        data_response = resp.json()
        print(data_response)
        if resp.status_code == 200:
            payments = data_response['result']['results']
            payment.set_list_payments(payments)
        elif resp.status_code == 401:
            return redirect('login')
        return render(request, 'payments/list_payments.html', {'products': payment.list})


def create_payment(request):
    product = Payment(request)
    auth = Auth(request)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            data = {'name': name, 'count': count, 'price': price}
            resp = post('http://localhost:3000/payments/', data=data, headers={
                'Authorization': f'Bearer {auth.token}'
            })
            if resp.status_code == 201:
                data_response = resp.json()
                print(data_response)
                product.add_product(data_response)
                return redirect('product_list')

    if request.method == 'GET':
        form = PaymentForm(request)

    return render(request, 'payments/upset_payment.html', {'form': form, 'update': False})


def delete_payment(request, payment_id):
    payment = Payment(request)
    auth = Auth(request)
    token = f'Bearer {auth.token}'
    resp = delete(f'http://localhost:3000/payments/{payment_id}', headers={
        'Authorization': token,
        'Content-Type': 'application/json'
    })
    if resp.status_code == 200:
        payment.delete_payment(payment_id)
    return redirect('list_payments')

@csrf_exempt
def select_order(request):
    print(request.POST.get('selected_value'))
    payment = Payment(request)
    payment.upset_order_selected(request.POST.get('selected_value'))
    return redirect('CreatePayment')


async def get_orders(request):
    order = Order(request)
    auth = Auth(request)
    resp = get('http://localhost:3000/orders/', headers={
                'Authorization': f'Bearer {auth.token}',
                'Content-Type': 'application/json'
            })
    print('get_orders', resp.status_code)
    print('get_orders', resp.json())
    if resp.status_code == 200:
        data_response = resp.json()
        orders = data_response['result']['results']
        order.set_list_orders(orders)