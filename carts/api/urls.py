from django.urls import path
from carts.api.views import (
    StartCartSessionView,
    AddCartItemView,
    RemoveCartItemView,
    ViewCartSessionView,
    CheckoutCartSessionView,
    CartView
)

urlpatterns = [
    path('', CartView.as_view(), name='cart'),

    path('start/<uuid:cart_id>/', StartCartSessionView.as_view(), name='start-cart-session'),
    path('session/<int:session_id>/', ViewCartSessionView.as_view(), name='view-cart-session'),
    path('session/<int:session_id>/add/', AddCartItemView.as_view(), name='add-cart-item'),
    path('session/<int:session_id>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    path('session/<int:session_id>/checkout/', CheckoutCartSessionView.as_view(), name='checkout-cart'),
]
