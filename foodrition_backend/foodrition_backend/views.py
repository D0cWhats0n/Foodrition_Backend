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
from django.http import JsonResponse

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

    def get_queryset(self):
        """ allow rest api to filter by description """
        queryset = Food.objects.all()
        name = self.request.query_params.get('name', None)
        ndb_no = self.request.query_params.get('ndb_no', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        elif ndb_no is not None:
            queryset = queryset.filter(ndb_no=ndb_no)
        return queryset


class ClassificationAPI(APIView):
    """
    API for classifying images. A JSON containing the classified id
    'pred_id', the corresponding model class description 'food_descr'
    and a mapping to the corresponding nutrition description is 
    returned.
    """
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        print("Request to classify file")
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        
        pred = ModelFactory.predict(f)
        print(f"Predicted Id for file upload {pred.pred_id}")

        print("Object dict: ", pred.__dict__)    
        food_image = FoodImage()
        food_image.img.save(f.name, f, save=True)
        food_image.classification = pred.pred_id
        food_image.save()
        return JsonResponse(pred.__dict__, status=status.HTTP_200_OK)