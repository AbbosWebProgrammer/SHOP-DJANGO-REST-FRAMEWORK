from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','password']
        extra_kwargs = {'password': {'write_only': True}}

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['phone','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['phone'],validated_data['password'])
        return user



class ClientphoneSerializer(serializers.Serializer):
    phone = serializers.RegexField("^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$")

class ClientphonecheckSerializer(serializers.Serializer):
    phone = serializers.RegexField("^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$")
    smscode = serializers.CharField(max_length=6)


class Customerserializers(serializers.ModelSerializer):
    class Meta:
        model= Customer
        fields="__all__"

class Locationserializers(serializers.ModelSerializer):
    class Meta:
        model= Location
        fields=["customer","latitude","longitude"]

class CustomerLikeserializers(serializers.ModelSerializer):
    class Meta:
        model= CustomerLike
        fields="__all__"


class Customercardserializers(serializers.ModelSerializer):
    class Meta:
        model= Customercard
        fields="__all__"

class Ordersserializers(serializers.ModelSerializer):
    class Meta:
        model= Orders
        fields="__all__"

class Order_detailsserializers(serializers.ModelSerializer):
    class Meta:
        model= Order_details
        fields="__all__"


class Questionserializers(serializers.ModelSerializer):
    class Meta:
        model= Question
        fields="__all__"
class Answertoquestionserializers(serializers.ModelSerializer):
    class Meta:
        model= Answertoquestion
        fields="__all__"

class Reviewserializers(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields="__all__"

class ImagesReviewserializers(serializers.ModelSerializer):
    class Meta:
        model= ImagesReview
        fields="__all__"