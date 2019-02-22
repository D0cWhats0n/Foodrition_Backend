from django.contrib.auth.models import User
from .models import Food
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class FoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Food
        fields = ('ndb_no', 'name', 'water_g', 'energy_kcal', 'protein_g', 'lipid_g',
                  'carbohydrt_g', 'fiber_g', 'sugar_g')