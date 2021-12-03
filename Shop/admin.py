from django.contrib import admin
from .models import *
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Subsubcategory)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(DescriptionForProduct)
admin.site.register(ProductParamsCaption)
admin.site.register(ProductParamsCaptionitem)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
admin.site.register(ProductImageFile)
