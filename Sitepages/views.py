from django.core.files.base import ContentFile
from django.http.request import QueryDict
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import viewsets
from django.shortcuts import render
from Shop.serializer import * 
from .serializer import * 
from .models import *
from PIL import Image
import io, base64
import uuid
import json

class ShoppingDayForHomePageCarouselView(viewsets.ModelViewSet):
    queryset=ShoppingDayForHomePageCarousel.objects.all()
    serializer_class=ShoppingDayForHomePageCarouselSerializer  

class MainPagePromoForHomePageView(viewsets.ModelViewSet):
    queryset=MainPagePromoForHomePage.objects.all()
    serializer_class=MainPagePromoForHomePageSerializer

class MainPagePromoForHomePageSliderView(viewsets.ModelViewSet):
    queryset=MainPagePromoForHomePageSlider.objects.all()
    serializer_class=MainPagePromoForHomePageSliderSerializer

class AdvertisingForCategoryMenuView(viewsets.ModelViewSet):
    queryset=AdvertisingForCategoryMenu.objects.all()
    serializer_class=AdvertisingForCategoryMenuViewSerializer

class ShoppingDayForCategoryCarouselView(viewsets.ModelViewSet):
    queryset=ShoppingDayForCategoryCarousel.objects.all()
    serializer_class=ShoppingDayForCategoryCarouselSerializer

class MainPagePromoForCategoryView(viewsets.ModelViewSet):
    queryset=MainPagePromoForCategory.objects.all()
    serializer_class=MainPagePromoForCategorySerializer

class ShoppingDayForBrandCarouselView(viewsets.ModelViewSet):
    queryset=ShoppingDayForBrandCarousel.objects.all()
    serializer_class=ShoppingDayForBrandCarouselSerializer

class MainPagePromoForBrandView(viewsets.ModelViewSet):
    queryset=MainPagePromoForBrand.objects.all()
    serializer_class=MainPagePromoForBrandSerializer

class AllcategoriesView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset,many=True)
        allcategories=[]
        for category in serializer.data:
            advertisements=AdvertisingForCategoryMenu.objects.filter(category=category['id'])
            alladvertisements=[]
            for advertisement in advertisements:
                d={
                    'id':advertisement.id,
                    'name':str(advertisement.name),
                    'image':str(advertisement.imageURL),
                    'category':str(advertisement.category),
                    'subcategory':str(advertisement.subcategory),
                    'subsubcategory':str(advertisement.subsubcategory),
                    'brand':str(advertisement.brand)
                }
                alladvertisements.append(d)

            subcategories=Subcategory.objects.filter(category=category['id'])
            allsubcategories=[]
            for subcategory in subcategories:
                allsubsubcategories=[]
                subsubcategories=Subsubcategory.objects.filter(subcategory=subcategory.id)
                for subsubcategory in subsubcategories:
                    d={
                    'id':subsubcategory.id,
                    'subsubcategoryname':subsubcategory.subsubcategoryname,
                    "description": subsubcategory.description,
                    }
                    allsubsubcategories.append(d)
                d={
                    'id':subcategory.id,
                    "subcategoryname": subcategory.subcategoryname,
                    "description": subcategory.description,
                    "subsubcategories": allsubsubcategories,
                }
                allsubcategories.append(d)

            d={
                'id':category['id'],
                'categoryname': category['categoryname'],
                'description':category['description'],
                'image':category['image'],
                'subcategories':allsubcategories,
                'alladvertisements': alladvertisements
                
             
            }

            allcategories.append(d)
        return Response({'data':allcategories})


