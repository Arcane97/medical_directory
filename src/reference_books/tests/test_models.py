from django.db import IntegrityError
from django.test import TestCase
from ..models import ReferenceBook, ReferenceBookVersion, ReferenceBookElement
from django.utils import timezone


class ReferenceBookTestCase(TestCase):
    def setUp(self):
        self.ref_book = ReferenceBook.objects.create(
            code='ref_book1',
            name='Справочник 1',
            description='This is Справочник 1'
        )

    def test_reference_book_creation(self):
        self.assertEqual(self.ref_book.code, 'ref_book1')
        self.assertEqual(self.ref_book.name, 'Справочник 1')
        self.assertEqual(self.ref_book.description, 'This is Справочник 1')

    def test_unique_code_constraint(self):
        """
        Проверка уникальности поля code.
        """
        with self.assertRaises(IntegrityError):
            ref_book = ReferenceBook.objects.create(
                code='ref_book1',
                name='Справочник 1',
                description='This is Справочник 1'
            )


class ReferenceBookVersionTestCase(TestCase):
    def setUp(self):
        self.ref_book = ReferenceBook.objects.create(
            code='ref_book1',
            name='Справочник 1'
        )
        self.version = ReferenceBookVersion.objects.create(
            ref_book=self.ref_book,
            version='1.0',
            date=timezone.now()
        )

    def test_reference_book_version_creation(self):
        self.assertEqual(self.version.ref_book, self.ref_book)
        self.assertEqual(self.version.version, '1.0')
        self.assertIsNotNone(self.version.date)

    def test_unique_version_constraint(self):
        """
        Проверка уникальности полей 'ref_book' и 'version'.
        """
        date = timezone.now()
        with self.assertRaises(IntegrityError):
            version = ReferenceBookVersion.objects.create(
                ref_book=self.ref_book,
                version='1.0',
                date=date
            )

    def test_unique_date_constraint(self):
        """
        Проверка уникальности полей 'ref_book' и 'date'.
        """
        with self.assertRaises(IntegrityError):
            version = ReferenceBookVersion.objects.create(
                ref_book=self.ref_book,
                version='2.0',
                date=self.version.date
            )


class ReferenceBookElementTestCase(TestCase):
    def setUp(self):
        self.ref_book = ReferenceBook.objects.create(
            code='ref_book1',
            name='Справочник 1'
        )
        self.version = ReferenceBookVersion.objects.create(
            ref_book=self.ref_book,
            version='1.0',
            date=timezone.now()
        )
        self.element = ReferenceBookElement.objects.create(
            ref_book_version=self.version,
            code='code1',
            value='Value 1'
        )

    def test_reference_book_element_creation(self):
        self.assertEqual(self.element.ref_book_version, self.version)
        self.assertEqual(self.element.code, 'code1')
        self.assertEqual(self.element.value, 'Value 1')

    def test_unique_element_constraint(self):
        """
        Проверка уникальности полей 'ref_book_version' и 'code'.
        """
        with self.assertRaises(IntegrityError):
            element = ReferenceBookElement.objects.create(
                ref_book_version=self.version,
                code='code1',
                value='Value 1'
            )
