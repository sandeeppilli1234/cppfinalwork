from django.views.generic import ListView
from django.db.models.fields import EmailField
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from .models import Product, Order, Category
from UserLogin.models import User
# Create your views here.


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'ProductOrder/cart.html', {'products': products})


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        print(request.session.__dict__)
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            quantity = cart.get(str(product.id))
            order = Order(customer=User.objects.filter(email=customer)[0],
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=quantity)
            product.quantity = product.quantity - quantity
            product.save()
            order.save()
        request.session['cart'] = {}

        return render(request, "ProductOrder/checkout_done.html", {'products': products})

    def get(self, request):
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

        return render(request, "ProductOrder/checkout.html", {'products': products})


class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('customer'))
    return render(request, 'home.html', data)


class SearchProductListView(ListView):
    template_name = "search.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.filter(name__contains=query)
        return Product.objects.none()
