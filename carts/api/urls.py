from django.urls import path
from carts.api.views import (
    StartCartSessionView,
    AddCartItemView,
    AddCartItemViewWithoutSession,
    RemoveCartItemView,
    RemoveCartItemViewWithoutSession,
    ViewCartSessionView,
    ViewCartSessionViewWithoutSession,
    CheckoutCartSessionView,
    GetActiveSession
)

urlpatterns = [
    path('start/<uuid:cart_id>/', StartCartSessionView.as_view(), name='start-cart-session'),
    path('session/<int:session_id>/', ViewCartSessionView.as_view(), name='view-cart-session'),
    path('session/<int:session_id>/add/', AddCartItemView.as_view(), name='add-cart-item'),
    path('session/<int:session_id>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    path('session/<int:session_id>/checkout/', CheckoutCartSessionView.as_view(), name='checkout-cart'),

    path('active-session/<slug:cart_id>/', GetActiveSession.as_view(), name='cart-session'),
    path('cart/session/<int:session_id>/', ViewCartSessionViewWithoutSession.as_view(), name='view-cart-session'),
    path('cart/session/<int:session_id>/add/', AddCartItemViewWithoutSession.as_view(), name='add-from-cart'),
    path('cart/session/<int:session_id>/remove/', RemoveCartItemViewWithoutSession.as_view(), name='remove-from-item'),
]
