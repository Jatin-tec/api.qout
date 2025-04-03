from django.db import models
from users.models import CustomUser
import uuid

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    status = models.CharField(max_length=255)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Carts"

class UserCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart"

    class Meta:
        unique_together = ('user', 'cart')
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in cart {self.cart.id}"

    class Meta:
        verbose_name_plural = "Cart Items"