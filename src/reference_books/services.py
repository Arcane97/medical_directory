from django.db.models import OuterRef, Subquery, QuerySet
from django.utils.timezone import localdate

from . import models


def get_queryset_of_ref_book_elements(ref_book_id: int, version: str | None = None) -> QuerySet:
    queryset = models.ReferenceBookElement.objects.all().only("code", "value")
    queryset = queryset.filter(ref_book_version__ref_book_id=ref_book_id)
    if version is not None:
        queryset = queryset.filter(ref_book_version__version=version)
    else:
        # Будем брать текущую версию. Текущей является та версия, дата начала действия
        # которой позже всех остальных версий данного справочника, но не позже текущей даты.
        current_date = localdate()
        current_version = (
            models.ReferenceBookVersion.objects
            .filter(
                ref_book_id=OuterRef('ref_book_version__ref_book_id'),
                date__lte=current_date,
            )
            .order_by('-date')
            .values('id')[:1]
        )
        queryset = queryset.filter(ref_book_version_id=Subquery(current_version))
    return queryset
