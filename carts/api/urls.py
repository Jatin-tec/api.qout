from django.urls import path
from carts.api.views import CartView

urlpatterns = [
    path('', CartView.as_view(), name="cart"),
]
