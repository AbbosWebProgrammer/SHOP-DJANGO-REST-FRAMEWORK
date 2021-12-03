from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import * 
from .models import *
import io, base64
import uuid

class CategoryView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    def update(self, request, *args, **kwargs):
        category=Category.objects.get(id=kwargs['pk'])
        if  request.data["categoryname"]!='' and request.data["categoryname"]!=category.categoryname:
            category.categoryname=request.data["categoryname"]
        if  request.data["description"]!='' and request.data["description"]!=category.description:
            category.description=request.data["description"]
        if request.data["image"]:
            category.image=request.data['image']
        category.save()


class SubcategoryView(viewsets.ModelViewSet):
    queryset=Subcategory.objects.all()
    serializer_class=SubcategorySerializer
    def update(self, request, *args, **kwargs):
        subcategory=Subcategory.objects.get(id=kwargs['pk'])
        if  request.data["category"]!='' and request.data["category"]!=subcategory.category:
            subcategory.category=request.data["category"]
        if  request.data["subcategoryname"]!='' and request.data["subcategoryname"]!=subcategory.subcategoryname:
            subcategory.subcategoryname=request.data["subcategoryname"]
        if  request.data["description"]!='' and request.data["description"]!=subcategory.description:
            subcategory.description=request.data["description"]
        subcategory.save()


class SubsubcategoryView(viewsets.ModelViewSet):
    queryset=Subsubcategory.objects.all()
    serializer_class=SubsubcategorySerializer
    def update(self, request, *args, **kwargs):
        subsubcategory=Subsubcategory.objects.get(id=kwargs['pk'])
        if  request.data["category"]!='' and request.data["category"]!=subsubcategory.category:
            subsubcategory.category=request.data["category"]
        if  request.data["subcategory"]!='' and request.data["subcategory"]!=subsubcategory.subcategory:
            subsubcategory.subcategory=request.data["subcategory"]
        if  request.data["subsubcategoryname"]!='' and request.data["subsubcategoryname"]!=subsubcategory.subsubcategoryname:
            subsubcategory.subsubcategoryname=request.data["subsubcategoryname"]
        if  request.data["description"]!='' and request.data["description"]!=subsubcategory.description:
            subsubcategory.description=request.data["description"]
        subsubcategory.save()
        return Response({'status':'OK'})


class BrandView(viewsets.ModelViewSet):
    queryset=Brand.objects.all()
    serializer_class=BrandSerializer
    def update(self, request, *args, **kwargs):
        brand=Brand.objects.get(id=kwargs['pk'])
        if  request.data["name"]!='' and request.data["name"]!=brand.name:
            brand.name=request.data["name"]
        if  request.data["description"]!='' and request.data["description"]!=brand.description:
            brand.description=request.data["description"]
        if request.data["image"]:
            brand.image=request.data['image']
        brand.save()
        return Response({'status':'OK'})


class ProductView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer


class DescriptionForProductView(viewsets.ModelViewSet):
    queryset=DescriptionForProduct.objects.all()
    serializer_class=DescriptionForProductSerializer


class ProductColorView(viewsets.ModelViewSet):
    queryset=ProductColor.objects.all()
    serializer_class=ProductColorSerializer


class ProductImageFileView(viewsets.ModelViewSet):
    queryset=ProductImageFile.objects.all()
    serializer_class=ProductImageFileSerializer


class ProductSizeView(viewsets.ModelViewSet):
    queryset=ProductSize.objects.all()
    serializer_class=ProductSizeSerializer


class ProductParamsCaptionView(viewsets.ModelViewSet):
    queryset=ProductParamsCaption.objects.all()
    serializer_class=ProductParamsCaptionSerializer


class ProductParamsCaptionitemsView(viewsets.ModelViewSet):
    queryset=ProductParamsCaptionitem.objects.all()
    serializer_class=ProductParamsCaptionitemSerializer

      
class SubcategoryByCategoryIdView(viewsets.ModelViewSet):
    queryset=Subcategory.objects.all()
    serializer_class=SubcategorySerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.queryset.filter(category=id)
        serializer = self.get_serializer(data,many=True)
        return Response(serializer.data)   


