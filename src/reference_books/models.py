from django.db import models


class ReferenceBook(models.Model):
    code = models.CharField(
        'Код',
        max_length=100,
        unique=True,
    )
    name = models.CharField(
        'Наименование',
        max_length=300,
    )
    description = models.TextField(
        'Описание',
        blank=True,
    )

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self):
        return f'Справочник `{self.name}`'


class ReferenceBookVersion(models.Model):
    ref_book = models.ForeignKey(
        ReferenceBook,
        on_delete=models.CASCADE,
        verbose_name='Справочник',
    )
    version = models.CharField(
        'Версия',
        max_length=50,
    )
    date = models.DateField(
        'Дата начала действия версии',
    )

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'
        unique_together = [['ref_book', 'version'], ['ref_book', 'date']]


class ReferenceBookElement(models.Model):
    ref_book_version = models.ForeignKey(
        ReferenceBookVersion,
        on_delete=models.CASCADE,
        verbose_name='Версия справочника',
    )
    code = models.CharField(
        'Код элемента',
        max_length=100,
    )
    value = models.CharField(
        'Значение элемента',
        max_length=300,
    )

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
        unique_together = [['ref_book_version', 'code']]
