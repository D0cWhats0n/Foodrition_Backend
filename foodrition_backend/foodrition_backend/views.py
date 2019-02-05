from django.contrib.auth.models import User
from rest_framework import viewsets
from foodrition_api.models import Food
from foodrition_api.serializers import UserSerializer, FoodSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class FoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows food to be viewed or edited.
    """
    queryset = Food.objects.all().order_by('id')
    serializer_class = FoodSerializer

