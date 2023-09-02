class Order:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        list = self.session.get('orders')

        if not list:
            self.clean()
            self.save_order()
        else:
            self.list = list

    def set_list_orders(self, orders):
        orders_dict = {}
        for o in orders:
            orders_dict[str(o['id'])] = o
        self.list = orders_dict
        self.save_order()

    def add_order(self, product):
        id = str(product['id'])
        self.list[id] = product
        self.save_order()

    def delete_order(self, product_id):
        id = str(product_id)
        if id in self.list.keys():
            del self.list[id]
            self.save_order()

    def clean(self):
        self.list = {}

    def save_order(self):
        self.session['orders'] = self.list
        self.session.modified = True
