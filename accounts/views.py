from rest_framework import viewsets
from .models import *
from .serializer import * 

class UserView(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=Userserializers