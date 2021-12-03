from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
User = get_user_model()

class Userserializers(serializers.ModelSerializer):
    class Meta:
        model= User
        fields="__all__"