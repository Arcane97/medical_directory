from django.utils.timezone import localdate
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import models
from . import serializers


class ReferenceBookListView(GenericViewSet):
    queryset = models.ReferenceBook.objects.all().only("id", "code", "name").order_by('id')
    serializer_class = serializers.ReferenceBookSerializer

    def get_queryset(self):
        # todo вынести фильтрацию в другое место
        queryset = super().get_queryset()
        date = self.request.query_params.get("date", None)
        if date is not None:
            queryset = queryset.filter(referencebookversion__date__lte=date).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Если нужен будет пагинатор, убрать этот метод и в пагинаторе, вместо "results", указать "refbooks".
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {"refbooks": serializer.data}
        return Response(data)


class ReferenceBookElementListView(GenericViewSet):
    queryset = models.ReferenceBookElement.objects.all().only("code", "value")
    serializer_class = serializers.ReferenceBookElementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(ref_book_version__ref_book_id=self.kwargs["id"])
        version = self.request.query_params.get("version", None)
        if version is not None:
            queryset = queryset.filter(ref_book_version__version=version)
        else:
            # Будем брать текущую версию. Текущей является та версия, дата начала действия
            # которой позже всех остальных версий данного справочника, но не позже текущей даты.
            date = localdate()
            latest_version = (
                models.ReferenceBookVersion.objects
                .filter(date__lte=date)
                .only("id")
                .order_by("date").last()
            )
            queryset = queryset.filter(ref_book_version_id=latest_version)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Если нужен будет пагинатор, убрать этот метод,
        использовать mixins.ListModelMixin,
        и в пагинаторе, вместо "results", указать "elements".
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {"elements": serializer.data}
        return Response(data)