class ShoppingDayForHomePageCarouselProductsView(viewsets.ModelViewSet):
    queryset=Product.objects.filter(shoppingday=True)
    serializer_class=ProductSerializer
    def list(self, request, *args, **kwargs):
        return Response({'data':[]})

    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        shopdayhomes=ShoppingDayForHomePageCarousel.objects.filter(id=id)
        product = self.queryset.order_by('-buy_quantity')
        allproducts=[]
        for shopdayhome in shopdayhomes:
            if len(shopdayhome.category.all())!=0:
                l=list(shopdayhome.category.all().values_list('id', flat=True))
                product = product.filter(category__in=l)

            if len(shopdayhome.subcategory.all())!=0:
                l=list(shopdayhome.subcategory.all().values_list('id', flat=True))
                product = product.filter(subcategory__in=l)
              
            if len(shopdayhome.subsubcategory.all())!=0:
                l=list(shopdayhome.subsubcategory.all().values_list('id', flat=True))
                product = product.filter(subsubcategory__in=l)
                
                
            if len(shopdayhome.brand.all())!=0:
                l=list(shopdayhome.brand.all().values_list('id', flat=True))
                product = product.filter(brand__in=l)
                
            
            serializer=self.get_serializer(product,many=True)
            for products in serializer.data:
                product=Product.objects.get(id=products['id'])
                productcolor=ProductColor.objects.filter(product=product)
                color=[]
                for i in productcolor:
                    productimage=ProductImageFile.objects.filter(productscolor=i.id)
                    img=[]
                    for j in productimage:
                        d={
                        'id':j.id,
                        'image':j.imageURL,
                        }
                        img.append(d)
                    d={
                        'id':i.id,
                        'productid':i.product.id,
                        'color':i.colorname,
                        'allquantity':i.allquantity,
                        'price':i.price,
                        'oldprice':i.oldprice,
                        'discount':i.product_discount,
                        'image':img
                    }
                    color.append(d)
                category=product.category
                if category is None: categoryname=''
                else: categoryname=category.categoryname
                subcategory=product.subcategory
                if subcategory is None:subcategoryname=''
                else: subcategoryname=subcategory.subcategoryname
                subsubcategory=product.subsubcategory
                if subsubcategory is None: subsubcategoryname=''
                else:subsubcategoryname=subsubcategory.subsubcategoryname
                if product.brand is None: 
                    brand=''
                    brandimageurl=''
                else: 
                    brand=product.brand
                    brandimageurl=product.brand.imageURL

                d={
                    'id':product.id,
                    'categoryname': f'''{categoryname}''',
                    'subcategoryname': f'''{subcategoryname}''',
                    'subsubcategory': f'''{subsubcategoryname}''',
                    'brand':f'''{brand}''',
                    'brandimage':f'''{brandimageurl}''',
                    'productname': f'''{product.productname}''',
                    'buy_quantity': f'''{product.buy_quantity}''',
                    'delivery': f'''{product.delivery}''',
                    'sellingcompany': f'''{product.sellingcompany}''',
                    'imagealt': f'''{product.imagealt}''',
                    'addproductUrl': f'''{product.addproductUrl}''',
                    'shoppingday':product.shoppingday,
                    'product_status':product.product_status,
                    'colors':color,
                    
                }

                allproducts.append(d)
        return Response({'data':allproducts})


