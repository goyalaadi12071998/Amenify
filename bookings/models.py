from django.db import models
from users.models import ExtendUser

class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Booking(models.Model):
    quantity = models.IntegerField()
    price = models.FloatField()
    user = models.ForeignKey(ExtendUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(default="created", max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
