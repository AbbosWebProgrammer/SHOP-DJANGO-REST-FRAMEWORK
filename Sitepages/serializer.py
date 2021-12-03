from rest_framework import serializers
from .models import *

class ShoppingDayForHomePageCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model= ShoppingDayForHomePageCarousel
        fields="__all__"


class MainPagePromoForHomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model= MainPagePromoForHomePage
        fields="__all__"

class MainPagePromoForHomePageSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model= MainPagePromoForHomePageSlider
        fields="__all__"

class AdvertisingForCategoryMenuViewSerializer(serializers.ModelSerializer):
    class Meta:
        model= AdvertisingForCategoryMenu
        fields="__all__"

class ShoppingDayForCategoryCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model= ShoppingDayForCategoryCarousel
        fields="__all__"
        
class MainPagePromoForCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= MainPagePromoForCategory
        fields="__all__"



class ShoppingDayForBrandCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model= ShoppingDayForBrandCarousel
        fields="__all__"

class MainPagePromoForBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model= MainPagePromoForBrand
        fields="__all__"