class SubsubcategoryByCategoryIdView(viewsets.ModelViewSet):
    queryset=Subsubcategory.objects.all()
    serializer_class=SubsubcategorySerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.queryset.filter(category=id)
        serializer = self.get_serializer(data,many=True)
        return Response(serializer.data)


class SubsubcategoryBySubcategorIdView(viewsets.ModelViewSet):
    queryset=Subsubcategory.objects.all()
    serializer_class=SubsubcategorySerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.queryset.filter(subcategory=id)
        serializer = self.get_serializer(data,many=True)
        return Response(serializer.data)

# Products get  by category ,subcategory ,subsubcategory
class ProductsByCategoryIdView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.queryset.filter(category=id).order_by('-buy_quantity')
        serializer = self.get_serializer(data,many=True)
        allproducts=[]
        for products in serializer.data:
            product=Product.objects.get(id=products['id'])
            productcolor=ProductColor.objects.filter(product=product)
            image=[]
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
                    'price':i.price,
                    'oldprice':i.oldprice,
                    'discount':i.product_discount,
                    'image':img
                }
                image.append(d)

            d={
                'id':product.id,
                'categoryname': f'''{product.category.categoryname}''',
                'subcategoryname': f'''{product.subcategory.subcategoryname}''',
                'subsubcategory': f'''{product.subsubcategory.subsubcategoryname}''',
                'brand':f'''{product.brand}''',
                'productname': f'''{product.productname}''',
                'buy_quantity': f'''{product.buy_quantity}''',
                'imagealt': f'''{product.imagealt}''',
                'addproductUrl': f'''{product.addproductUrl}''',
                'shoppingday':product.shoppingday,
                'product_status':product.product_status,
                'colors':image, 
            }

            allproducts.append(d)
        return Response({'data':allproducts})


