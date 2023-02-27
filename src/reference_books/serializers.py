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


class ReferenceBookListViewQueryParamSerializer(serializers.Serializer):
    date = serializers.DateField(required=False)


class ReferenceBookElementListViewQueryParamSerializer(serializers.Serializer):
    version = serializers.CharField(max_length=50, required=False)


class ElementValidationViewQueryParamSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)
    value = serializers.CharField(max_length=300)
    version = serializers.CharField(max_length=50, required=False)
