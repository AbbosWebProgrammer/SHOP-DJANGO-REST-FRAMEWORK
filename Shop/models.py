from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length = 50,null=False)
    description = models.CharField(max_length=200,null=True)
    views=models.IntegerField(null=True,default=0)
    def __str__(self):
        return self.category_name
class Subcategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length = 50,null=False)
    views=models.IntegerField(null=True,default=0)
    description = models.CharField(max_length=200,null=True)
    def __str__(self):
        return f"{self.category.category_name} <=> {self.subcategory_name}"
class Products(models.Model):
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=False)
    price = models.FloatField(default=0,null=True)
    discounts = models.DecimalField(decimal_places=0, max_digits=100)
    oldprice = models.FloatField(default=0,null=True)
    delivery= models.IntegerField(default=3,)
    buy_quantity= models.IntegerField(default=3,)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.subcategory.subcategory_name}||{self.name}"

class Descproduct(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='Description')
    description= models.CharField(max_length=600)
    date_time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class ProductsColor(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    colorname=models.CharField(max_length=100,default=None)
    def __str__(self):
        return f"{self.product.subcategory.subcategory_name} <||> {self.product.name} <||> {self.colorname}"

class ProductSize(models.Model):
    productscolor = models.ForeignKey(ProductsColor,on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    quentity = models.IntegerField(default=0,null=True)
    def __str__(self):
        return str(self.size)

class Imagefiles(models.Model):
    productscolor = models.ForeignKey(ProductsColor,on_delete=models.CASCADE)
    alt = models.CharField(max_length=200,null=False)
    image = models.ImageField()
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
class ProductParamsCaption(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    captionname=models.CharField(max_length=100,null=False)
    def __str__(self):
        return self.captionname

class ProductParamsCaptionitems(models.Model):
    productparamscaption=models.ForeignKey(ProductParamsCaption,on_delete=models.CASCADE)
    paramscell=models.CharField(max_length=100,null=False)
    paramscelldecor=models.CharField(max_length=100,null=False)
    def __str__(self):
        return self.paramscell


