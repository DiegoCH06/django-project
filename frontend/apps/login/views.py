from django.shortcuts import render, redirect
from .forms import LoginForm
import requests
from .Auth import Auth


# Create your views here.
def view_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            data = {'username': username, 'password': password}
            resp = requests.post('http://localhost:3000/auth/token/', data=data)
            if resp.status_code == 200:
                auth = Auth(request)
                data_response = resp.json()
                print(data_response)
                auth.add_tokens(data_response['access'], data_response['refresh'])
                return redirect('product_list')

    if request.method == 'GET':
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

