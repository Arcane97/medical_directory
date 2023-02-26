from datetime import timedelta

from django.db.models import QuerySet
from django.test import TestCase
from django.utils.timezone import localdate

from ..models import ReferenceBook, ReferenceBookVersion, ReferenceBookElement
from ..services import get_queryset_of_ref_book_elements, validate_elements


class ServicesTestCase(TestCase):
    def setUp(self):
        self.ref_book = ReferenceBook.objects.create(code='ref_book1', name='Справочник 1')
        self.version1 = ReferenceBookVersion.objects.create(ref_book=self.ref_book, version='1.0',
                                                            date=localdate() - timedelta(days=1))
        self.version2 = ReferenceBookVersion.objects.create(ref_book=self.ref_book, version='2.0', date=localdate())

        self.element1 = ReferenceBookElement.objects.create(ref_book_version=self.version1, code='1', value='Element 1')
        self.element2 = ReferenceBookElement.objects.create(ref_book_version=self.version2, code='2', value='Element 2')

        ref_book_element_1 = ReferenceBookElement.objects.create(
            code="elem1",
            value="Element 1",
            ref_book_version=self.version2,
        )
        ref_book_element_2 = ReferenceBookElement.objects.create(
            code="elem2",
            value="Element 2",
            ref_book_version=self.version2,
        )
        ref_book_element_3 = ReferenceBookElement.objects.create(
            code="elem3",
            value="Element 3",
            ref_book_version=self.version1,
        )

    def test_get_queryset_of_ref_book_elements_returns_queryset(self):
        queryset = get_queryset_of_ref_book_elements(self.ref_book.id)
        self.assertIsInstance(queryset, QuerySet)

    def test_get_queryset_of_ref_book_elements_returns_elements_of_latest_version(self):
        """
        Проверка того, что функция возвращает элементы последней версии, если версия не указана.
        """
        queryset = get_queryset_of_ref_book_elements(self.ref_book.id)
        self.assertIn(self.element2, queryset)
        self.assertNotIn(self.element1, queryset)

    def test_get_queryset_of_ref_book_elements_returns_elements_of_specified_version(self):
        """
        Проверка того, что функция возвращает элементы указанной версии.
        """
        queryset = get_queryset_of_ref_book_elements(self.ref_book.id, version='1.0')
        self.assertIn(self.element1, queryset)
        self.assertNotIn(self.element2, queryset)

    def test_get_queryset_of_ref_book_elements_returns_nothing_for_invalid_version(self):
        """
        Проверка того, что функция возвращает пустой QuerySet для несуществующей версии.
        """
        queryset = get_queryset_of_ref_book_elements(self.ref_book.id, version='3.0')
        self.assertFalse(queryset)

    def test_get_queryset_of_ref_book_elements_returns_nothing_for_invalid_ref_book_id(self):
        """
        Проверка того, что функция возвращает пустой QuerySet для несуществующего ref_book_id.
        """
        queryset = get_queryset_of_ref_book_elements(999)
        self.assertFalse(queryset)

    def test_validate_elements(self):
        self.assertTrue(validate_elements(self.ref_book.id, code="elem1", value="Element 1"))
        self.assertTrue(validate_elements(self.ref_book.id, code="elem2", value="Element 2"))
        self.assertTrue(validate_elements(self.ref_book.id, code="elem3", value="Element 3", version="1.0"))

        self.assertFalse(validate_elements(self.ref_book.id, code="elem1", value="Element 2"))
        self.assertFalse(validate_elements(self.ref_book.id, code="elem2", value="Element 3"))
        self.assertFalse(validate_elements(self.ref_book.id, code="elem1", value="Element 1", version="1.0"))
