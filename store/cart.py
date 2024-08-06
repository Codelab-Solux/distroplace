from store.models import Product


class Cart:
    def __init__(self, req):
        self.session = req.session
        cart = self.session.get('cart', {})
        self.cart = cart
        self.session['cart'] = cart

    def add_item(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += 1
        else:
            self.cart[product_id] = {
                'price': str(product.promo_price if product.is_promoted else product.price),
                'quantity': 1
            }
        self.session.modified = True

    def remove_item(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
            else:
                del self.cart[product_id]
        self.session.modified = True

    def clear_item(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_cart_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []
        for product in products:
            item = {
                'product': product,
                'quantity': self.cart[str(product.id)]['quantity'],
                'total_price': float(self.cart[str(product.id)]['price']) * self.cart[str(product.id)]['quantity']
            }
            cart_items.append(item)
        return cart_items

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear_cart(self):
        self.session['cart'] = {}
        self.session.modified = True