class MainPagePromoForHomePageProductsView(viewsets.ModelViewSet):
    queryset=Product.objects.filter(shoppingday=True)
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        shopdayhomes=MainPagePromoForHomePage.objects.filter(id=id)
        product = self.queryset.order_by('-buy_quantity')
        allproducts=[]
        for shopdayhome in shopdayhomes:
            if len(shopdayhome.category.all())!=0:
                l=list(shopdayhome.category.all().values_list('id', flat=True))
                product = product.filter(category__in=l)

            if len(shopdayhome.subcategory.all())!=0:
                l=list(shopdayhome.subcategory.all().values_list('id', flat=True))
                product = product.filter(subcategory__in=l)

            if len(shopdayhome.subsubcategory.all())!=0:
                l=list(shopdayhome.subsubcategory.all().values_list('id', flat=True))
                product = product.filter(subsubcategory__in=l)
                
            product = product.filter(brand=shopdayhome.brand.id)    
            serializer=self.get_serializer(product,many=True)
            for products in serializer.data:
                product=Product.objects.get(id=products['id'])
                productcolor=ProductColor.objects.filter(product=product)
                color=[]
                for i in productcolor:
                    productimage=ProductImageFile.objects.filter(productscolor=i.id)
                    img=[]
                    for j in productimage:
                        d={
                        'id':j.id,
                        'image':j.imageURL,
                        }
                        img.append(d)
                    d={
                        'id':i.id,
                        'productid':i.product.id,
                        'color':i.colorname,
                        'allquantity':i.allquantity,
                        'price':i.price,
                        'oldprice':i.oldprice,
                        'discount':i.product_discount,
                        'image':img
                    }
                    color.append(d)

                category=product.category
                if category is None: categoryname=''
                else: categoryname=category.categoryname
                subcategory=product.subcategory
                if subcategory is None:subcategoryname=''
                else: subcategoryname=subcategory.subcategoryname
                subsubcategory=product.subsubcategory
                if subsubcategory is None: subsubcategoryname=''
                else:subsubcategoryname=subsubcategory.subsubcategoryname
                if product.brand is None: 
                    brand=''
                    brandimageurl=''
                else: 
                    brand=product.brand
                    brandimageurl=product.brand.imageURL

                d={
                    'id':product.id,
                    'categoryname': f'''{categoryname}''',
                    'subcategoryname': f'''{subcategoryname}''',
                    'subsubcategory': f'''{subsubcategoryname}''',
                    'brand':f'''{brand}''',
                    'brandimage':f'''{brandimageurl}''',
                    'productname': f'''{product.productname}''',
                    'buy_quantity': f'''{product.buy_quantity}''',
                    'delivery': f'''{product.delivery}''',
                    'sellingcompany': f'''{product.sellingcompany}''',
                    'imagealt': f'''{product.imagealt}''',
                    'addproductUrl': f'''{product.addproductUrl}''',
                    'shoppingday':product.shoppingday,
                    'product_status':product.product_status,
                    'colors':color,  
                }

                allproducts.append(d)
        return Response({'data':allproducts})


class MainPagePromoForHomePageSliderProductsView(viewsets.ModelViewSet):
    queryset=Product.objects.filter(shoppingday=True)
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        shopdayhomes=MainPagePromoForHomePageSlider.objects.filter(id=id)
        product = self.queryset.order_by('-buy_quantity')
        allproducts=[]
        for shopdayhome in shopdayhomes:
            if len(shopdayhome.category.all())!=0:
                l=list(shopdayhome.category.all().values_list('id', flat=True))
                product = product.filter(category__in=l)

            if len(shopdayhome.subcategory.all())!=0:
                l=list(shopdayhome.subcategory.all().values_list('id', flat=True))
                product = product.filter(subcategory__in=l)
                
            if len(shopdayhome.subsubcategory.all())!=0:
                l=list(shopdayhome.subsubcategory.all().values_list('id', flat=True))
                product = product.filter(subsubcategory__in=l)
                
           
            
            product = product.filter(brand=shopdayhome.brand.id)
            serializer=self.get_serializer(product,many=True)
            for products in serializer.data:
                product=Product.objects.get(id=products['id'])
                productcolor=ProductColor.objects.filter(product=product)
                color=[]
                for i in productcolor:
                    productimage=ProductImageFile.objects.filter(productscolor=i.id)
                    img=[]
                    for j in productimage:
                        d={
                        'id':j.id,
                        'image':j.imageURL,
                        }
                        img.append(d)
                    d={
                        'id':i.id,
                        'productid':i.product.id,
                        'color':i.colorname,
                        'allquantity':i.allquantity,
                        'price':i.price,
                        'oldprice':i.oldprice,
                        'discount':i.product_discount,
                        'image':img
                    }
                    color.append(d)

                category=product.category
                if category is None: categoryname=''
                else: categoryname=category.categoryname
                subcategory=product.subcategory
                if subcategory is None:subcategoryname=''
                else: subcategoryname=subcategory.subcategoryname
                subsubcategory=product.subsubcategory
                if subsubcategory is None: subsubcategoryname=''
                else:subsubcategoryname=subsubcategory.subsubcategoryname
                if product.brand is None: 
                    brand=''
                    brandimageurl=''
                else: 
                    brand=product.brand
                    brandimageurl=product.brand.imageURL

                d={
                    'id':product.id,
                    'categoryname': f'''{categoryname}''',
                    'subcategoryname': f'''{subcategoryname}''',
                    'subsubcategory': f'''{subsubcategoryname}''',
                    'brand':f'''{brand}''',
                    'brandimage':f'''{brandimageurl}''',
                    'productname': f'''{product.productname}''',
                    'buy_quantity': f'''{product.buy_quantity}''',
                    'delivery': f'''{product.delivery}''',
                    'sellingcompany': f'''{product.sellingcompany}''',
                    'imagealt': f'''{product.imagealt}''',
                    'addproductUrl': f'''{product.addproductUrl}''',
                    'shoppingday':product.shoppingday,
                    'product_status':product.product_status,
                    'colors':color,
                    
                }

                allproducts.append(d)
        return Response({'data':allproducts})
        return Response({'data':"data"})


