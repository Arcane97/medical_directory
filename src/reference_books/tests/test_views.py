from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localdate
from rest_framework import status

from .. import models


class ReferenceBookListViewTestCase(TestCase):
    def setUp(self):
        self.ref_book1 = models.ReferenceBook.objects.create(
            code='ref_book1',
            name='Справочник 1',
        )
        self.ref_book2 = models.ReferenceBook.objects.create(
            code='ref_book2',
            name='Справочник 2',
        )
        self.ref_book3 = models.ReferenceBook.objects.create(
            code='ref_book3',
            name='Справочник 3',
        )
        self.version1 = models.ReferenceBookVersion.objects.create(
            ref_book=self.ref_book1,
            version='1.0',
            date=localdate() - timedelta(days=1),
        )
        self.version2 = models.ReferenceBookVersion.objects.create(
            ref_book=self.ref_book2,
            version='1.0',
            date=localdate() + timedelta(days=1),
        )
        self.version3 = models.ReferenceBookVersion.objects.create(
            ref_book=self.ref_book3,
            version='1.0',
            date=localdate() - timedelta(days=1),
        )
        self.element1 = models.ReferenceBookElement.objects.create(
            ref_book_version=self.version1,
            code='code1',
            value='Value 1',
        )
        self.element2 = models.ReferenceBookElement.objects.create(
            ref_book_version=self.version2,
            code='code2',
            value='Value 2',
        )
        self.element3 = models.ReferenceBookElement.objects.create(
            ref_book_version=self.version3,
            code='code3',
            value='Value 3',
        )

    def test_list_all_ref_books(self):
        url = reverse('referencebook-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['refbooks']), 3)
        self.assertEqual(
            list([b['code'] for b in response.data['refbooks']]),
            [self.ref_book1.code, self.ref_book2.code, self.ref_book3.code]
        )

    def test_list_ref_books_with_date(self):
        url = reverse('referencebook-list')
        date = localdate() - timedelta(days=1)
        response = self.client.get(url, {'date': date.isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['refbooks']), 2)
        self.assertEqual(
            list([b['code'] for b in response.data['refbooks']]),
            [self.ref_book1.code, self.ref_book3.code]
        )

# todo добавить тесты для остальных вьюшек
