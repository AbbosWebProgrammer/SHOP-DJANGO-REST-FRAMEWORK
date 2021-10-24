from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from django.template import loader
from datetime import  date
from rest_framework.response import Response
from .serializer import * 
from rest_framework import viewsets
import json
from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response

class CategoryView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class SubcategoryView(viewsets.ModelViewSet):
    queryset=Subcategory.objects.all()
    serializer_class=SubcategorySerializer
class BrandView(viewsets.ModelViewSet):
    queryset=Brand.objects.all()
    serializer_class=BrandSerializer

class ProductsView(viewsets.ModelViewSet):
    queryset=Products.objects.all()
    serializer_class=ProductsSerializer
#     def retrieve(self, request, *args, **kwargs):
#         id= kwargs['pk']
#         product = self.queryset.filter(id=id)
#         productserializer = self.get_serializer(product,many=True)
#         productdate = productserializer.data 
#         data = []        
#         data.append({"product":productdate})
#         image=Imagefiles.objects.filter(product=productdate[0]["id"])
#         imagesserializer = ImagefilesSerializer(image,many=True)
#         imagesdate= imagesserializer.data
#         data.append({"images":imagesdate})    
#         return Response(data)


class DescproductView(viewsets.ModelViewSet):
    queryset=Descproduct.objects.all()
    serializer_class=DescproductSerializer

class ProductColorView(viewsets.ModelViewSet):
    queryset=ProductsColor.objects.all()
    serializer_class=ProductColorSerializer

class ImagefilesView(viewsets.ModelViewSet):
    queryset=Imagefiles.objects.all()
    serializer_class=ImagefilesSerializer

class ProductSizeView(viewsets.ModelViewSet):
    queryset=ProductSize.objects.all()
    serializer_class=ProductSizeSerializer
class ProductParamsCaptionView(viewsets.ModelViewSet):
    queryset=ProductParamsCaption.objects.all()
    serializer_class=ProductParamsCaptionSerializer
class ProductParamsCaptionitemsView(viewsets.ModelViewSet):
    queryset=ProductParamsCaptionitems.objects.all()
    serializer_class=ProductParamsCaptionitemsSerializer
    
class SubcategoryByCategoryIdView(viewsets.ModelViewSet):
    queryset=Subcategory.objects.all()
    serializer_class=SubcategorySerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.queryset.filter(category=id)
        serializer = self.get_serializer(data,many=True)
        return Response(serializer.data)
class ProductsBySubcategoryIdView(viewsets.ModelViewSet):
    queryset=Products.objects.all()
    serializer_class=ProductsSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.queryset.filter(subcategory=id)
        serializer = self.get_serializer(data,many=True)
        return Response(serializer.data)

class ProductsColorByProductIdView(viewsets.ModelViewSet):
    queryset=ProductsColor.objects.all()
    serializer_class=ProductColorSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(product=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)
class ImagefilesByProductsColorIdView(viewsets.ModelViewSet):
    queryset=Imagefiles.objects.all()
    serializer_class=ImagefilesSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(product=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)

class ProductsizeByProductsColorIdView(viewsets.ModelViewSet):
    queryset=ProductSize.objects.all()
    serializer_class=ProductSizeSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(product=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)

class DescProductsByProductIdView(viewsets.ModelViewSet):
    queryset=Descproduct.objects.all()
    serializer_class=DescproductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(product=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)

class ProductParamsCaptionByProductIdView(viewsets.ModelViewSet):
    queryset=ProductParamsCaption.objects.all()
    serializer_class=ProductParamsCaptionSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(product=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)

class ProductParamsCaptionitemsByProductParamsCaptionIdView(viewsets.ModelViewSet):
    queryset=ProductParamsCaptionitems.objects.all()
    serializer_class=ProductParamsCaptionitemsSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(productparamscaption=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)




class DateForProductPageByIdView(viewsets.ModelViewSet):
    queryset=Products.objects.all()
    serializer_class=ProductsSerializer



class ProductscreateView(viewsets.ModelViewSet):
    queryset = ProductsColor.objects.all()
    serializer_class = CreateProductsSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            print(data)
            product = Products.objects.create(
                subcategory=data['user']['subcategory'],
                name=data['user']['name'],
                price=data['user']['price'],
                discounts=data['user']['discounts'],
                oldprice=data['user']['oldprice'],
                delivery=data['user']['delivery'],
            )
            product.save()
            productcolor = ProductsColor.objects.create(
                productcolor=product,
                colorname = data['colorname'],
            )
            productcolor.save()
            return Response({'status':'created'},status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     def update(self, request, *args, **kwargs):
#         print('update..')
#         id = kwargs['pk']
#         emp = self.queryset.get(id=id)
#         user = emp.user
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             data = serializer.validated_data
#             print(data)
#             if data['user']['first_name']:
#                 user.first_name = data['user']['first_name']
#             if data['user']['last_name']:
#                 user.last_name = data['user']['last_name']
#             if data['user']['username']:
#                 user.username = data['user']['username']
#             if data['user']['password']:
#                 user.password = data['user']['password']
#             if data['user']['email']:
#                 user.email = data['user']['email']
#             user.save()
#             if data['phone']:
#                 emp.phone = data['phone']
#             if data['image']:
#                 emp.image = data['image']
#             if data['address']:
#                 emp.address = data['address']
#             if data['territorie']:
#                 t = data['territorie']
#                 print(t)
#                 emp.territorie.clear()
#                 for i in t:
#                     emp.territorie.add(i)
#             emp.save()
#         return Response({'status':'OK'})






#     # def retrieve(self, request, *args, **kwargs):
#     #     id= kwargs['pk']
#     #     product = self.queryset.filter(id=id)
#     #     productserializer = self.get_serializer(product,many=True)
#     #     productdate = productserializer.data 

#         # data = []        
#         # data.append({"product":productdate})
#         # image=Imagefiles.objects.filter(product=productdate[0]["id"])
#         # imagesserializer = ImagefilesSerializer(image,many=True)
#         # imagesdate= imagesserializer.data
#         # data.append({"images":imagesdate})
#         # strukture=Strukture.objects.filter(product=productdate[0]["id"])
#         # struktureserializer = StruktureSerializer(strukture,many=True)
#         # struktures= struktureserializer.data
#         # data.append({"struktures":struktures})
#         # comment=Comment.objects.filter(product=productdate[0]["id"])
#         # commentserializer = CommentSerializer(comment,many=True)
#         # commentdate= commentserializer.data 
#         # data.append({"comments":commentdate})

#         # resivercomment=ResiverComment.objects.filter(resiver=commentdate[0]["id"])
#         # resivercommentserializer = ResiverCommentSerializer(resivercomment,many=True)
#         # resivercomment= resivercommentserializer.data
#         # data.append({"resivercomments":resivercomment})
        
#         # return Response(data)
 

          
# # class SearchInNewsView(viewsets.ModelViewSet):
# #     queryset=News.objects.all()
# #     serializer_class=NewsSerializer
# #     def retrieve(self, request, *args, **kwargs):
# #         name=kwargs['pk']
# #         print(name)
# #         news=self.queryset.filter(news_name__contains=name)
# #         serializer = self.get_serializer(news,many=True)
# #         return Response(serializer.data)
