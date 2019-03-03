from foodrition_api.services.ml_model import ModelFactory
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import IntegrityError

def foodrition_api_startup_func():
    username = 'guest'
    password = 'bacon'

    try:
        guest_user = User.objects.create_user(username, password)
    except IntegrityError:
        print("User already exists in database! Resetting password...")
        guest_user = User.objects.get(username=username)
        guest_user.set_password(password)
        guest_user.save()

    _ = Token.objects.get_or_create(user=guest_user)

    ModelFactory.load_model_and_maps()