from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()



class AuthTokenSerializer(serializers.Serializer):
    phone = serializers.RegexField("^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$",write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        print(phone)
        print(password)
        
        if phone and password:
                      
            user = authenticate(request=self.context.get('request'),
                                phone=phone, password=password)

            print(user)
            if not user:
                msg = _('Phone or Password entered incorrectly..')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "phone" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','password']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['phone'],validated_data['password'])
        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    
class ChangeUserInfoSerializer(serializers.Serializer):
    model = User
    username = serializers.CharField(required=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    birthday=serializers.DateField(required=True)
    image=serializers.ImageField(required=True)

class ClientphoneSerializer(serializers.Serializer):
    phone = serializers.RegexField("^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$")

class ClientphonecheckSerializer(serializers.Serializer):
    phone = serializers.RegexField("^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$")
    smscode = serializers.CharField(max_length=6)


class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model= Location
        fields="__all__"

class GoodsThatTheCustomerLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model= GoodsThatTheCustomerLikes
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields="__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= OrderDetail
        fields="__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model= QuestionForProduct
        fields="__all__"
class AnswertoquestionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Answertoquestion
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields="__all__"

class ImagesReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= ImagesReview
        fields="__all__"


class OrderAndOrderDetailsJsonSerializer(serializers.Serializer):
    data = serializers.JSONField(required=True)


class TheSellerAddedAnOrderJsonSerializer(serializers.Serializer):
    data = serializers.JSONField(required=True)

class ReviewJsonSerializer(serializers.Serializer):
    data = serializers.JSONField(required=True)

