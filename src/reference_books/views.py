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
        date = self.request.query_params.get('date', None)
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
