from django.db import models
from users.models import CustomUser
from store.models import Store
import uuid

class Cart(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('idle', 'Idle'),
        ('charging', 'Charging'),
        ('full_charged', 'Full Charged')
    )

    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='full_charged')

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.store.name}"

    class Meta:
        verbose_name_plural = "Carts"

class CartSession(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    is_checked_out = models.BooleanField(default=False)

    def __str__(self):
        return f"Session for {self.cart.cart_id} by {self.user.email}"

    class Meta:
        verbose_name_plural = "Cart Sessions"
        ordering = ['-started_at']

class CartItem(models.Model):
    session = models.ForeignKey(CartSession, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in session {self.session.id}"

    class Meta:
        verbose_name_plural = "Cart Items"