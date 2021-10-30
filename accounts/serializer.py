from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class Userserializers(serializers.ModelSerializer):
    class Meta:
        model= User
        fields="__all__"