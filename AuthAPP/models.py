from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _
from django.db import models
import  pandas as pd
from Shop.models import *
from django.conf import settings
User=settings.AUTH_USER_MODEL

class CheckTheSmsCodeSentToThePhone(models.Model):
    phone = PhoneNumberField(unique=True)
    smscode = models.CharField(max_length=6,null=False)
    def __str__(self):
        return str(self.phone)
    class Meta:
        ordering = ['id']
        db_table = 'CheckTheSmsCodeSentToThePhone'
        verbose_name = 'CheckTheSmsCodeSentToThePhone'
        verbose_name_plural = 'CheckTheSmsCodeSentToThePhones'

class Location(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    city = models.CharField(max_length=200, blank=True, null=True, verbose_name="Shahar / Viloyat")
    district = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tuman")
    street = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ko'cha")
    def __str__(self):
        return f"{self.user.phone}"
    class Meta:
        ordering = ['id']
        db_table = 'Location'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class GoodsThatTheCustomerLikes(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} % {self.product}"
    class Meta:
        ordering = ['id']
        db_table = 'GoodsThatTheCustomerLikes'
        verbose_name = 'GoodsThatTheCustomerLikes'
        verbose_name_plural = 'GoodsThatTheCustomerLikess'



class Order(models.Model):
    status = {
        ('Buyurma','Buyurnama'),
        ("Jo'natildi","Jo'natildi"),
        ('Yetkazildi','Yetkazildi'),
        ('Buyurma bekor qilindi','Buyurma bekor qilindi'),
    }
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    phone = PhoneNumberField()
    firstname = models.CharField(max_length=100,blank=True)
    lastname = models.CharField(max_length=100,blank=True)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=200, blank=True, null=True, verbose_name="Shahar / Viloyat")
    district = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tuman")
    street = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ko'cha")
    status = models.CharField(max_length=50, default='Buyurnama',choices=status)
    vendoradd=models.BooleanField(default=False)
    vendorphone = PhoneNumberField(blank=True)
    vendorfirstname = models.CharField(max_length=100,blank=True)
    vendorlastname = models.CharField(max_length=100,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    supported=models.BooleanField(default=False)
    @property
    def day(self):
        return pd.to_datetime(self.date).strftime("%m/%d/%Y")
    @property
    def time(self):
        return pd.to_datetime(self.date).strftime("%H:%M:%S")
    def __str__(self):
        return f"{self.phone}  {self.day}  {self.time}"
    class Meta:
        ordering = ['id']
        db_table = 'Order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    productcolor = models.ForeignKey(ProductColor,blank=True,on_delete=models.SET_NULL,null=True)
    productsize = models.ForeignKey(ProductSize,blank=True,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1,null=True)
    price = models.FloatField(null=True)
    oldprice = models.FloatField(null=True)
    discount=models.IntegerField(null=True)
    totalprice=models.FloatField(null=True)
    
    def save(self, *args, **kwargs):
        self.price = self.productcolor.price
        self.oldprice = self.productcolor.oldprice
        self.discount = self.productcolor.product_discount
        self.totalprice = self.productcolor.price*self.quantity
        super(OrderDetail, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.product.productname}  {self.productcolor.colorname}  {self.productsize.size}  {self.quantity}"
    class Meta:
        ordering = ['id']
        db_table = 'OrderDetail'
        verbose_name = 'OrderDetail'
        verbose_name_plural = 'OrderDetails'


class Pay(models.Model):
    pay_type = {
        ('Naqd','Naqd'),
        ('UzCard','UzCard'),
        ('Humo','Humo'),
        ('PaymeGo','PaymeGo'),
        ('Click','Click')
    }
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    payment = models.CharField(max_length=10,default='Naqd',choices=pay_type)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.order
    class Meta:
        ordering = ['id']
        db_table = 'Pay'
        verbose_name = 'Pay'
        verbose_name_plural = 'Pays'

class QuestionForProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    question=models.CharField(max_length=500,null=False)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['id']
        db_table = 'QuestionForProduct'
        verbose_name = 'QuestionForProduct'
        verbose_name_plural = 'QuestionForProducts'

class Answertoquestion(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    question = models.ForeignKey(QuestionForProduct,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,default="Brend vakili",null=False)
    answer=models.CharField(max_length=500,null=False)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['id']
        db_table = 'Answertoquestion'
        verbose_name = 'Answertoquestion'
        verbose_name_plural = 'Answertoquestions'


class Review(models.Model):
    product = models.ForeignKey(OrderDetail,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500,null=False)
    ball=models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    class Meta:
        ordering = ['id']
        db_table = 'Review'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

class ImagesReview(models.Model):
    review=models.ForeignKey(Review,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    image=models.ImageField()
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    class Meta:
        ordering = ['id']
        db_table = 'ImagesReview'
        verbose_name = 'ImagesReview'
        verbose_name_plural = 'ImagesReviews'