class AdvertisingForCategoryMenuProductsView(viewsets.ModelViewSet):
    queryset=Product.objects.filter(shoppingday=True)
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        shopdayhomes=AdvertisingForCategoryMenu.objects.filter(id=id)
        product = self.queryset.order_by('-buy_quantity')
        allproducts=[]
        for shopdayhome in shopdayhomes:
            product = product.filter(category=shopdayhome.category.id)

            if len(shopdayhome.subcategory.all())!=0:
                l=list(shopdayhome.subcategory.all().values_list('id', flat=True))
                product = product.filter(subcategory__in=l)
                print("subcategory")
            if len(shopdayhome.subsubcategory.all())!=0:
                l=list(shopdayhome.subsubcategory.all().values_list('id', flat=True))
                product = product.filter(subsubcategory__in=l)
                print("subsubcategory")
                
            if len(shopdayhome.brand.all())!=0:
                l=list(shopdayhome.brand.all().values_list('id', flat=True))
                product = product.filter(brand__in=l)
                print("brand")
            
            serializer=self.get_serializer(product,many=True)
            for products in serializer.data:
                product=Product.objects.get(id=products['id'])
                productcolor=ProductColor.objects.filter(product=product)
                color=[]
                for i in productcolor:
                    productimage=ProductImageFile.objects.filter(productscolor=i.id)
                    img=[]
                    for j in productimage:
                        d={
                        'id':j.id,
                        'image':j.imageURL,
                        }
                        img.append(d)
                    d={
                        'id':i.id,
                        'productid':i.product.id,
                        'color':i.colorname,
                        'allquantity':i.allquantity,
                        'price':i.price,
                        'oldprice':i.oldprice,
                        'discount':i.product_discount,
                        'image':img
                    }
                    color.append(d)

                category=product.category
                if category is None: categoryname=''
                else: categoryname=category.categoryname
                subcategory=product.subcategory
                if subcategory is None:subcategoryname=''
                else: subcategoryname=subcategory.subcategoryname
                subsubcategory=product.subsubcategory
                if subsubcategory is None: subsubcategoryname=''
                else:subsubcategoryname=subsubcategory.subsubcategoryname
                if product.brand is None: 
                    brand=''
                    brandimageurl=''
                else: 
                    brand=product.brand
                    brandimageurl=product.brand.imageURL

                d={
                    'id':product.id,
                    'categoryname': f'''{categoryname}''',
                    'subcategoryname': f'''{subcategoryname}''',
                    'subsubcategory': f'''{subsubcategoryname}''',
                    'brand':f'''{brand}''',
                    'brandimage':f'''{brandimageurl}''',
                    'productname': f'''{product.productname}''',
                    'buy_quantity': f'''{product.buy_quantity}''',
                    'delivery': f'''{product.delivery}''',
                    'sellingcompany': f'''{product.sellingcompany}''',
                    'imagealt': f'''{product.imagealt}''',
                    'addproductUrl': f'''{product.addproductUrl}''',
                    'shoppingday':product.shoppingday,
                    'product_status':product.product_status,
                    'colors':color,
                    
                }

                allproducts.append(d)
        return Response({'data':allproducts})


