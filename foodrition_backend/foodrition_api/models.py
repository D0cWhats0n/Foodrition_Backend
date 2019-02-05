from django.db import models


class Food(models.Model):
    name = models.CharField(null=False, max_length=100)
    protein = models.FloatField(null=True, blank=True)
