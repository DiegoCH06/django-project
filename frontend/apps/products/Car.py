from apps.products.Product import Product
class Car:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        car = self.session['car']
        if not car:
            self.clean()
            self.car = self.session['car']
        else:
            self.car = car

    def add_product(self, product):
        id = str(product['id'])
        product_class = Product(self.request)
        if id not in self.car['products'].keys():
            self.car['products'][id] = {
                "name": product['name'],
                "id": product['id'],
                "price": product['price'],
                "count": product['count'],
                "items": 1
            }
            self.car['total'] += product['price']
        elif product_class.list[id]['count'] > self.car['products'][id]["items"]:
            self.car['products'][id]["items"] += 1
            self.car['products'][id]["price"] += product['price']
            self.car['total'] += product['price']
        self.save_car()

    def save_car(self):
        self.session['car'] = self.car
        self.session.modified = True

    def delete_product(self, product):
        id = str(product['id'])
        if id in self.car['products'].keys():
            del self.car['products'][id]
            self.save_car()

    def subtract(self, product):
        id = str(product['id'])
        if id in self.car['products'].keys():
                self.car['products'][id]['items'] -= 1
                self.car['products'][id]['price'] -= product['price']
                self.car['total'] -= product['price']
                if self.car['products'][id]['items'] < 1:
                    self.delete_product(product)
                self.save_car()

    def clean(self):
        self.session['car'] = {
            'total': 0,
            'products': {}
        }
        self.session.modified = True
        self.car = self.session['car']
        self.save_car()