class ShoppingDayForCategoryCarouselProductsView(viewsets.ModelViewSet):
    queryset=Product.objects.filter(shoppingday=True)
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        shopdayhomes=ShoppingDayForCategoryCarousel.objects.filter(id=id)
        product = self.queryset.order_by('-buy_quantity')
        allproducts=[]
        for shopdayhome in shopdayhomes:
            product = product.filter(category=shopdayhome.category.id)
            if len(shopdayhome.subcategory.all())!=0:
                l=list(shopdayhome.subcategory.all().values_list('id', flat=True))
                product = product.filter(subcategory__in=l)
                print("subcategory")
            if len(shopdayhome.subsubcategory.all())!=0:
                l=list(shopdayhome.subsubcategory.all().values_list('id', flat=True))
                product = product.filter(subsubcategory__in=l)
                print("subsubcategory")
                
            if len(shopdayhome.brand.all())!=0:
                l=list(shopdayhome.brand.all().values_list('id', flat=True))
                product = product.filter(brand__in=l)
                print("brand")
            
            serializer=self.get_serializer(product,many=True)
            for products in serializer.data:
                product=Product.objects.get(id=products['id'])
                productcolor=ProductColor.objects.filter(product=product)
                color=[]
                for i in productcolor:
                    productimage=ProductImageFile.objects.filter(productscolor=i.id)
                    img=[]
                    for j in productimage:
                        d={
                        'id':j.id,
                        'image':j.imageURL,
                        }
                        img.append(d)
                    d={
                        'id':i.id,
                        'productid':i.product.id,
                        'color':i.colorname,
                        'allquantity':i.allquantity,
                        'price':i.price,
                        'oldprice':i.oldprice,
                        'discount':i.product_discount,
                        'image':img
                    }
                    color.append(d)

                category=product.category
                if category is None: categoryname=''
                else: categoryname=category.categoryname
                subcategory=product.subcategory
                if subcategory is None:subcategoryname=''
                else: subcategoryname=subcategory.subcategoryname
                subsubcategory=product.subsubcategory
                if subsubcategory is None: subsubcategoryname=''
                else:subsubcategoryname=subsubcategory.subsubcategoryname
                if product.brand is None: 
                    brand=''
                    brandimageurl=''
                else: 
                    brand=product.brand
                    brandimageurl=product.brand.imageURL

                d={
                    'id':product.id,
                    'categoryname': f'''{categoryname}''',
                    'subcategoryname': f'''{subcategoryname}''',
                    'subsubcategory': f'''{subsubcategoryname}''',
                    'brand':f'''{brand}''',
                    'brandimage':f'''{brandimageurl}''',
                    'productname': f'''{product.productname}''',
                    'buy_quantity': f'''{product.buy_quantity}''',
                    'delivery': f'''{product.delivery}''',
                    'sellingcompany': f'''{product.sellingcompany}''',
                    'imagealt': f'''{product.imagealt}''',
                    'addproductUrl': f'''{product.addproductUrl}''',
                    'shoppingday':product.shoppingday,
                    'product_status':product.product_status,
                    'colors':color,
                    
                }

                allproducts.append(d)
        return Response({'data':allproducts})


