from decimal import Decimal
from django.conf import settings
from craft.models import Product


class Cart(object):

    def __init__(self, request):
        """ Инициализация корзины """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохроняем пустую корзину
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """ Перебераем товары в корзине и получаем товары из базы данных """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        # считаем колличесво и цену
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ Считаем количество товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def add_product(self, product, quantity=1, update_quantity=False):
        """ Добавляем товар в корзину и обновляем его колличесто """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        """сохроняем товар в корзине"""
        self.session.modified = True

    def remove(self, product):
        """Удаление продукта из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        # счет общей стоймости товаров
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear_cart(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
