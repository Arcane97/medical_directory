from django.db.models import OuterRef, Subquery, QuerySet
from django.utils.timezone import localdate

from . import models


def get_queryset_of_ref_book_elements(ref_book_id: int, version: str | None = None) -> QuerySet:
    """
    Получение QuerySet элементов заданного справочника ref_book_id.
    :ref_book_id: id справочника.
    :version: Версия справочника.
              Если не указана, то должны возвращаться элементы текущей версии.
              Текущей является та версия, дата начала действия которой позже всех остальных версий данного справочника,
              но не позже текущей даты.
    :return: QuerySet элементов заданного справочника.
    """
    queryset = (
        models.ReferenceBookElement.objects
        .filter(ref_book_version__ref_book_id=ref_book_id)
        .only("code", "value")
    )
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


def validate_elements(ref_book_id: int, code: str, value: str, version: str | None = None) -> bool:
    """
    Проверка на то, что элемент с данным кодом (code) и значением (value) присутствует в указанной версии справочника.
    :ref_book_id: id справочника.
    :code: Код элемента справочника.
    :value: Значение элемента справочника.
    :version: Версия справочника.
              Если не указана, то должны возвращаться элементы текущей версии.
              Текущей является та версия, дата начала действия которой позже всех остальных версий данного справочника,
              но не позже текущей даты.
    :return: Флаг, присутствует (True), не присутствует (False).
    """
    queryset = get_queryset_of_ref_book_elements(ref_book_id, version)
    queryset = queryset.filter(code=code, value=value)
    return queryset.exists()
