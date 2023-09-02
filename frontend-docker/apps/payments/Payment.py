from .Order import Order


class Payment:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        list = self.session.get('payments')
        orders_selected = self.session.get('orders_selected')

        if not list:
            self.list = {}

        else:
            self.list = list

        if not orders_selected:
            self.orders_selected = {}

        else:
            self.orders_selected = orders_selected

        self.save_payment()

    def set_list_payments(self, payments):
        payments_dict = {}
        for p in payments:
            payments_dict[str(p['id'])] = p
        self.list = payments_dict
        self.save_payment()

    def add_payment(self, payment):
        id = str(payment['id'])
        self.list[id] = payment
        self.save_payment()

    def delete_payment(self, payment_id):
        id = str(payment_id)
        if id in self.list.keys():
            del self.list[id]
            self.save_payment()

    def upset_order_selected(self, order_id):
        id = str(order_id)
        order = Order(self.request)
        print('UPSET')
        if id not in self.orders_selected.keys():
            self.orders_selected[id] = order.list[id]
        else:
            del self.orders_selected[id]
        self.save_payment()

    def clean(self):
        self.list = {}
        self.orders_selected = {}

    def save_payment(self):
        self.session['payments'] = self.list
        self.session['orders_selected'] = self.orders_selected
        self.session.modified = True
