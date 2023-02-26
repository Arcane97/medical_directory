from django.test import TestCase
from django.utils.timezone import localdate

from .. import models
from ..serializers import ReferenceBookSerializer, ReferenceBookElementSerializer


class ReferenceBookSerializerTestCase(TestCase):
    def setUp(self):
        self.book = models.ReferenceBook.objects.create(
            code='ref_book1',
            name='Справочник 1',
            description='A test ref_book1'
        )

    def test_serialized_fields(self):
        serializer = ReferenceBookSerializer(instance=self.book)
        data = serializer.data
        self.assertEqual(list(data.keys()), ['id', 'code', 'name'])
        self.assertEqual(data['id'], self.book.id)
        self.assertEqual(data['code'], self.book.code)
        self.assertEqual(data['name'], self.book.name)


class ReferenceBookElementSerializerTestCase(TestCase):
    def setUp(self):
        self.book = models.ReferenceBook.objects.create(
            code='ref_book1',
            name='Справочник 1'
        )
        self.version = models.ReferenceBookVersion.objects.create(
            ref_book=self.book,
            version='1.0',
            date=localdate(),
        )
        self.element = models.ReferenceBookElement.objects.create(
            ref_book_version=self.version,
            code='code1',
            value='Value 1'
        )

    def test_serialized_fields(self):
        serializer = ReferenceBookElementSerializer(instance=self.element)
        data = serializer.data
        self.assertEqual(list(data.keys()), ['code', 'value'])
        self.assertEqual(data['code'], self.element.code)
        self.assertEqual(data['value'], self.element.value)
