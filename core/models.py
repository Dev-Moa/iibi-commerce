from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


class CustomUser(AbstractUser):
    profile = models.FileField(null=True ,upload_to="profiles")


class Category (models.Model):
    category_name = models.CharField(null=True ,max_length=100)

    def __str__(self):
        return self.category_name
    
    def get_absolute_url(self):
        return reverse("category_detail", args=[self.category_name])
    

class Product(models.Model):
    name=models.CharField(max_length=100)
    image = models.FileField(blank=True ,upload_to='products')
    owner =  models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="products"
        )
    description = models.CharField(null=True ,max_length=200)
    category = models.ManyToManyField(Category, related_name="products" )
    price = models.PositiveIntegerField(null=True)
    date = models.DateField(auto_now=True)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("product_detail", args=[self.id])
    