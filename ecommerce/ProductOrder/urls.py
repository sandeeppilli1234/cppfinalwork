from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .views import Index, store, Cart, OrderView, CheckOut, SearchProductListView


def auth_middleware(get_response):

    def middleware(request):
        print(request.session.get('customer'))
        returnUrl = request.META['PATH_INFO']
        print(request.META['PATH_INFO'])
        if not request.session.get('customer'):
            return redirect(f'UserLogin/login?return_url={returnUrl}')

        response = get_response(request)
        return response

    return middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store, name='store'),
    path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('store/search', SearchProductListView.as_view(), name="search_products")


]
