from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='date',
                description='Дата начала действия в формате ГГГГ-ММ-ДД. </br>'
                            'Если указана, то должны возвратиться только те справочники, '
                            'в которых имеются Версии с Датой начала действия раннее '
                            'или равной указанной.',
                required=False,
                type=OpenApiTypes.DATE,
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.ReferenceBookSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=serializers.ReferenceBookListViewQueryParamSerializer,
                examples=[OpenApiExample(  # todo разобраться почему нет примера
                    'Bad request',
                    summary='Ошибка отправки данных',
                    description='Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD.',
                    value={
                        'date': "Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD.",
                    },
                    response_only=True,
                )],
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        """
        Получение списка справочников (+ актуальных на указанную дату).
        """
        # Если нужен будет пагинатор, убрать этот метод и в пагинаторе, вместо "results", указать "refbooks".
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

    @extend_schema(
        parameters=[
            # OpenApiParameter(
            #     name='id',
            #     description='Идентификатор справочника',
            #     required=True,
            #     type=OpenApiTypes.INT,
            # ),
            OpenApiParameter(
                name='version',
                description='Версия справочника. </br>Если не указана, '
                            'то должны возвращаться элементы текущей версии.'
                            'Текущей является та версия, дата начала действия которой '
                            'позже всех остальных версий данного справочника, '
                            'но не позже текущей даты.',
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.ReferenceBookElementSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=serializers.ReferenceBookElementListViewQueryParamSerializer,
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        """
        Получение элементов заданного справочника
        """
        # Если нужен будет пагинатор, убрать этот метод, использовать mixins.ListModelMixin,
        # и в пагинаторе, вместо "results", указать "elements".
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

    @extend_schema(
        parameters=[
            # OpenApiParameter(
            #     name='id',
            #     description='Идентификатор справочника',
            #     required=True,
            #     type=OpenApiTypes.INT,
            # ),
            OpenApiParameter(
                name='code',
                description='Код элемента справочника',
                required=True,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name='value',
                description='Значение элемента справочника',
                required=True,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name='version',
                description='Версия справочника. </br>Если не указана, '
                            'то должны возвращаться элементы текущей версии.'
                            'Текущей является та версия, дата начала действия которой '
                            'позже всех остальных версий данного справочника, '
                            'но не позже текущей даты.',
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiTypes.BOOL,  # todo поменять
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=serializers.ElementValidationViewQueryParamSerializer,
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        ref_book_id = self.kwargs["id"]
        query_params_serializer = serializers.ElementValidationViewQueryParamSerializer(
            data=self.request.query_params)
        if not query_params_serializer.is_valid():
            return Response(query_params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        exists = services.validate_elements(ref_book_id=ref_book_id, **query_params_serializer.data)
        return Response({"exists": exists})
