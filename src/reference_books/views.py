from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from . import models
from . import serializers


class ReferenceBookListView(mixins.ListModelMixin, GenericViewSet):
    queryset = models.ReferenceBook.objects.all()
    serializer_class = serializers.ReferenceBookSerializer
    # todo привести ответ к формату как в примере {"refbooks": [{},{}] }
    # todo фильтрация с date
