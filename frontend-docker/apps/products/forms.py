from django import forms


class ProductForm(forms.Form):
    name = forms.CharField(label='Nombre', required=True)
    price = forms.IntegerField(label='Precio unitario', required=True)
    count = forms.IntegerField(label='Cantidad de productos', required=True)
