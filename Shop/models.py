from django.db import models

def category_path(instance, filename):
    return 'Category/{0}/{1}'.format(instance.categoryname,filename)
class Category(models.Model):
    categoryname = models.CharField(max_length = 100,null=False)
    description = models.CharField(max_length=200,null=True)
    views=models.IntegerField(default=0)
    image = models.ImageField(upload_to=category_path)
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return f'''{self.category.id} {self.categoryname}'''
    class Meta:
        ordering = ['id']
        db_table = 'Category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Subcategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    subcategoryname = models.CharField(max_length = 100,null=False)
    description = models.CharField(max_length=200,null=True)
    views=models.IntegerField(default=0)
    def __str__(self):
        return f'''{self.category} % {self.id} {self.subcategoryname}'''
    class Meta:
        ordering = ['id']
        db_table = 'Subcategory'
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

class Subsubcategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.SET_NULL,null=True)
    subsubcategoryname = models.CharField(max_length = 100,null=False)
    views=models.IntegerField(default=0)
    description = models.CharField(max_length=200,null=True)
    def __str__(self):
        return f'''{self.subcategory.category.categoryname} % {self.subcategory.subcategoryname} % {self.subsubcategoryname}'''
    class Meta:
        ordering = ['id']
        db_table = 'Subsubcategory'
        verbose_name = 'Subsubcategory'
        verbose_name_plural = 'Subsubcategories'

def brand_path(instance, filename):
    return 'Brand/{0}/{1}'.format(instance.name,filename)
class Brand(models.Model):
    name = models.CharField(max_length=200,null=False)
    description = models.CharField(max_length=1000,null=True)
    views=models.IntegerField(default=0)
    image = models.ImageField(upload_to=brand_path)
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return str(self.name)
    class Meta:
        ordering = ['id']
        db_table = 'Brand'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.SET_NULL,null=True)
    subsubcategory = models.ForeignKey(Subsubcategory,on_delete=models.SET_NULL,null=True)
    brand=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    productname = models.CharField(max_length=500,null=False)
    sameprice=models.BooleanField(default=False)
    price = models.FloatField(default=0,null=True)
    oldprice = models.FloatField(default=0,null=True)
    delivery= models.IntegerField(default=1)
    sellingcompany=models.CharField(default="Alsafia",max_length=200,null=False)
    buy_quantity= models.IntegerField(default=1)
    shoppingday=models.BooleanField(default=False)
    product_status=models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    addproductUrl=models.CharField(default="http://Alsafia.uz/",max_length=200,null=False)
    imagealt = models.CharField(max_length=1000,null=True)
    views=models.IntegerField(default=0)
    def __str__(self):
        return f'''{self.id} {self.subsubcategory} % {self.productname}'''
    @property
    def product_discount(self):
        k = int(100*(self.oldprice-self.price)/self.oldprice)
        if k>0:
                return f'''-{k}'''
        else:
                return f'''+{-k}'''

    class Meta:
        ordering = ['id']
        db_table = 'Product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductColor(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    colorname=models.CharField(max_length=100,default=None)
    price = models.FloatField(null=True)
    oldprice = models.FloatField(null=True)
    allquantity = models.IntegerField(default=0)
    @property
    def product_discount(self):
        k = int(100*(self.oldprice-self.price)/self.oldprice)
        if k>0:
                return f'''-{k}'''
        else:
                return f'''+{-k}'''
    def save(self, *args, **kwargs):
        if not self.price:
              self.price = self.product.price
        if not self.oldprice:
              self.oldprice = self.product.oldprice
        super(ProductColor, self).save(*args, **kwargs)
    def __str__(self):
        return f'''{self.product} % {self.colorname}'''
    class Meta:
        ordering = ['id']
        db_table = 'ProductColor'
        verbose_name = 'ProductColor'
        verbose_name_plural = 'ProductColors'


class ProductSize(models.Model):
    productscolor = models.ForeignKey(ProductColor,on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    quentity = models.IntegerField(default=0,null=True)
    def __str__(self):
        return f'''{self.productscolor} % {self.size}'''
    class Meta:
        ordering = ['id']
        db_table = 'ProductSize'
        verbose_name = 'ProductSize'
        verbose_name_plural = 'ProductSizes'

def product_path(instance, filename):
    k='`~<>,.:;[!@#$}\'"{?|/\*-+=()]^'
    category=instance.productscolor.product.category
    subcategory=instance.productscolor.product.subcategory
    subsubcategory=instance.productscolor.product.subsubcategory
    name=instance.productscolor.product.productname
    for char in name:
        if char in k:
            name = name.replace(char,'')
    if subsubcategory is  None:
        return 'Products/{0}/{1}/{2}/{3}/{4}'.format(category.categoryname,
                                            subcategory.subcategoryname,
                                            name,
                                            instance.productscolor.colorname,filename)
    else:
        return 'Products/{0}/{1}/{2}/{3}/{4}/{5}'.format(category.categoryname,
                                            subcategory.subcategoryname,
                                            subsubcategory.subsubcategoryname,
                                            name,
                                            instance.productscolor.colorname,filename)

class ProductImageFile(models.Model):
    productscolor = models.ForeignKey(ProductColor,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_path)
    @property
    def imageURL(self):
        try: return self.image.url
        except: return ''
    class Meta:
        ordering = ['id']
        db_table = 'ProductImageFile'
        verbose_name = 'ProductImageFile'
        verbose_name_plural = 'ProductImageFiles'

class DescriptionForProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='None')
    description= models.CharField(max_length=600)
    date_time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name)
    class Meta:
        ordering = ['id']
        db_table = 'DescriptionForProduct'
        verbose_name = 'DescriptionForProduct'
        verbose_name_plural = 'DescriptionForProducts'

class ProductParamsCaption(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    captionname=models.CharField(max_length=100,default='None',null=False)
    def __str__(self):
        return str(self.captionname)
    class Meta:
        ordering = ['id']
        db_table = 'ProductParamsCaption'
        verbose_name = 'ProductParamsCaption'
        verbose_name_plural = 'ProductParamsCaptions'

class ProductParamsCaptionitem(models.Model):
    productparamscaption=models.ForeignKey(ProductParamsCaption,on_delete=models.CASCADE)
    paramscell=models.CharField(max_length=100,null=False)
    paramscelldecor=models.CharField(max_length=100,null=False)
    def __str__(self):
        return self.paramscell
    class Meta:
        ordering = ['id']
        db_table = 'ProductParamsCaptionitem'
        verbose_name = 'ProductParamsCaptionitem'
        verbose_name_plural = 'ProductParamsCaptionitems'
