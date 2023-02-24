from rest_framework import serializers

from . import models


class ReferenceBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferenceBook
        fields = ["id", "code", "name"]


class ReferenceBookElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferenceBookElement
        fields = ['code', 'value']
