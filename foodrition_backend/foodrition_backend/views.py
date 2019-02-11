from django.contrib.auth.models import User
from rest_framework import viewsets
from foodrition_api.models import Food, FoodImage
from foodrition_api.serializers import UserSerializer, FoodSerializer
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from foodrition_api.services.ml_model import ModelFactory
from rest_framework.decorators import api_view


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


class ClassificationAPI(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        
        predict_id = ModelFactory.predict(f)

        food_image = FoodImage()
        food_image.img.save(f.name, f, save=True)
        food_image.classification = predict_id
        food_image.save()
        print(f"Predicted Id for file upload {predict_id}")
        return Response(status=status.HTTP_200_OK)