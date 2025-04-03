from django.urls import path
from products.api.views import ProductView

urlpatterns = [
    path('', ProductView.as_view(), name="list-products"),
    path('<slug:barcode>/', ProductView.as_view(), name="product-detail")
]
