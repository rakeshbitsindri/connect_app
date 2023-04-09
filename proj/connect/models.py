from django.db import models

class Device(models.Model):
    hostname = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=15)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

