from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _
from django.db import models
import  pandas as pd
from Shop.models import *
from django.conf import settings
User=settings.AUTH_USER_MODEL
class Phonesmscodecheck(models.Model):
    phone = PhoneNumberField(unique=True)
    smscode = models.CharField(max_length=6,null=False)
    def __str__(self):
        return str(self.phone)




class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birthday=models.DateField(null=True)
    def __str__(self):
        return str(self.user.phone)

class Location(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    latitude=models.CharField(max_length=200,null=True)
    longitude=models.CharField(max_length=200,null=True)
    def __str__(self):
        return f"{self.user.phone}"

class CustomerLike(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Customercard(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    productscolor = models.ForeignKey(ProductsColor,on_delete=models.CASCADE)
    productsize = models.ForeignKey(ProductSize,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,null=True)
    date = models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    user = models.ForeignKey(User,related_name="phoneW", on_delete= models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = {
        ('Start','Start'),
        ("To'lov","To'lov"),
        ('Buyurma','Buyurnama'),
        ("Jo'natildi","Jo'natildi"),
        ('Yetkazildi','Yetkazildi'),
        ('Buyurma bekor qilindi','Buyurma bekor qilindi'),
    }
    status = models.CharField(max_length=50, default='Start',choices=status)
    def __str__(self):
        return f"{self.user.phone} <=> {self.order_date}"
class Order_details(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    productscolor = models.ForeignKey(ProductsColor,on_delete=models.CASCADE)
    productsize = models.ForeignKey(ProductSize,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,null=True)
    @property
    def total(self):
        return self.quantity * self.product.price


class Question(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    question=models.CharField(max_length=500,null=False)
    date=models.DateTimeField(auto_now_add=True)
class Answertoquestion(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    name=models.CharField(max_length=10,null=False)
    answer=models.CharField(max_length=500,null=False)
    date=models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500,null=False)
    ball=models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

class ImagesReview(models.Model):
    reviews=models.ForeignKey(Review,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    image=models.ImageField()
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''


# class pay(models.Model):
#     pay_type = {
#         ('Naqd','Naqd'),
#         ('UzCard','UzCard'),
#         ('Humo','Humo'),
#         ('PaymeGo','PaymeGo'),
#         ('Click','Click')
#     }
#     seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
#     sale_date = models.DateTimeField(auto_now_add=True)
#     payment = models.CharField(max_length=10,default='Naqd',choices=pay_type)

#     def __str__(self):
#         return self.