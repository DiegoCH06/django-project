from django import forms
from .Order import Order


class PaymentForm(forms.Form):
    total = forms.IntegerField(label='Total a Pagar', required=True, min_value=0, )
    orders = forms.ChoiceField(label='Orders', widget=forms.Select, choices= ())

    def __init__(self, *args, **kwargs):
        request = args[0]
        args = ()
        print(args)
        super(PaymentForm, self).__init__(*args, **kwargs)
        print("req ", request)
        session = request.session
        print(session)
        if session is not None:
            print('----')
            order = Order(request)
            orders = [(p['id'], p['total']) for p in order.list.values()]

            self.fields['orders'] = forms.MultipleChoiceField(label='Orders', required=True, choices=orders, widget=forms.CheckboxSelectMultiple(attrs={'class': 'orders'}))
            print(orders)