class MainPagePromoForCategoryProductsView(viewsets.ModelViewSet):
    queryset=Product.objects.filter(shoppingday=True)
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        shopdayhomes=MainPagePromoForCategory.objects.filter(id=id)
        product = self.queryset.order_by('-buy_quantity')
        allproducts=[]
        for shopdayhome in shopdayhomes:
            product = product.filter(category=shopdayhome.category)
            if len(shopdayhome.subcategory.all())!=0:
                l=list(shopdayhome.subcategory.all().values_list('id', flat=True))
                product = product.filter(subcategory__in=l)
                print("subcategory")
            if len(shopdayhome.subsubcategory.all())!=0:
                l=list(shopdayhome.subsubcategory.all().values_list('id', flat=True))
                product = product.filter(subsubcategory__in=l)
                print("subsubcategory")
                
            if len(shopdayhome.brand.all())!=0:
                l=list(shopdayhome.brand.all().values_list('id', flat=True))
                product = product.filter(brand__in=l)
                print("brand")
            
            serializer=self.get_serializer(product,many=True)
            for products in serializer.data:
                product=Product.objects.get(id=products['id'])
                productcolor=ProductColor.objects.filter(product=product)
                color=[]
                for i in productcolor:
                    productimage=ProductImageFile.objects.filter(productscolor=i.id)
                    img=[]
                    for j in productimage:
                        d={
                        'id':j.id,
                        'image':j.imageURL,
                        }
                        img.append(d)
                    d={
                        'id':i.id,
                        'productid':i.product.id,
                        'color':i.colorname,
                        'allquantity':i.allquantity,
                        'price':i.price,
                        'oldprice':i.oldprice,
                        'discount':i.product_discount,
                        'image':img
                    }
                    color.append(d)

                category=product.category
                if category is None: categoryname=''
                else: categoryname=category.categoryname
                subcategory=product.subcategory
                if subcategory is None:subcategoryname=''
                else: subcategoryname=subcategory.subcategoryname
                subsubcategory=product.subsubcategory
                if subsubcategory is None: subsubcategoryname=''
                else:subsubcategoryname=subsubcategory.subsubcategoryname
                if product.brand is None: 
                    brand=''
                    brandimageurl=''
                else: 
                    brand=product.brand
                    brandimageurl=product.brand.imageURL

                d={
                    'id':product.id,
                    'categoryname': f'''{categoryname}''',
                    'subcategoryname': f'''{subcategoryname}''',
                    'subsubcategory': f'''{subsubcategoryname}''',
                    'brand':f'''{brand}''',
                    'brandimage':f'''{brandimageurl}''',
                    'productname': f'''{product.productname}''',
                    'buy_quantity': f'''{product.buy_quantity}''',
                    'delivery': f'''{product.delivery}''',
                    'sellingcompany': f'''{product.sellingcompany}''',
                    'imagealt': f'''{product.imagealt}''',
                    'addproductUrl': f'''{product.addproductUrl}''',
                    'shoppingday':product.shoppingday,
                    'product_status':product.product_status,
                    'colors':color,
                    
                }

                allproducts.append(d)
        return Response({'data':allproducts})


