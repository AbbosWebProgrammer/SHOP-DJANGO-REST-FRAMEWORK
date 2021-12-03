from django.db import models
from Shop.models import *


#  Home Page Reklama For Brang
def shoppingdayforhomepagecarousel_path(instance, filename):
    return 'Advertising/HomePage/ShoppingDayForHomePageCarousel/{0}/{1}'.format(instance.name,filename)
class ShoppingDayForHomePageCarousel(models.Model):
    name=models.CharField(max_length=200,null=False)
    image = models.ImageField(upload_to=shoppingdayforhomepagecarousel_path)
    category=models.ManyToManyField(Category,blank=True)
    subcategory=models.ManyToManyField(Subcategory,blank=True)
    subsubcategory=models.ManyToManyField(Subsubcategory,blank=True)
    brand=models.ManyToManyField(Brand,blank=True)
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
        db_table = 'ShoppingDayForHomePageCarousel'
        verbose_name = 'ShoppingDayForHomePageCarousel'
        verbose_name_plural = 'ShoppingDayForHomePageCarousels'

#   Home Page Reklama For Brang
def mainpagepromoforhomepage_path(instance, filename):
    return 'Advertising/HomePage/MainPagePromoForHomePage/{0}/{1}'.format(instance.brand.name,filename)
class MainPagePromoForHomePage(models.Model):
    name=models.CharField(max_length=200,null=False)
    image = models.ImageField(upload_to=mainpagepromoforhomepage_path)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    category=models.ManyToManyField(Category,blank=True)
    subcategory=models.ManyToManyField(Subcategory,blank=True)
    subsubcategory=models.ManyToManyField(Subsubcategory,blank=True)
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return self.brand.name
    class Meta:
        ordering = ['id']
        db_table = 'MainPagePromoForHomePage'
        verbose_name = 'MainPagePromoForHomePage'
        verbose_name_plural = 'MainPagePromoForHomePages'

#  Home Page Reklama For Brang Sileder
def mainpagepromoforhomepageslider_path(instance, filename):
    return 'Advertising/HomePage/MainPagePromoForHomePageSlider/{0}/{1}'.format(instance.brand.name,filename)
class MainPagePromoForHomePageSlider(models.Model):
    name=models.CharField(max_length=200,null=False)
    image = models.ImageField(upload_to=mainpagepromoforhomepageslider_path)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    category=models.ManyToManyField(Category,blank=True)
    subcategory=models.ManyToManyField(Subcategory,blank=True)
    subsubcategory=models.ManyToManyField(Subsubcategory,blank=True)
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return self.brand.name
    class Meta:
        ordering = ['id']
        db_table = 'MainPagePromoForHomePageSlider'
        verbose_name = 'MainPagePromoForHomePageSlider'
        verbose_name_plural = 'MainPagePromoForHomePageSliders'

# Reklama For Category id in Category Menu
def categorymenuadvertising_path(instance, filename):
    return 'Advertising/CategoryMenu/{0}/{1}'.format(instance.category.categoryname,filename)
class AdvertisingForCategoryMenu(models.Model):
    name=models.CharField(max_length=200,null=False)
    image = models.ImageField(upload_to=categorymenuadvertising_path)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ManyToManyField(Subcategory,blank=True)
    subsubcategory=models.ManyToManyField(Subsubcategory,blank=True)
    brand=models.ManyToManyField(Brand,blank=True)
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
        db_table = 'AdvertisingForCategoryMenu'
        verbose_name = 'AdvertisingForCategoryMenu'
        verbose_name_plural = 'AdvertisingForCategoryMenus'

# Reklama for category page carusel 
def shoppingdayforcategorycarusel_path(instance, filename):
    return 'Advertising/Category/ShoppingDayForCategoryCarousel/{0}/{1}'.format(instance.category.categoryname,filename)
class ShoppingDayForCategoryCarousel(models.Model):
    name=models.CharField(max_length=200,null=False)
    image = models.ImageField(upload_to=shoppingdayforcategorycarusel_path)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ManyToManyField(Subcategory,blank=True)
    subsubcategory=models.ManyToManyField(Subsubcategory,blank=True)
    brand=models.ManyToManyField(Brand,blank=True)
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
        db_table = 'ShoppingDayForCategoryCarousel'
        verbose_name = 'ShoppingDayForCategoryCarousel'
        verbose_name_plural = 'ShoppingDayForCategoryCarousels'


# Reklama for category page
def shoppingdayformainpagepromoforcategory_path(instance, filename):
    return 'Advertising/Category/MainPagePromoForCategory/{0}/{1}'.format(instance.category.categoryname,filename)
class MainPagePromoForCategory(models.Model):
    name=models.CharField(max_length=200,null=False)
    image = models.ImageField(upload_to=shoppingdayformainpagepromoforcategory_path)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ManyToManyField(Subcategory,blank=True)
    subsubcategory=models.ManyToManyField(Subsubcategory,blank=True)
    brand=models.ManyToManyField(Brand,blank=True)
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return self.brand.name
    class Meta:
        ordering = ['id']
        db_table = 'MainPagePromoForCategory'
        verbose_name = 'MainPagePromoForCategory'
        verbose_name_plural = 'MainPagePromoForCategorys'


# Reklama for brand page carusel 
def shoppingdayforbrandcarusel_path(instance, filename):
    return 'Advertising/Brand/ShoppingDayForBrandCarousel/{0}/{1}'.format(instance.brand.name,filename)
class ShoppingDayForBrandCarousel(models.Model):
    name=models.CharField(max_length=200,null=False)
    image = models.ImageField(upload_to=shoppingdayforbrandcarusel_path)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    category=models.ManyToManyField(Category,blank=True)
    subcategory=models.ManyToManyField(Subcategory,blank=True)
    subsubcategory=models.ManyToManyField(Subsubcategory,blank=True)
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
        db_table = 'ShoppingDayForBrandCarousel'
        verbose_name = 'ShoppingDayForBrandCarousel'
        verbose_name_plural = 'ShoppingDayForBrandCarousels'

# Reklama for brand page
def mainpagepromoforbrand_path(instance, filename):
    return 'Advertising/Brand/MainPagePromoForBrand/{0}/{1}'.format(instance.brand.name,filename)
class MainPagePromoForBrand(models.Model):
    name=models.CharField(max_length=200,null=False)
    image = models.ImageField(upload_to=mainpagepromoforbrand_path)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    category=models.ManyToManyField(Category,blank=True)
    subcategory=models.ManyToManyField(Subcategory,blank=True)
    subsubcategory=models.ManyToManyField(Subsubcategory,blank=True)
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return self.brand.name
    class Meta:
        ordering = ['id']
        db_table = 'MainPagePromoForBrand'
        verbose_name = 'MainPagePromoForBrand'
        verbose_name_plural = 'MainPagePromoForBrands'




