from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class StoreStaff(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.role} at {self.store.name}"
