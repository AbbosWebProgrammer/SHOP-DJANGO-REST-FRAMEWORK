from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category 
        fields="__all__"
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Subcategory 
        fields="__all__"
class SubsubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Subsubcategory 
        fields="__all__"
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model= Brand 
        fields="__all__"
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields="__all__"
class DescriptionForProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= DescriptionForProduct
        fields="__all__"

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductColor
        fields="__all__"  

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductSize
        fields="__all__"
class ProductImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductImageFile
        fields="__all__"

class ProductParamsCaptionSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductParamsCaption
        fields="__all__"

class ProductParamsCaptionitemSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductParamsCaptionitem
        fields="__all__"

class AddProductJsonSerializer(serializers.Serializer):
    data = serializers.JSONField(required=True)


