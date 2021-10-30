# from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from rest_framework import viewsets
from knox.models import AuthToken
from .serializer import * 
from AuthAPP.models import Location
import json
from random import choice
import requests
class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
            })
         
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)

        return super(LoginAPI, self).post(request, format=None)



class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
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
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ClientphoneView(generics.GenericAPIView):
    serializer_class=ClientphoneSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        
        password = self.generate_code()
        obj, created = Phonesmscodecheck.objects.get_or_create(
                    phone=f'{phone}'
                )
        obj.smscode=password
        obj.save()
        k=self.sendphonepassword(phone[1:],password)
        print(k)
        # k=dict(k)
        # print("waiting")
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
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9ub3RpZnkuZXNraXoudXpcL2FwaVwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MzMyNjE2NzQsImV4cCI6MTYzNTg1MzY3NCwibmJmIjoxNjMzMjYxNjc0LCJqdGkiOiJNUzIyRGlHR2oyTUFmZ080Iiwic3ViIjo1MDgsInBydiI6Ijg3ZTBhZjFlZjlmZDE1ODEyZmRlYzk3MTUzYTE0ZTBiMDQ3NTQ2YWEifQ.VePvxptsCisc9HmRMwFOoPtaPDK-3AnvXNyDjt-YoRU'
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        return response.text
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
        if not Phonesmscodecheck.objects.filter(phone=f'{phone}'): 
            
            return Response({'Message':f"Telefon raqam ro'yxatdan o'tmagan."})
        else:
            custom = Phonesmscodecheck.objects.get(phone=f'{phone}')
            if smscode==custom.smscode:
                return Response({'Message':f"OK"})
            else:
                return Response({'Message':f"Parol not'g'ri kiritildi."})
         



class LocationView(viewsets.ModelViewSet):
    queryset=Location.objects.all()
    serializer_class=Locationserializers

class CustomerLikeView(viewsets.ModelViewSet):
    queryset=CustomerLike.objects.all()
    serializer_class= CustomerLikeserializers

class CustomercardView(viewsets.ModelViewSet):
    queryset=Customercard.objects.all()
    serializer_class= Customercardserializers



class OrdersView(viewsets.ModelViewSet):
    queryset=Orders.objects.all()
    serializer_class= Ordersserializers
    def list(self, request, *args, **kwargs):
        serializer=self.get_serializer(self.queryset,many=True)
        orders=[]
        for order in serializer.data:
            ord=Orders.objects.get(id=order["id"])
            d={
                'id':ord.id,
                'user':f'''{ord.user}''',
                'location':f'''{ord.location.latitude}:{ord.location.longitude}''',
                'status':ord.status,
                'day': ord.day,
                'time': ord.time,
            }
            orders.append(d)
        return Response({'orders':orders})
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        ordd = self.queryset.filter(id=id)
        serializer = self.get_serializer(ordd,many=True)
        order = serializer.data
        order=order[0]
        ord=Orders.objects.get(id=order["id"])

        orders=[]
        d={
            'id':ord.id,
            'user':f'''{ord.user}''',
            'location':f'''{ord.location.latitude}:{ord.location.longitude}''',
            'status':ord.status,
            'day': ord.day,
            'time': ord.time,
        }
        orders.append(d)
        return Response({'order':orders})
    def update(self, request, *args, **kwargs):
        id = kwargs['pk']
        status=request.data.get("status")
        order_status = self.queryset.get(id=id)
        order_status.status=status
        order_status.save()
        return Response({'status':order_status.status})
            



class Order_detailsView(viewsets.ModelViewSet):
    queryset=Order_details.objects.all()
    serializer_class= Order_detailsserializers
    def list(self, request, *args, **kwargs):
        serializer=self.get_serializer(self.queryset,many=True)
        orders_details=[]
        for ordd in serializer.data:
            orderdetail=Order_details.objects.get(id=ordd['id'])
            d={
                'id':orderdetail.id,
                'order': f'''{orderdetail.order.user}''',
                'category':f'''{orderdetail.productscolor.colorname}''',
                'subcategory':f'''{orderdetail.product.subcategory}''',
                'brand':f'''{orderdetail.product.brand}''',
                'product': orderdetail.product.name,
                'productscolor':orderdetail.productscolor.colorname,
                'productsize': orderdetail.productsize.size,
                'quantity': orderdetail.quantity,
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

        order_detail=[]
        orderdetail=Order_details.objects.get(id=ordd['id'])
        d={
            'id':orderdetail.id,
            'order': f'''{orderdetail.order.user}''',
            'category':f'''{orderdetail.productscolor.colorname}''',
            'subcategory':f'''{orderdetail.product.subcategory}''',
            'brand':f'''{orderdetail.product.brand}''',
            'product': orderdetail.product.name,
            'productscolor':orderdetail.productscolor.colorname,
            'productsize': orderdetail.productsize.size,
            'quantity': orderdetail.quantity,
            'day': orderdetail.order.day,
            'time': orderdetail.order.time,
        }

        order_detail.append(d)
        return Response({'order_detail':order_detail})



class Order_detailsByOrderIdView(viewsets.ModelViewSet):
    queryset=Order_details.objects.all()
    serializer_class= Order_detailsserializers
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        ordd = self.queryset.filter(order=id)
        serializer = self.get_serializer(ordd,many=True)
        orders_details=[]
        for ordd in serializer.data:
            orderdetail=Order_details.objects.get(id=ordd['id'])
            d={
                'id':orderdetail.id,
                'order': f'''{orderdetail.order.user}''',
                'category':f'''{orderdetail.productscolor.colorname}''',
                'subcategory':f'''{orderdetail.product.subcategory}''',
                'brand':f'''{orderdetail.product.brand}''',
                'product': orderdetail.product.name,
                'productscolor':orderdetail.productscolor.colorname,
                'productsize': orderdetail.productsize.size,
                'quantity': orderdetail.quantity,
                'day': orderdetail.order.day,
                'time': orderdetail.order.time,
            }
            orders_details.append(d)
        return Response({'orders_details':orders_details})



class OrdersByDayView(viewsets.ModelViewSet):
    queryset=Orders.objects.all()
    serializer_class= Ordersserializers

class QuestionView(viewsets.ModelViewSet):
    queryset=Question.objects.all()
    serializer_class= Questionserializers

class AnsertwoquestionView(viewsets.ModelViewSet):
    queryset=Answertoquestion.objects.all()
    serializer_class= Answertoquestionserializers

class ReviewView(viewsets.ModelViewSet):
    queryset=Review.objects.all()
    serializer_class= Reviewserializers

class ImagesReviewView(viewsets.ModelViewSet):
    queryset=ImagesReview.objects.all()
    serializer_class= ImagesReviewserializers