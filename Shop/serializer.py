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
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Products
        fields="__all__"
class DescproductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Descproduct
        fields="__all__"

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductsColor
        fields="__all__"    

class GetColorByProductIdSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductsColor
        fields="__all__"  
class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductSize
        fields="__all__"
class ImagefilesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Imagefiles
        fields="__all__"

class ProductParamsCaptionSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductParamsCaption
        fields="__all__"

class ProductParamsCaptionitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductParamsCaptionitems
        fields="__all__"


class CreateProductsSerializer(serializers.ModelSerializer):
    user = ProductsSerializer(required=False)
    class Meta:
        model = ProductsColor
        fields = '__all__'





