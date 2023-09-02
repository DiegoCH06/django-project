class Product:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        list = self.session['products']

        if not list:
            self.clean()
        else:
            self.list = list
        self.save_product()

    def set_list_products(self, products):
        products_dict = {}
        for p in products:
            products_dict[str(p['id'])] = p
        self.list = products_dict
        self.save_product()

    def add_product(self, product):
        id = str(product['id'])
        self.list[id] = product
        print('save ', product)
        self.save_product()

    def delete_product(self, product_id):
        id = str(product_id)
        if id in self.list.keys():
            del self.list[id]
            self.save_product()

    def clean(self):
        self.list = {}

    def save_product(self):
        self.session['products'] = self.list
        self.session.modified = True