class ShoppingDayForBrandCarouselProductsView(viewsets.ModelViewSet):
    queryset=Product.objects.filter(shoppingday=True)
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        shopdayhomes=ShoppingDayForBrandCarousel.objects.filter(id=id)
        product = self.queryset.order_by('-buy_quantity')
        allproducts=[]
        for shopdayhome in shopdayhomes:
            if len(shopdayhome.category.all())!=0:
                l=list(shopdayhome.category.all().values_list('id', flat=True))
                product = product.filter(category__in=l)

            if len(shopdayhome.subcategory.all())!=0:
                l=list(shopdayhome.subcategory.all().values_list('id', flat=True))
                product = product.filter(subcategory__in=l)
                
            if len(shopdayhome.subsubcategory.all())!=0:
                l=list(shopdayhome.subsubcategory.all().values_list('id', flat=True))
                product = product.filter(subsubcategory__in=l)
                
            product = product.filter(brand=shopdayhome.brand.id)  
            serializer=self.get_serializer(product,many=True)
            for products in serializer.data:
                product=Product.objects.get(id=products['id'])
                productcolor=ProductColor.objects.filter(product=product)
                color=[]
                for i in productcolor:
                    productimage=ProductImageFile.objects.filter(productscolor=i.id)
                    img=[]
                    for j in productimage:
                        d={
                        'id':j.id,
                        'image':j.imageURL,
                        }
                        img.append(d)
                    d={
                        'id':i.id,
                        'productid':i.product.id,
                        'color':i.colorname,
                        'allquantity':i.allquantity,
                        'price':i.price,
                        'oldprice':i.oldprice,
                        'discount':i.product_discount,
                        'image':img
                    }
                    color.append(d)

                category=product.category
                if category is None: categoryname=''
                else: categoryname=category.categoryname
                subcategory=product.subcategory
                if subcategory is None:subcategoryname=''
                else: subcategoryname=subcategory.subcategoryname
                subsubcategory=product.subsubcategory
                if subsubcategory is None: subsubcategoryname=''
                else:subsubcategoryname=subsubcategory.subsubcategoryname
                if product.brand is None: 
                    brand=''
                    brandimageurl=''
                else: 
                    brand=product.brand
                    brandimageurl=product.brand.imageURL

                d={
                    'id':product.id,
                    'categoryname': f'''{categoryname}''',
                    'subcategoryname': f'''{subcategoryname}''',
                    'subsubcategory': f'''{subsubcategoryname}''',
                    'brand':f'''{brand}''',
                    'brandimage':f'''{brandimageurl}''',
                    'productname': f'''{product.productname}''',
                    'buy_quantity': f'''{product.buy_quantity}''',
                    'delivery': f'''{product.delivery}''',
                    'sellingcompany': f'''{product.sellingcompany}''',
                    'imagealt': f'''{product.imagealt}''',
                    'addproductUrl': f'''{product.addproductUrl}''',
                    'shoppingday':product.shoppingday,
                    'product_status':product.product_status,
                    'colors':color,
                    
                }

                allproducts.append(d)
        return Response({'data':allproducts})