class ProductsBySubcategoryIdView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.queryset.filter(subcategory=id).order_by('-buy_quantity')
        serializer = self.get_serializer(data,many=True)
        allproducts=[]
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
                    'price':i.price,
                    'oldprice':i.oldprice,
                    'discount':i.product_discount,
                    'image':img
                }
                color.append(d)

            d={
                'id':product.id,
                'categoryname': f'''{product.category.categoryname}''',
                'subcategoryname': f'''{product.subcategory.subcategoryname}''',
                'subsubcategory': f'''{product.subsubcategory.subsubcategoryname}''',
                'brand':f'''{product.brand}''',
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


class ProductsBySubsubcategoryIdView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.queryset.filter(subsubcategory=id).order_by('-buy_quantity')
        serializer = self.get_serializer(data,many=True)
        allproducts=[]
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
                    'price':i.price,
                    'oldprice':i.oldprice,
                    'discount':i.product_discount,
                    'image':img
                }
                color.append(d)

            d={
                'id':product.id,
                'categoryname': f'''{product.category.categoryname}''',
                'subcategoryname': f'''{product.subcategory.subcategoryname}''',
                'subsubcategory': f'''{product.subsubcategory.subsubcategoryname}''',
                'brand':f'''{product.brand}''',
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


class ProductsByBrandIdView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = self.queryset.filter(brand=id).order_by('-buy_quantity')
        serializer = self.get_serializer(data,many=True)
        allproducts=[]
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
                    'price':i.price,
                    'oldprice':i.oldprice,
                    'discount':i.product_discount,
                    'image':img
                }
                color.append(d)

            d={
                'id':product.id,
                'categoryname': f'''{product.category.categoryname}''',
                'subcategoryname': f'''{product.subcategory.subcategoryname}''',
                'subsubcategory': f'''{product.subsubcategory.subsubcategoryname}''',
                'brand':f'''{product.brand}''',
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


class ProductsColorByProductIdView(viewsets.ModelViewSet):
    queryset=ProductColor.objects.all()
    serializer_class=ProductColorSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(product=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)


class ImagefilesByProductsColorIdView(viewsets.ModelViewSet):
    queryset=ProductImageFile.objects.all()
    serializer_class=ProductImageFileSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(productscolor=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)


class ProductsizeByProductsColorIdView(viewsets.ModelViewSet):
    queryset=ProductSize.objects.all()
    serializer_class=ProductSizeSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(productscolor=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)


class DescriptionsByProductIdView(viewsets.ModelViewSet):
    queryset=DescriptionForProduct.objects.all()
    serializer_class=DescriptionForProductSerializer
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
    queryset=ProductParamsCaptionitem.objects.all()
    serializer_class=ProductParamsCaptionitemSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(productparamscaption=id)
        serializer = self.get_serializer(products,many=True)
        return Response(serializer.data)


class XitProductSView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def list(self, request, *args, **kwargs):
        products = self.queryset.order_by('-buy_quantity')
        serializer=self.get_serializer(products,many=True)
        xitproducts=[]
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

            d={
                'id':product.id,
                'categoryname': f'''{product.category.categoryname}''',
                'subcategoryname': f'''{product.subcategory.subcategoryname}''',
                'subsubcategory': f'''{product.subsubcategory.subsubcategoryname}''',
                'brand':f'''{product.brand}''',
                'brandimage':f'''{product.brand.imageURL}''',
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

            xitproducts.append(d)
        return Response({'data':xitproducts})


class ProductInfoView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def list(self, request, *args, **kwargs):
        product = self.queryset.order_by('-buy_quantity')
        serializer=self.get_serializer(product,many=True)
        xitproducts=[]
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
                    'price':i.price,
                    'oldprice':i.oldprice,
                    'discount':i.product_discount,
                    'image':img
                }
                color.append(d)

            d={
                'id':product.id,
                'categoryname': f'''{product.category.categoryname}''',
                'subcategoryname': f'''{product.subcategory.subcategoryname}''',
                'subsubcategory': f'''{product.subsubcategory.subsubcategoryname}''',
                'brand':f'''{product.brand}''',
                'brandimage':f'''{product.brand.imageURL}''',
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

            xitproducts.append(d)
        return Response({'data':xitproducts})
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(id=id)
        data=[]
        for product in products:
            des=DescriptionForProduct.objects.filter(product=id)
            desc=[]
            for i in des:
                d={
                        'id':i.id,
                        'name':i.name,
                        'description':i.description
                    }
                desc.append(d)        
            productcolor=ProductColor.objects.filter(product=id)
            color=[]
            for i in productcolor:
                images=ProductImageFile.objects.filter(productscolor=i.id)
                img=[]
                for image in images:
                    d={
                        'id':image.id,
                        'image':image.imageURL,
                    }
                    img.append(d)
                sizes=ProductSize.objects.filter(productscolor=i.id)
                sizess=[]
                for size in sizes:
                    d={
                        'id':size.id,
                        'size':size.size,
                        'quantity':size.quentity,
                    }
                    sizess.append(d)
        
                d={
                    'id':i.id,
                    'id':i.id,
                    'productid':i.product.id,
                    'color':i.colorname,
                    'price':i.price,
                    'oldprice':i.oldprice,
                    'discount':i.product_discount,
                    'image':img,
                    'size':sizess
                }
                color.append(d)

                    
            d={
                'id':product.id,
                'categoryname': f'''{product.category.categoryname}''',
                'subcategoryname': f'''{product.subcategory.subcategoryname}''',
                'subsubcategory': f'''{product.subsubcategory.subsubcategoryname}''',
                'brand':f'''{product.brand}''',
                'brandimage':f'''{product.brand.imageURL}''',
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

            data.append(d)
        return Response({'data':data})


class ProductAllInfoView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def list(self, request, *args, **kwargs):
        product = self.queryset.order_by('-buy_quantity')
        serializer=self.get_serializer(product,many=True)
        xitproducts=[]
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
                    'price':i.price,
                    'oldprice':i.oldprice,
                    'discount':i.product_discount,
                    'image':img
                }
                color.append(d)
                      
        
            d={
                'id':product.id,
                'categoryname': f'''{product.category.categoryname}''',
                'subcategoryname': f'''{product.subcategory.subcategoryname}''',
                'subsubcategory': f'''{product.subsubcategory.subsubcategoryname}''',
                'brand':f'''{product.brand}''',
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

            xitproducts.append(d)
        return Response({'data':xitproducts})
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        products = self.queryset.filter(id=id)
        data=[]
        for product in products:
            des=DescriptionForProduct.objects.filter(product=id)
            desc=[]
            for i in des:
                d={
                        'id':i.id,
                        'name':i.name,
                        'description':i.description
                    }
                desc.append(d)
            
            PPCaptions=ProductParamsCaption.objects.filter(product=id)
            ppcaption=[]
            for ppc in PPCaptions:
                items=[]
                PPCitems=ProductParamsCaptionitem.objects.filter(productparamscaption=id)
                for item in PPCitems:
                    k={
                        'id':item.id,
                        'paramscell':item.paramscell,
                        'paramscelldecor':item.paramscelldecor,
                    }
                    items.append(k)
               

                d={
                        'id':ppc.id,
                        'name':ppc.captionname,
                        'items':items

                    }
                ppcaption.append(d)
            print(ppcaption)
            
            
            productcolor=ProductColor.objects.filter(product=id)
            color=[]
            for i in productcolor:
                images=ProductImageFile.objects.filter(productscolor=i.id)
                img=[]
                for image in images:
                    d={
                        'id':image.id,
                        'image':image.imageURL,
                    }
                    img.append(d)
                sizes=ProductSize.objects.filter(productscolor=i.id)
                sizess=[]
                for size in sizes:
                    d={
                        'id':size.id,
                        'size':size.size,
                        'quantity':size.quentity,
                    }
                    sizess.append(d)
        
                d={
                    'id':i.id,
                    'id':i.id,
                    'productid':i.product.id,
                    'color':i.colorname,
                    'price':i.price,
                    'oldprice':i.oldprice,
                    'discount':i.product_discount,
                    'image':img,
                    'size':sizess
                }
                color.append(d)

                    
            d={
                'id':product.id,
                'categoryname': f'''{product.category.categoryname}''',
                'subcategoryname': f'''{product.subcategory.subcategoryname}''',
                'subsubcategory': f'''{product.subsubcategory.subsubcategoryname}''',
                'brand':f'''{product.brand}''',
                'productname': f'''{product.productname}''',
                'buy_quantity': f'''{product.buy_quantity}''',
                'imagealt': f'''{product.imagealt}''',
                'addproductUrl': f'''{product.addproductUrl}''',
                'shoppingday':product.shoppingday,
                'product_status':product.product_status,
                'description':desc,
                "additional":ppcaption,
                'colors':color, 
               
            }

            data.append(d)
        return Response({'data':data})


class AddProductJsonView(viewsets.ModelViewSet):
    serializer_class= AddProductJsonSerializer
    def list(self, request, *args, **kwargs):
        return Response({"date":"data"})
    def create(self, request, *args, **kwargs):    
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            # for i in serializer.data['data']:
                # print(i.name)



        #     image_data=base64.decodebytes(bytes(serializer.data['data']['image'], "utf-8"))
        #     imagename = str(uuid.uuid4()) + ".jpeg"
        #     object=Brand.objects.create(
        #         name=serializer.data['data']['name'],
        #         description=serializer.data['data']['description'],
        #         image=ContentFile(image_data, imagename)
        #     )
        #     object.save()

        return Response({"data":"data"})    


    # def create(self, request, *args, **kwargs):    
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer.is_valid())
    #     if serializer.is_valid():
    #         image_data=base64.decodebytes(bytes(serializer.data['data']['image'], "utf-8"))
    #         imagename = str(uuid.uuid4()) + ".jpeg"
    #         object=Brand.objects.create(
    #             name=serializer.data['data']['name'],
    #             description=serializer.data['data']['description'],
    #             image=ContentFile(image_data, imagename)
    #         )
    #         object.save()

    #     return Response({"data":"data"})