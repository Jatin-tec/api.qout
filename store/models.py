from django.db import models
from users.models import CustomUser

class Store(models.Model):
    name = models.CharField(max_length=255)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_stores', null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name

class StoreStaff(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.role} at {self.store.name}"
