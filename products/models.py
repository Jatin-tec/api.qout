from django.db import models
from store.models import Store
import random
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    
    product_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    barcode = models.BigIntegerField(unique=True, blank=True, null=True)
    
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.barcode:
            while True:
                new_barcode = random.randint(10**7, 10**8 - 1)
                if not Product.objects.filter(barcode=new_barcode).exists():
                    self.barcode = new_barcode
                    break
        super().save(*args, **kwargs)
