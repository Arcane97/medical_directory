from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import models
from . import serializers
from . import services


class ReferenceBookListView(GenericViewSet):
    queryset = models.ReferenceBook.objects.all().only("id", "code", "name").order_by('id')
    serializer_class = serializers.ReferenceBookSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get("date", None)
        if date is not None:
            queryset = queryset.filter(referencebookversion__date__lte=date).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Если нужен будет пагинатор, убрать этот метод и в пагинаторе, вместо "results", указать "refbooks".
        """
        query_params_serializer = serializers.ReferenceBookListViewQueryParamSerializer(data=self.request.query_params)
        if not query_params_serializer.is_valid():
            return Response(query_params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {"refbooks": serializer.data}
        return Response(data)


class ReferenceBookElementListView(GenericViewSet):
    serializer_class = serializers.ReferenceBookElementSerializer

    def get_queryset(self):
        ref_book_id = self.kwargs["id"]
        version = self.request.query_params.get("version", None)
        queryset = services.get_queryset_of_ref_book_elements(ref_book_id, version)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Если нужен будет пагинатор, убрать этот метод,
        использовать mixins.ListModelMixin,
        и в пагинаторе, вместо "results", указать "elements".
        """
        query_params_serializer = serializers.ReferenceBookElementListViewQueryParamSerializer(
            data=self.request.query_params)
        if not query_params_serializer.is_valid():
            return Response(query_params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {"elements": serializer.data}
        return Response(data)


class ElementValidationView(GenericAPIView):
    """
    Валидация элемента справочника - это проверка на то,
    что элемент с данным кодом и значением присутствует в указанной версии справочника.
    """

    def get(self, request, *args, **kwargs):
        ref_book_id = self.kwargs["id"]
        query_params_serializer = serializers.ElementValidationViewQueryParamSerializer(
            data=self.request.query_params)
        if not query_params_serializer.is_valid():
            return Response(query_params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        exists = services.validate_elements(ref_book_id=ref_book_id, **query_params_serializer.data)
        return Response({"exists": exists})
