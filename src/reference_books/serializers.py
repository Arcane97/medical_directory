from rest_framework import serializers

from . import models


class ReferenceBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferenceBook
        fields = ["id", "code", "name"]
