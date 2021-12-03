from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from rest_framework import viewsets
from knox.models import AuthToken
from .serializer import * 
from AuthAPP.models import Location
from random import choice
from django.conf import settings
import json
import base64
import uuid

import requests
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.save()
            # "user": UserSerializer(user, context=self.get_serializer_context()).data,
            return Response({
            "token": AuthToken.objects.create(user)[1],
            "phone": str(user.phone),
            "staff": user.is_staff,
            "admin": user.admin,
            "is_active": user.is_active,
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "lastname": user.lastname,
            "email": user.email,
            "birthday": user.birthday,
            "image": user.imageURL,
            })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user) 
        log=super(LoginAPI, self).post(request, format=None)
        user=User.objects.get(phone=user.phone)
      
        return Response({
            "phone": str(user.phone),
            "token": log.data['token'],
            "staff": user.is_staff,
            "admin": user.admin,
            "is_active": user.is_active,
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "lastname": user.lastname,
            "email": user.email,
            "birthday": user.birthday,
            "image": user.imageURL
            })



class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': f'''{status.HTTP_200_OK}''',
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserInfoView(generics.UpdateAPIView):
    queryset=User.objects.all()
    serializer_class = ChangeUserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
        
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.object.username=request.data["username"]
                self.object.firstname=request.data["firstname"]
                self.object.lastname=request.data["lastname"]
                self.object.email=request.data["email"]
                self.object.birthday=request.data["birthday"]
                if request.data["image"]:
                    self.object.image=request.data["image"]
                self.object.save()
                data=[]
                d={
                    "username":self.object.username,
                    "firstname":self.object.firstname,
                    "lastname":self.object.lastname,
                    "email":self.object.email,
                    "birthday":self.object.birthday,
                    "image":self.object.imageURL,
                }
                data.append(d)

                response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'User data updated successfully',
                'data':data}

                return Response(response)
            except Exception as e:
                response = {
                'status': 'failed',
                'message': 'User with this Username already exists.'}
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ClientphoneView(generics.GenericAPIView):
    serializer_class=ClientphoneSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        
        password = self.generate_code()
        obj, created =CheckTheSmsCodeSentToThePhone.objects.get_or_create(
                    phone=f'{phone}'
                )
        obj.smscode=password
        obj.save()
        k=self.sendphonepassword(phone[1:],password)
        if "waiting" in str(k):  
            return Response({"message":"Password yuborildi."})
        else:
            return Response({"message":"Password yuborilmadi."})
            
    def sendphonepassword(self,phone,password):
        url = "http://notify.eskiz.uz/api/message/sms/send"
        payload={'mobile_phone': f'{phone}',
        'message': f'{password}',
        'from': '4546',
        'callback_url': 'http://0000.uz/test.php'}
        files=[ ]
        headers = {
        'Authorization': f'''Bearer {settings.SMSTOKEN}'''
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        dic = json.loads(f'''{response.text}''')
        if dic['message']=="Token has expired":
            self.refresh()
            self.sendphonepassword(phone,password)
        return response.text

    def refresh():
        url = "http://notify.eskiz.uz/api/auth/login"
        payload={'email': 'atadjitdinov@gmail.com',
        'password': '4RQ2lCrYGYxhZkFmGL2snlcLlPGCY9bg8fW3wydE'}
        files=[]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        dic = json.loads(f'''{response.text}''')
        if 'data' in dic.keys() and 'data' in dic['data'].keys(): 
            settings.SMSTOKEN=dic['data']['token']
    def generate_code(self):
        numbers=list('1234567890')
        chars=list('abcdefghijklmnopqrstuvwxyz')
        charS=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        password=''
        for i in range(6):
            c = choice([numbers,chars,charS])
            password+=choice(c)
        password
        return password


class ClientphonecheckView(generics.GenericAPIView):
    serializer_class=ClientphonecheckSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        smscode = serializer.validated_data['smscode']
        if not CheckTheSmsCodeSentToThePhone.objects.filter(phone=f'{phone}'): 
            
            return Response({'Message':f"Telefon raqam ro'yxatdan o'tmagan."})
        else:
            custom = CheckTheSmsCodeSentToThePhone.objects.get(phone=f'{phone}')
            if smscode==custom.smscode:
                return Response({'Message':f"OK"})
            else:
                return Response({'Message':f"Parol noto'g'ri kiritildi."})
         

class LocationView(viewsets.ModelViewSet):
    queryset=Location.objects.all()
    serializer_class=LocationSerializers


class GoodsThatTheCustomerLikesView(viewsets.ModelViewSet):
    serializer_class= ReviewJsonSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def list(self,request, *args, **kwargs):
        return Response({"data":"data"})

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)    

        if serializer.is_valid(raise_exception=True) and request.user.is_authenticated:
            product=serializer.data['data']['product']
            user=self.get_object().id
            user = User.objects.get(id=user)
            product = Product.objects.get(id=product)
            try:
                object,create=GoodsThatTheCustomerLikes.objects.get_or_create(
                    user=user,
                    product=product
                )
                object.like=True
                object.save()
                
                response = {
                'status': 'success',
                }
                return Response(response)
            except Exception as e:
                response = {
                'status': 'failed',
                'Error':f'''{e}'''}
                return Response(response)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(viewsets.ModelViewSet):
    queryset=Order.objects.all()
    serializer_class= OrderSerializer
    def list(self, request, *args, **kwargs):
        serializer=self.get_serializer(self.queryset,many=True)
        orders=[]

        for order in serializer.data:
            ord=Order.objects.get(id=order["id"])
            orderdetail=OrderDetail.objects.filter(order=ord.id)
            quantity=0
            sum=0
            for i in orderdetail:
                quantity+=i.quantity
                sum+=i.total
            print(len(orderdetail))
   
            d={
                'id':ord.id,
                'phone':f'''{ord.phone}''',
                'firstname':f'''{ord.firstname}''',
                'lastname':f'''{ord.lastname}''',
                'email':f'''{ord.email}''',
                'city':f'''{ord.city}''',
                'district':f'''{ord.district}''',
                'street':f'''{ord.street}''',
                'status':ord.status,
                'productstypequantity':len(orderdetail),
                'quantity':quantity,
                'sum':sum,
                'day': ord.day,
                'time': ord.time,
            }
            orders.append(d)
        return Response({'orders':orders})
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        ordd = self.queryset.filter(id=id)
        serializer = self.get_serializer(ordd,many=True)
        orders=[]
        for order in serializer.data:
            ord=Order.objects.get(id=order["id"])
            orderdetail=OrderDetail.objects.filter(order=ord.id)
            
            quantity=0
            sum=0
            for i in orderdetail:
                quantity+=i.quantity
                sum+=i.total
            d={
                'id':ord.id,
                'phone':f'''{ord.phone}''',
                'firstname':f'''{ord.firstname}''',
                'lastname':f'''{ord.lastname}''',
                'email':f'''{ord.email}''',
                'city':f'''{ord.city}''',
                'district':f'''{ord.district}''',
                'street':f'''{ord.street}''',
                'status':ord.status,
                'productstypequantity':len(orderdetail),
                'quantity':quantity,
                'sum':sum,
                'day': ord.day,
                'time': ord.time,
            }
            orders.append(d)
        return Response({'orders':orders})
      
    def update(self, request, *args, **kwargs):
        id = kwargs['pk']
        status=request.data.get("status")
        order_status = self.queryset.get(id=id)
        order_status.status=status
        order_status.save()
        return Response({'status':order_status.status})
            

class OrderDetailView(viewsets.ModelViewSet):
    queryset=OrderDetail.objects.all()
    serializer_class= OrderDetailSerializer
    def list(self, request, *args, **kwargs):
        serializer=self.get_serializer(self.queryset,many=True)
        orders_details=[]
        for ordd in serializer.data:
            orderdetail=OrderDetail.objects.get(id=ordd['id'])

            d={
                'id':orderdetail.id,
                'order': f'''{orderdetail.order.phone}''',
                'category':f'''{orderdetail.product.category}''',
                'subcategory':f'''{orderdetail.product.subcategory}''',
                'subsubcategory':f'''{orderdetail.product.subsubcategory}''',
                'brand':f'''{orderdetail.product.brand}''',
                'product': orderdetail.product.name,
                'productscolor':orderdetail.productscolor.colorname,
                'productsize': orderdetail.productsize.size,
                'quantity': orderdetail.quantity,
                'sum':orderdetail.total,
                'day': orderdetail.order.day,
                'time': orderdetail.order.time,
            }
            orders_details.append(d)
        return Response({'orders_details':orders_details})
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        orderd = self.queryset.filter(id=id)
        serializer = self.get_serializer(orderd,many=True)
        ordd = serializer.data
        ordd=ordd[0]

        orderDetail=[]
        orderdetail=OrderDetail.objects.get(id=ordd['id'])
        d={
            'id':orderdetail.id,
                'order': f'''{orderdetail.order.phone}''',
                'category':f'''{orderdetail.product.category}''',
                'subcategory':f'''{orderdetail.product.subcategory}''',
                'subsubcategory':f'''{orderdetail.product.subsubcategory}''',
                'brand':f'''{orderdetail.product.brand}''',
                'product': orderdetail.product.name,
                'productscolor':orderdetail.productcolor.colorname,
                'productsize': orderdetail.productsize.size,
                'quantity': orderdetail.quantity,
                'sum':orderdetail.total,
        }
        orderDetail.append(d)
        return Response({'orderDetail':orderDetail})


class OrderDetailsByOrderIdView(viewsets.ModelViewSet):
    queryset=OrderDetail.objects.all()
    serializer_class= OrderDetailSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        ordd = self.queryset.filter(order=id)
        serializer = self.get_serializer(ordd,many=True)
        orders_details=[]
        for ordd in serializer.data:
            orderdetail=OrderDetail.objects.get(id=ordd['id'])
            d={
               
                'id':orderdetail.id,
                'order': f'''{orderdetail.order.phone}''',
                'category':f'''{orderdetail.product.category}''',
                'subcategory':f'''{orderdetail.product.subcategory}''',
                'brand':f'''{orderdetail.product.brand}''',
                'product': orderdetail.product.productname,
                'productscolor':orderdetail.productcolor.colorname,
                'productsize': str(orderdetail.productsize),
                'quantity': orderdetail.quantity,
                'productprice':orderdetail.price,
                'productoldprice':orderdetail.oldprice,
                'productdiscount':orderdetail.discount,
                'totalprice':orderdetail.totalprice,
            }
            orders_details.append(d)
        return Response({'orders_details':orders_details})



class OrdersByDayView(viewsets.ModelViewSet):
    queryset=Order.objects.all()
    serializer_class= OrderSerializer


class QuestionForProductView(viewsets.ModelViewSet):
    queryset=QuestionForProduct.objects.all()
    serializer_class= QuestionSerializer
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                product=serializer.data['data']['product']
                question=serializer.data['data']['question']
                user= self.get_object()
                question=QuestionForProduct.objects.create(
                                            user=user.id,
                                            product=product,
                                            question=question)
                question.save()
                return Response({'status':'OK'})


class AnsertoquestionView(viewsets.ModelViewSet):
    queryset=Answertoquestion.objects.all()
    serializer_class= AnswertoquestionSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                question=serializer.data['data']['question']
                anwer=serializer.data['data']['answer']
                user= self.get_object()
                question=Answertoquestion.objects.create(
                                            user=user.id,
                                            question=question,
                                            anwer=anwer)
                question.save()
                return Response({'status':'OK'})

class ReviewView(viewsets.ModelViewSet):
    queryset=Review.objects.all()
    serializer_class= ReviewSerializer

class ReviewJsonView(viewsets.ModelViewSet):
    serializer_class= ReviewJsonSerializer
      
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                data=serializer.data['data']
                product=serializer.data['data']['product']
                text=serializer.data['data']['text']
                ball=serializer.data['data']['ball']
                user= self.get_object().id
                user = User.objects.get(id=user)
                product = Product.objects.get(id=product)
                review=Review.objects.create(
                                            product=product,
                                            user=user.id,
                                            text=text,
                                            ball=ball,
                )
                review.save()
                images=serializer.data['data']['images']

                for i in images:
                    image=base64.decodebytes(bytes(i['image'], "utf-8"))
                    imagename = str(uuid.uuid4()) + ".jpeg"
                    image=ImagesReview.objects.create(
                        review=review.id,
                        image=ContentFile(image, imagename)
                    )
                    image.save()
                return Response({'status':'OK'})

        else:
            return Response({"json":"not defined"})



class ImagesReviewView(viewsets.ModelViewSet):
    queryset=ImagesReview.objects.all()
    serializer_class= ImagesReviewSerializer


class OrderAndOrderDetailsJsonSerializerView(viewsets.ModelViewSet):
    serializer_class= OrderAndOrderDetailsJsonSerializer
    def list(self, request, *args, **kwargs):
        return Response({"date":[]})
    
  
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                data=serializer.data['data']
                location=serializer.data['data']['location']
                user= self.get_object().id
                user = User.objects.get(id=user)
                order=Order.objects.create(
                                            user=user,
                                            phone=user.phone,
                                            firstname=user.firstname,
                                            lastname=user.lastname,
                                            email=user.email,
                                            city=location['city'],
                                            district=location['district'],
                                            street=location['street']
                )
                order.save()
                order_details=serializer.data['data']['order_details']
                for i in order_details:
                    ordd=OrderDetail.objects.create(
                        order=order.id,
                        product=i['product'],
                        productcolor=i['productscolor'],
                        productsize=i['productsize'],
                        quantity=i['quantity']
                    )
                    ordd.save()
                return Response({'status':'OK'})
            else:
                data=serializer.data['data']
                location=serializer.data['data']['location']
                user= serializer.data['data']['order']
                order=Order.objects.create(
                                            phone=user['phone'],
                                            firstname=user['firstname'],
                                            lastname=user['lastname'],
                                            email=user['email'],
                                            city=location['city'],
                                            district=location['district'],
                                            street=location['street']
                )
                order.save()
                order_details=serializer.data['data']['order_details']
                for i in order_details:
                    product=i['product']
                    productscolor=i['productscolor']
                    productsize=i['productsize']
                    if i['product']!='':
                        product = User.objects.get(id=int(product))
                    if i['productscolor']!='':
                        productscolor = User.objects.get(id=int(productscolor))
                    if i['productsize']!='':
                        productsize = User.objects.get(id=int(productsize))

                    ordd=OrderDetail.objects.create(
                        order=order.id,
                        product=product,
                        productcolor=productscolor,
                        productsize=productsize,
                        quantity=i['quantity']
                    )
                    ordd.save()
                return Response({'status':'OK'})

        else:
            return Response({"json":"not defined"})



class TheSellerAddedAnOrderJsonSerializerView(viewsets.ModelViewSet):
    serializer_class= OrderAndOrderDetailsJsonSerializer
    def list(self, request, *args, **kwargs):
        return Response({"date":[]})
    
  
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("salom")
        if serializer.is_valid():
            if request.user.is_authenticated:
                vendor=self.get_object()
                data=serializer.data['data']
                location=serializer.data['data']['location']
                user= serializer.data['data']['order']
                user = User.objects.get(id=user)
                order=Order.objects.create(
                                            phone=user['phone'],
                                            firstname=user['firstname'],
                                            lastname=user['lastname'],
                                            email=user['email'],
                                            city=location['city'],
                                            district=location['district'],
                                            street=location['street'],
                                            vendoradd=True,
                                            vendorphone=vendor.phone,
                                            vendorfistname=vendor.firstname,
                                            vendorlastname=vendor.lastname
                )
                order.save()
                order_details=serializer.data['data']['order_details']
                for i in order_details:
                    product=i['product']
                    productscolor=i['productscolor']
                    productsize=i['productsize']
                    if i['product']!='':
                        product = User.objects.get(id=int(product))
                    if i['productscolor']!='':
                        productscolor = User.objects.get(id=int(productscolor))
                    if i['productsize']!='':
                        productsize = User.objects.get(id=int(productsize))

                    ordd=OrderDetail.objects.create(
                        order=order.id,
                        product=product,
                        productcolor=productscolor,
                        productsize=productsize,
                        quantity=i['quantity']
                    )
                    ordd.save()
                return Response({'status':'OK'})

        else:
            return Response({"json":"not defined"})


