from django.contrib import admin
from .models import *
admin.site.register(CheckTheSmsCodeSentToThePhone)
admin.site.register(Location)
admin.site.register(GoodsThatTheCustomerLikes)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(QuestionForProduct)
admin.site.register(Answertoquestion)
admin.site.register(Review)
admin.site.register(ImagesReview)


