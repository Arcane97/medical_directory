from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import models
from . import serializers


class ReferenceBookListView(GenericViewSet):
    queryset = models.ReferenceBook.objects.all()
    serializer_class = serializers.ReferenceBookSerializer

    # todo фильтрация с date

    def list(self, request, *args, **kwargs):
        """
        Если нужен будет пагинатор, убрать этот метод и в пагинаторе, вместо "results", указать "refbooks".
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {"refbooks": serializer.data}
        return Response(data)