class MainPagePromoForBrandProductsView(viewsets.ModelViewSet):
    queryset=Product.objects.filter(shoppingday=True)
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        shopdayhomes=MainPagePromoForBrand.objects.filter(id=id)
        product = self.queryset.order_by('-buy_quantity')
        allproducts=[]
        for shopdayhome in shopdayhomes:  
            if len(shopdayhome.category.all())!=0:
                l=list(shopdayhome.category.all().values_list('id', flat=True))
                product = product.filter(category__in=l)

            if len(shopdayhome.subcategory.all())!=0:
                l=list(shopdayhome.subcategory.all().values_list('id', flat=True))
                product = product.filter(subcategory__in=l)
                
            if len(shopdayhome.subsubcategory.all())!=0:
                l=list(shopdayhome.subsubcategory.all().values_list('id', flat=True))
                product = product.filter(subsubcategory__in=l)
                
            product = product.filter(brand=shopdayhome.brand.id)
            serializer=self.get_serializer(product,many=True)
            for products in serializer.data:
                product=Product.objects.get(id=products['id'])
                productcolor=ProductColor.objects.filter(product=product)
                color=[]
                for i in productcolor:
                    productimage=ProductImageFile.objects.filter(productscolor=i.id)
                    img=[]
                    for j in productimage:
                        d={
                        'id':j.id,
                        'image':j.imageURL,
                        }
                        img.append(d)
                    d={
                        'id':i.id,
                        'productid':i.product.id,
                        'color':i.colorname,
                        'allquantity':i.allquantity,
                        'price':i.price,
                        'oldprice':i.oldprice,
                        'discount':i.product_discount,
                        'image':img
                    }
                    color.append(d)

                category=product.category
                if category is None: categoryname=''
                else: categoryname=category.categoryname
                subcategory=product.subcategory
                if subcategory is None:subcategoryname=''
                else: subcategoryname=subcategory.subcategoryname
                subsubcategory=product.subsubcategory
                if subsubcategory is None: subsubcategoryname=''
                else:subsubcategoryname=subsubcategory.subsubcategoryname
                if product.brand is None: 
                    brand=''
                    brandimageurl=''
                else: 
                    brand=product.brand
                    brandimageurl=product.brand.imageURL

                d={
                    'id':product.id,
                    'categoryname': f'''{categoryname}''',
                    'subcategoryname': f'''{subcategoryname}''',
                    'subsubcategory': f'''{subsubcategoryname}''',
                    'brand':f'''{brand}''',
                    'brandimage':f'''{brandimageurl}''',
                    'productname': f'''{product.productname}''',
                    'buy_quantity': f'''{product.buy_quantity}''',
                    'delivery': f'''{product.delivery}''',
                    'sellingcompany': f'''{product.sellingcompany}''',
                    'imagealt': f'''{product.imagealt}''',
                    'addproductUrl': f'''{product.addproductUrl}''',
                    'shoppingday':product.shoppingday,
                    'product_status':product.product_status,
                    'colors':color,
                    
                }

                allproducts.append(d)
        return Response({'data':allproducts})



class SearchProductsView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer


    def retrieve(self, request, *args, **kwargs):
        print(kwargs['pk'])
        product=self.queryset.filter(Q(productname__contains=kwargs['pk']) | Q(imagealt__contains=kwargs['pk']))
        serializer = self.get_serializer(product,many=True)
        searchproducts=[]
        for products in serializer.data:
            product=Product.objects.get(id=products['id'])
            productcolor=ProductColor.objects.filter(product=product)
            color=[]
            for i in productcolor:
                productimage=ProductImageFile.objects.filter(productscolor=i.id)
                img=[]
                for j in productimage:
                    d={
                    'id':j.id,
                    'image':j.imageURL,
                    }
                    img.append(d)
                d={
                    'id':i.id,
                    'productid':i.product.id,
                    'color':i.colorname,
                    'allquantity':i.allquantity,
                    'price':i.price,
                    'oldprice':i.oldprice,
                    'discount':i.product_discount,
                    'image':img
                }
                color.append(d)

            category=product.category
            if category is None: categoryname=''
            else: categoryname=category.categoryname
            subcategory=product.subcategory
            if subcategory is None:subcategoryname=''
            else: subcategoryname=subcategory.subcategoryname
            subsubcategory=product.subsubcategory
            if subsubcategory is None: subsubcategoryname=''
            else:subsubcategoryname=subsubcategory.subsubcategoryname
            if product.brand is None: 
                brand=''
                brandimageurl=''
            else: 
                brand=product.brand
                brandimageurl=product.brand.imageURL

            d={
                'id':product.id,
                'categoryname': f'''{categoryname}''',
                'subcategoryname': f'''{subcategoryname}''',
                'subsubcategory': f'''{subsubcategoryname}''',
                'brand':f'''{brand}''',
                'brandimage':f'''{brandimageurl}''',
                'productname': f'''{product.productname}''',
                'buy_quantity': f'''{product.buy_quantity}''',
                'delivery': f'''{product.delivery}''',
                'sellingcompany': f'''{product.sellingcompany}''',
                'imagealt': f'''{product.imagealt}''',
                'addproductUrl': f'''{product.addproductUrl}''',
                'shoppingday':product.shoppingday,
                'product_status':product.product_status,
                'colors':color,
            }

            searchproducts.append(d)
        return Response({'data':searchproducts})
















