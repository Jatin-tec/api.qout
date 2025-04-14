from django.urls import path
from products.api.views import ProductView, sum_, ProductAddView, ProductEditView

urlpatterns = [
    path('', ProductView.as_view(), name="list-products"),
    path('<slug:barcode>/', ProductView.as_view(), name="product-detail"),
    path('sum/<int:num1>/<int:num2>/', sum_, name='sum')
]
